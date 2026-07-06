import ctypes
import fnmatch
import os
import os.path
import pathlib

from rich import print
from rich.console import Console, ConsoleOptions
from rich.filesize import decimal
from rich.markup import escape
from rich.status import Status
from rich.text import Text
from rich.traceback import install
from rich.tree import Tree

from ._icons import default_file_icon, default_folder_icon, icons, named_icons, folder_icons


install()


IMPORTANT_DOTFILES = {
    ".gitignore",
    ".gitattributes",
    ".editorconfig",
    ".env",
    ".env.example",
    ".env.local",
    ".env.development",
    ".env.production",
    ".npmrc",
    ".babelrc",
    ".eslintrc",
    ".eslintrc.json",
    ".prettierrc",
    ".vscodeignore",
}


def is_hidden(path: pathlib.Path) -> bool:
    name = path.name
    if name in IMPORTANT_DOTFILES:
        return False
    if name.startswith('.'):
        return True
    if os.name == 'nt':
        try:
            attrs = ctypes.windll.kernel32.GetFileAttributesW(str(path))
            if attrs != -1:
                return bool(attrs & 2)  # FILE_ATTRIBUTE_HIDDEN
        except Exception:
            pass
    return False


class GitIgnoreSpec:
    def __init__(self, base_dir: pathlib.Path, patterns: list):
        self.base_dir = base_dir.resolve()
        self.rules = []
        for pat in patterns:
            pat = pat.strip()
            if not pat or pat.startswith('#'):
                continue
            is_negated = pat.startswith('!')
            if is_negated:
                pat = pat[1:]
            
            is_dir_only = pat.endswith('/')
            if is_dir_only:
                pat = pat[:-1]
            
            self.rules.append((pat, is_negated, is_dir_only))

    def matches(self, path: pathlib.Path, is_dir: bool) -> bool:
        try:
            rel_path = path.resolve().relative_to(self.base_dir)
        except ValueError:
            return False
        
        rel_str = rel_path.as_posix()
        parts = rel_path.parts
        
        ignored = False
        for pat, is_negated, is_dir_only in self.rules:
            if is_dir_only and not is_dir:
                continue
            
            match_at_root = pat.startswith('/')
            clean_pat = pat.lstrip('/')
            
            if '/' not in clean_pat:
                matched = any(fnmatch.fnmatch(part, clean_pat) for part in parts)
            else:
                if match_at_root:
                    matched = fnmatch.fnmatch(rel_str, clean_pat) or fnmatch.fnmatch(rel_str, clean_pat + '/*')
                else:
                    matched = (
                        fnmatch.fnmatch(rel_str, clean_pat) or
                        fnmatch.fnmatch(rel_str, '*/' + clean_pat) or
                        fnmatch.fnmatch(rel_str, clean_pat + '/*') or
                        fnmatch.fnmatch(rel_str, '*/' + clean_pat + '/*')
                    )
            
            if matched:
                ignored = not is_negated
                
        return ignored


def load_gitignore(path: pathlib.Path) -> GitIgnoreSpec:
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        return GitIgnoreSpec(path.parent, lines)
    except Exception:
        return None


def is_ignored(path: pathlib.Path, is_dir: bool, gitignore_specs: list) -> bool:
    for spec in gitignore_specs:
        if spec.matches(path, is_dir):
            return True
    return False


def get_icon_for_filename(filename):
    lower_name = filename.lower()
    icon_info = named_icons.get(lower_name)
    if icon_info is not None:
        return icon_info["icon"], icon_info["color"]
    
    if "." in lower_name:
        ext = lower_name.rsplit(".", 1)[-1]
        icon_info = icons.get(ext)
        if icon_info is not None:
            return icon_info["icon"], icon_info["color"]
            
    return default_file_icon["icon"], default_file_icon["color"]

def get_icon_for_directory(filename):
    lower_name = filename.lower()
    icon_info = folder_icons.get(lower_name)
    if icon_info is not None:
        return icon_info["icon"], icon_info["color"]
    return default_folder_icon["icon"], default_folder_icon["color"]

class Options:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


def walk_directory(directory: pathlib.Path, tree: Tree, status: Status, options: Options, depth=None, gitignore_specs=None) -> None:
    """Recursively build a Tree with directory contents."""
    if depth == 0:
        return

    if gitignore_specs is None:
        gitignore_specs = []

    # Parse local .gitignore if not ignoring gitignore rules
    new_specs = list(gitignore_specs)
    if not getattr(options, "no_gitignore", False):
        local_gitignore = directory / ".gitignore"
        if local_gitignore.is_file():
            spec = load_gitignore(local_gitignore)
            if spec:
                new_specs.append(spec)

    # Sort dirs first then by filename
    try:
        entries = sorted(
            os.scandir(directory),
            key=lambda entry: (entry.is_file(), entry.name.lower()),
        )
    except (IOError, PermissionError, FileNotFoundError):
        return

    for entry in entries:
        name = entry.name
        full_path = directory / name

        try:
            is_dir = entry.is_dir()
        except (IOError, PermissionError):
            continue

        is_important = name in IMPORTANT_DOTFILES
        hidden = is_hidden(full_path) if not is_important else False
        ignored = is_ignored(full_path, is_dir, new_specs) if not is_important else False

        # Decide whether to skip this file/directory
        should_skip = False
        
        # If --all is not set, we skip hidden and ignored files
        if not getattr(options, "all_files", False):
            if hidden:
                should_skip = True
            elif ignored:
                should_skip = True
            elif options.ignore_dot and name.startswith(".") and not is_important:
                should_skip = True
        
        if name in options.ignore_files:
            should_skip = True

        if should_skip:
            continue

        # If hidden, ignored, or starts with a dot (and is not an important dev file), style it as "dim"
        is_dim = hidden or ignored or (name.startswith(".") and not is_important)

        if is_dir:
            style = "dim" if (name.startswith("__") or is_dim) else ""
            icon, color = get_icon_for_directory(name)
            if is_dim:
                color = "dim"
            branch = tree.add(
                Text.assemble(
                    Text(icon, style=color),
                    " ",
                    Text(escape(name), style="dim" if is_dim else "default on default"),
                ),
                style=style,
                guide_style=style,
            )
            walk_directory(full_path, branch, status, options, depth=-1 if depth == -1 else (depth - 1), gitignore_specs=new_specs)
        else:
            icon, color = get_icon_for_filename(name)
            text_filename = Text(name, style="dim" if is_dim else "default on default")
            text_filename.stylize(f"link file://{full_path}")
            if options.show_size:
                try:
                    file_size = entry.stat().st_size
                except (IOError, PermissionError):
                    file_size = 0
                text_filename.append(f" ({decimal(file_size)})", "blue" if not is_dim else "dim")
            
            icon_style = "dim" if is_dim else color
            tree.add(Text(icon, style=icon_style) + Text(" ", style="default on default") + text_filename)

            status.update(f"Processing [blue]{full_path}[/]")
