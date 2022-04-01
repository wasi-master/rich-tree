import os
import pathlib

import rich_click as click

from click import Path
from .core import walk_directory, Tree, Status, Console, Options
from .__init__ import __version__ as VERSION

click.rich_click.USE_RICH_MARKUP = True
DEFAULT_IGNORE = "venv,node_modules,.git,.history"

@click.command()
@click.argument("directory", default=".", type=Path(exists=True, file_okay=False))
@click.option("--soft", is_flag=True, help="Enable soft wrapping of text.", default=None)
@click.option("--width", "-w", metavar="SIZE", type=int, help="Fit output to [b]SIZE[/] characters.", default=-1)
@click.option("--export-html", "-o", metavar="PATH", default="", help="Write HTML to [b]PATH[/b].")
@click.option("--version", "-v", is_flag=True, help="Print version and exit.")
@click.option("--exclude", "-e", help="Comma seperated list of files and folders to ignore.", default=DEFAULT_IGNORE)
@click.option("--ignore-dot", "-id", is_flag=True, help="Ignore files and directories starting with a period.")
@click.option("--show-size", "-ss", is_flag=True, help="Show the size of each file.", default=False)
@click.option("--depth", "-d", type=int, help="How many levels to show ", default=-1)
def cli(directory, soft, width, export_html, version, exclude, ignore_dot, show_size, depth):
    if version:
        print(f"{VERSION}\n")
        return
    console = Console(soft_wrap=soft, record=bool(export_html))

    exclude = exclude.split(",")

    directory = os.path.abspath(directory)
    options = Options(ignore_files = exclude, ignore_dot=ignore_dot, show_size=show_size, directory=directory, depth=depth)
    tree = Tree(
        f":open_file_folder: [link file://{directory}]{directory}",
        # guide_style="",
    )
    with Status("Preparing") as status:
        walk_directory(pathlib.Path(directory), tree, status, options, depth)
        status.update("Finishing up")
        console.print(tree, width=None if width <= 0 else width)
        if export_html:
            console.save_html(export_html)


if __name__ == "__main__":
    cli()
