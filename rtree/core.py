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


def get_icon_for_filename(filename):
    file_name, file_extension = os.path.splitext(filename)
    if filename.lower() in named_icons:
        return named_icons[filename.lower()]["icon"], named_icons[filename.lower()]["color"]
    if file_extension[1:] in icons:
        return icons[file_extension[1:]]["icon"], icons[file_extension[1:]]["color"]
    return default_file_icon["icon"], default_file_icon["color"]

def get_icon_for_directory(filename):
    if filename.lower() in folder_icons:
        return folder_icons[filename.lower()]["icon"], folder_icons[filename.lower()]["color"]
    return default_folder_icon["icon"], default_folder_icon["color"]

class Options:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


def walk_directory(directory: pathlib.Path, tree: Tree, status: Status, options: Options, depth=None) -> None:
    """Recursively build a Tree with directory contents."""
    if depth == 0:
        return

    # Sort dirs first then by filename
    try:
        paths = sorted(
            pathlib.Path(directory).iterdir(),
            key=lambda path: (path.is_file(), path.name.lower()),
        )
    except (IOError, PermissionError, FileNotFoundError):
        return
    for path in paths:
        try:
            full_path = path.resolve()
        except (IOError, PermissionError, FileNotFoundError):
            # Maybe the full path cannot be gotten for some reason
            full_path = path.name
        if options.ignore_dot:
            # Remove hidden files and directories
            if path.name.startswith("."):
                continue
        if path.name in options.ignore_files:
            continue
        if path.is_dir():
            style = "dim" if path.name.startswith("__") else ""
            icon, color = get_icon_for_directory(path.name)
            branch = tree.add(
                Text.assemble(
                    Text(icon, style=color),
                    " ",
                    Text(escape(path.name), style=f"default on default"),
                ),
                style=style,
                guide_style=style,
            )
            walk_directory(path, branch, status, options, depth = -1 if depth == -1 else (depth-1))
        else:
            icon, color = get_icon_for_filename(path.name)
            text_filename = Text(path.name, style="default on default")
            text_filename.stylize(f"link file://{path}")
            if options.show_size:
                file_size = path.stat().st_size
                text_filename.append(f" ({decimal(file_size)})", "blue")
            tree.add(Text(icon, style=color) + Text(" ", style="default on default") + text_filename)

            status.update(f"Processing [blue]{full_path}[/]")
