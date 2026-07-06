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


def walk_directory(directory: pathlib.Path, tree: Tree, status: Status, options: Options, depth=None) -> None:
    """Recursively build a Tree with directory contents."""
    if depth == 0:
        return

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
        if options.ignore_dot and name.startswith("."):
            continue
        if name in options.ignore_files:
            continue

        full_path = directory / name

        try:
            is_dir = entry.is_dir()
        except (IOError, PermissionError):
            continue

        if is_dir:
            style = "dim" if name.startswith("__") else ""
            icon, color = get_icon_for_directory(name)
            branch = tree.add(
                Text.assemble(
                    Text(icon, style=color),
                    " ",
                    Text(escape(name), style="default on default"),
                ),
                style=style,
                guide_style=style,
            )
            walk_directory(full_path, branch, status, options, depth=-1 if depth == -1 else (depth - 1))
        else:
            icon, color = get_icon_for_filename(name)
            text_filename = Text(name, style="default on default")
            text_filename.stylize(f"link file://{full_path}")
            if options.show_size:
                try:
                    file_size = entry.stat().st_size
                except (IOError, PermissionError):
                    file_size = 0
                text_filename.append(f" ({decimal(file_size)})", "blue")
            tree.add(Text(icon, style=color) + Text(" ", style="default on default") + text_filename)

            status.update(f"Processing [blue]{full_path}[/]")
