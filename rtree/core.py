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


def get_icon_for_chain(chain_entries):
    for entry in reversed(chain_entries):
        icon_info = folder_icons.get(entry.name.lower())
        if icon_info is not None:
            return icon_info["icon"], icon_info["color"]
    for entry in chain_entries:
        icon_info = folder_icons.get(entry.name.lower())
        if icon_info is not None:
            return icon_info["icon"], icon_info["color"]
    return default_folder_icon["icon"], default_folder_icon["color"]


class Options:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


def get_git_status_mapping(directory_path: pathlib.Path) -> dict:
    """Finds git root and gets a dictionary mapping absolute file paths to status string."""
    import subprocess
    import shutil
    if not shutil.which("git"):
        return {}
    try:
        # Get repository root
        res = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=str(directory_path),
            capture_output=True,
            text=True,
            check=True
        )
        git_root = pathlib.Path(res.stdout.strip()).resolve()
        
        # Get git status --porcelain -z
        res_status = subprocess.run(
            ["git", "status", "--porcelain", "-z"],
            cwd=str(git_root),
            capture_output=True,
            text=True,
            check=True
        )
        
        mapping = {}
        # Parse NUL-terminated output
        parts = res_status.stdout.split('\x00')
        i = 0
        while i < len(parts):
            part = parts[i]
            if not part:
                i += 1
                continue
            status_code = part[:2]
            path_str = part[3:]
            if 'R' in status_code or 'C' in status_code:
                # The next element in parts is the destination path
                if i + 1 < len(parts):
                    dest_path = parts[i + 1]
                    abs_dest = (git_root / dest_path).resolve()
                    mapping[abs_dest] = status_code.strip()
                    i += 2
                    continue
            
            abs_path = (git_root / path_str).resolve()
            mapping[abs_path] = status_code.strip()
            i += 1
        return mapping
    except Exception:
        return {}


def format_time(timestamp: float) -> str:
    from datetime import datetime
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def _get_valid_entries(directory: pathlib.Path, options: Options, gitignore_specs: list):
    new_specs = list(gitignore_specs)
    if not getattr(options, "no_gitignore", False):
        local_gitignore = directory / ".gitignore"
        if local_gitignore.is_file():
            spec = load_gitignore(local_gitignore)
            if spec:
                new_specs.append(spec)

    try:
        scanned = sorted(
            os.scandir(directory),
            key=lambda entry: (entry.is_file(), entry.name.lower()),
        )
    except (IOError, PermissionError, FileNotFoundError):
        return [], new_specs

    valid = []
    for entry in scanned:
        name = entry.name
        full_path = directory / name

        try:
            is_dir = entry.is_dir()
        except (IOError, PermissionError):
            continue

        is_important = name in IMPORTANT_DOTFILES
        hidden = is_hidden(full_path) if not is_important else False
        ignored = is_ignored(full_path, is_dir, new_specs) if not is_important else False

        should_skip = False
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

        is_dim = hidden or ignored or (name.startswith(".") and not is_important)
        valid.append((entry, full_path, is_dir, is_dim))

    return valid, new_specs


def walk_directory(directory: pathlib.Path, tree: Tree, status: Status, options: Options, depth=None, gitignore_specs=None) -> None:
    """Recursively build a Tree with directory contents."""
    if depth == 0:
        return

    if gitignore_specs is None:
        gitignore_specs = []

    # Initialize git status mapping on options if requested and not yet initialized
    if getattr(options, "show_git", False) and not hasattr(options, "git_status_mapping"):
        options.git_status_mapping = get_git_status_mapping(directory)

    valid_entries, new_specs = _get_valid_entries(directory, options, gitignore_specs)

    for entry, full_path, is_dir, is_dim in valid_entries:
        name = entry.name

        if is_dir:
            chain = [(entry, full_path, is_dir, is_dim)]
            curr_dir = full_path
            curr_specs = new_specs
            curr_depth = depth

            if getattr(options, "compact", True):
                while curr_depth != 0 and curr_depth != 1:
                    sub_valid, sub_specs = _get_valid_entries(curr_dir, options, curr_specs)
                    if len(sub_valid) == 1 and sub_valid[0][2]:
                        sub_item = sub_valid[0]
                        chain.append(sub_item)
                        curr_dir = sub_item[1]
                        curr_specs = sub_specs
                        if curr_depth > 1:
                            curr_depth -= 1
                    else:
                        break

            if len(chain) == 1:
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
                next_depth = -1 if depth == -1 else (depth - 1)
                walk_directory(full_path, branch, status, options, depth=next_depth, gitignore_specs=new_specs)
            else:
                rel_name = "/".join(item[0].name for item in chain)
                chain_is_dim = any(item[3] or item[0].name.startswith("__") for item in chain)
                style = "dim" if chain_is_dim else ""
                icon, color = get_icon_for_chain([item[0] for item in chain])
                if chain_is_dim:
                    color = "dim"
                branch = tree.add(
                    Text.assemble(
                        Text(icon, style=color),
                        " ",
                        Text(escape(rel_name), style="dim" if chain_is_dim else "default on default"),
                    ),
                    style=style,
                    guide_style=style,
                )
                next_depth = -1 if depth == -1 else (curr_depth - 1)
                walk_directory(curr_dir, branch, status, options, depth=next_depth, gitignore_specs=curr_specs)
        else:
            icon, color = get_icon_for_filename(name)
            text_filename = Text(name, style="dim" if is_dim else "default on default")
            text_filename.stylize(f"link file://{full_path}")
            
            # Fetch stats if needed
            stat = None
            if options.show_size or getattr(options, "show_created", False) or getattr(options, "show_modified", False) or getattr(options, "show_accessed", False):
                try:
                    stat = entry.stat()
                except (IOError, PermissionError):
                    pass

            # Gather file details for parentheses
            stat_infos = []
            if options.show_size and stat:
                stat_infos.append((decimal(stat.st_size), "blue" if not is_dim else "dim"))
            if getattr(options, "show_created", False) and stat:
                stat_infos.append((f"created: {format_time(stat.st_ctime)}", "cyan" if not is_dim else "dim"))
            if getattr(options, "show_modified", False) and stat:
                stat_infos.append((f"modified: {format_time(stat.st_mtime)}", "green" if not is_dim else "dim"))
            if getattr(options, "show_accessed", False) and stat:
                stat_infos.append((f"accessed: {format_time(stat.st_atime)}", "yellow" if not is_dim else "dim"))

            if stat_infos:
                text_filename.append(" (", "dim" if is_dim else "default")
                for idx, (info_text, info_style) in enumerate(stat_infos):
                    if idx > 0:
                        text_filename.append(", ", "dim" if is_dim else "default")
                    text_filename.append(info_text, info_style)
                text_filename.append(")", "dim" if is_dim else "default")

            if getattr(options, "show_git", False):
                git_mapping = getattr(options, "git_status_mapping", {})
                file_status = git_mapping.get(full_path.resolve())
                if file_status:
                    color_map = {
                        "M": "yellow",
                        "A": "green",
                        "D": "red",
                        "??": "magenta",
                        "R": "green",
                        "C": "green",
                        "U": "red",
                    }
                    git_color = color_map.get(file_status, "magenta")
                    if is_dim:
                        git_color = "dim"
                    text_filename.append(f" [{file_status}]", git_color)
            
            icon_style = "dim" if is_dim else color
            tree.add(Text(icon, style=icon_style) + Text(" ", style="default on default") + text_filename)

            status.update(f"Processing [blue]{full_path}[/]")
