import os
import shutil
import sys

import questionary

from rich.columns import Columns  # noqa: F401 — kept for other callers
from rich.panel import Panel
from rich.align import Align
from rich.markdown import Markdown
from rich.box import HEAVY, ROUNDED, SIMPLE
from rich.console import Console
from rich.rule import Rule
from rich.text import Text
from rich.table import Table
from rtree._icons import default_file_icon, default_folder_icon, folder_icons, named_icons, icons

console = Console()

# ──────────────────────────────────────────────
#  Step counter
# ──────────────────────────────────────────────

_TOTAL_STEPS = 3
_current_step = 0


def _step(title: str) -> None:
    global _current_step
    _current_step += 1
    console.print()
    console.print(Rule(
        f"[bold cyan]Step {_current_step}/{_TOTAL_STEPS}[/]  [bold white]{title}[/]",
        style="dim cyan",
    ))


# ──────────────────────────────────────────────
#  Shell detection
# ──────────────────────────────────────────────

def provide_default_shell() -> str:
    if os.name == "posix":
        return os.environ.get("SHELL", "bash")
    elif os.name == "nt":
        return os.environ.get("COMSPEC", "cmd")
    raise NotImplementedError(f"OS {os.name!r} support not available")


def get_shell() -> str:
    try:
        import shellingham
        return shellingham.detect_shell()[0]
    except Exception:
        return provide_default_shell()


# ──────────────────────────────────────────────
#  Icon display
# ──────────────────────────────────────────────

_ICON_CELL_WIDTH = 4   # icon glyph (1–2 wide) + 1 space padding each side
_OUTER_PANEL_OVERHEAD = 5  # top border + title + bottom border + subtitle + blank line
_STEP_HEADER_LINES = 3     # Rule + description line + blank line
_PROMPT_LINES = 1          # questionary prompt


def _icon_budget() -> tuple[int, int]:
    """Return (icons_per_row, max_rows) based on the current terminal size."""
    size = shutil.get_terminal_size(fallback=(80, 24))
    icons_per_row = max(1, (size.columns - 4) // _ICON_CELL_WIDTH)
    reserved = _OUTER_PANEL_OVERHEAD + _STEP_HEADER_LINES + _PROMPT_LINES
    # Each icon row is 1 line tall inside the table (compact grid)
    available_rows = max(1, size.lines - reserved)
    return icons_per_row, available_rows


def show_all_icons() -> None:
    all_icons: dict = {}

    for i in (
        default_file_icon,
        default_folder_icon,
        *folder_icons.values(),
        *named_icons.values(),
        *icons.values(),
    ):
        all_icons.update([tuple(i.values())])

    icon_items = list(all_icons.items())
    total = len(icon_items)

    icons_per_row, max_rows = _icon_budget()
    max_icons = icons_per_row * max_rows
    shown = icon_items[:max_icons]
    hidden = total - len(shown)

    # Build a compact Table grid — no nested Panel boxes, just coloured glyphs
    grid = Table.grid(padding=(0, 1))
    for _ in range(icons_per_row):
        grid.add_column(justify="center", width=2)

    row: list[Text] = []
    for icon, color in shown:
        row.append(Text(icon, style=color))
        if len(row) == icons_per_row:
            grid.add_row(*row)
            row = []
    if row:
        # pad the last partial row so the table renders evenly
        while len(row) < icons_per_row:
            row.append(Text(""))
        grid.add_row(*row)

    subtitle = (
        f"[dim]Showing {len(shown)} of {total} icons · Nerd Fonts[/]"
        if hidden
        else "[dim]Powered by Nerd Fonts[/]"
    )

    console.print(
        Panel(
            Align.center(grid),
            box=HEAVY,
            title="[bold]All Icons[/]",
            subtitle=subtitle,
            border_style="bright_black",
        )
    )


# ──────────────────────────────────────────────
#  Font troubleshooting
# ──────────────────────────────────────────────

def show_font_fix_instructions() -> None:
    text = Text.assemble(
        ("To display icons correctly, you need a ", "yellow"),
        ("Nerd Font", "bold yellow"),
        (" installed and selected in your terminal.\n\n", "yellow"),
        ("  1. ", "bold white"), ("Download a font from  ", "white"),
        ("https://www.nerdfonts.com/font-downloads", "link https://www.nerdfonts.com/font-downloads cyan"),
        ("\n", "default"),
        ("     (Recommended: ", "dim"), ("JetBrainsMono Nerd Font", "bold magenta"),
        (", CaskaydiaCove, or FiraCode Nerd Font)\n\n", "dim"),
        ("  2. ", "bold white"), ("Install it on your system.\n\n", "white"),
        ("  3. ", "bold white"),
        ("In your terminal settings, set the font to the installed Nerd Font.\n\n", "white"),
        ("  4. ", "bold white"), ("Re-run  ", "white"),
        ("rtree --onboard", "bold green"),
        ("  to verify icons look correct.\n", "white"),
        ("     Or, patch your own font at  ", "dim"),
        ("https://github.com/ryanoasis/nerd-fonts#font-patcher", "link https://github.com/ryanoasis/nerd-fonts#font-patcher cyan"),
    )
    console.print(
        Panel(
            text,
            title="[bold yellow]⚠  Icons not rendering correctly[/]",
            border_style="yellow",
            box=ROUNDED,
            padding=(1, 2),
        )
    )


# ──────────────────────────────────────────────
#  Alias instructions
# ──────────────────────────────────────────────

def show_alias_instructions() -> None:
    shell = get_shell()

    instructions = {
        "cmd": (
            "Create a file named `tree.bat` inside `C:\\Windows\\System32` and paste:\n\n"
            "```bat\n@echo off\ncall rtree%*\n```"
        ),
        **dict.fromkeys(
            ["pwsh", "powershell"],
            "Open your PowerShell profile (`echo $profile`) and add:\n\n"
            "```powershell\nNew-Alias tree rtree\n```",
        ),
        **dict.fromkeys(
            ["bash", "zsh"],
            f"Open `~/.{shell}rc` and add:\n\n"
            "```bash\nalias tree=\"rtree\"\n```\n\n"
            f"Then reload your shell with `source ~/.{shell}rc`.",
        ),
    }

    fallback = (
        f"Search online for **how to add aliases to `{shell}`** "
        "and map `tree` → `rtree`."
    )

    body = instructions.get(shell, fallback)

    console.print(
        Panel(
            Markdown(body, inline_code_lexer="shell"),
            title=f"[bold green]Alias setup for [cyan]{shell}[/cyan][/]",
            border_style="green",
            box=ROUNDED,
            padding=(1, 2),
        )
    )


# ──────────────────────────────────────────────
#  Feature showcase
# ──────────────────────────────────────────────

def show_feature_showcase() -> None:
    table = Table(
        show_header=True,
        header_style="bold magenta",
        box=SIMPLE,
        padding=(0, 2),
        expand=True,
    )
    table.add_column("Flag", style="bold green", no_wrap=True)
    table.add_column("Description", style="white")
    table.add_column("Example", style="dim cyan")

    features = [
        ("--show-size / -ss",     "Show file sizes",                      "rtree -ss"),
        ("--show-modified / -sm", "Show last-modified timestamps",         "rtree -sm"),
        ("--show-created / -sc",  "Show creation timestamps",              "rtree -sc"),
        ("--show-accessed / -sa", "Show last-accessed timestamps",         "rtree -sa"),
        ("--show-git / -sg",      "Overlay git status on each file",       "rtree -sg"),
        ("--depth / -d",          "Limit tree depth",                      "rtree -d 3"),
        ("--exclude / -e",        "Exclude folders (comma-separated)",     "rtree -e dist,build"),
        ("--ignore-dot / -id",    "Hide dotfiles",                         "rtree -id"),
        ("--all / -a",            "Show hidden & git-ignored files",       "rtree -a"),
        ("--export-html / -o",    "Save tree as an HTML file",             "rtree -o out.html"),
    ]

    for flag, desc, example in features:
        table.add_row(flag, desc, example)

    console.print(
        Panel(
            table,
            title="[bold]✨  What you can do with rtree[/]",
            border_style="magenta",
            box=ROUNDED,
            padding=(1, 1),
        )
    )


# ──────────────────────────────────────────────
#  Helpers
# ──────────────────────────────────────────────

def show_welcome() -> None:
    console.print()
    console.print(
        Panel(
            Align.center(
                Text.assemble(
                    ("  rtree  ", "bold white on #1e40af"),
                    "\n\n",
                    ("A beautiful, icon-rich alternative to the classic ", "dim white"),
                    ("tree", "bold cyan"),
                    (" command.", "dim white"),
                    "\n",
                    ("Powered by ", "dim white"),
                    ("Rich", "bold magenta"),
                    (" · Nerd Fonts · Python", "dim white"),
                )
            ),
            title="[bold cyan]Welcome to the rtree setup wizard[/]",
            border_style="bright_blue",
            box=HEAVY,
            padding=(1, 4),
        )
    )
    console.print(
        f"[dim]This wizard has [bold white]{_TOTAL_STEPS}[/] steps and will only take a moment.[/]"
    )


def _ask(prompt: str, **kwargs):
    """Thin wrapper around questionary.confirm that handles Ctrl+C gracefully."""
    try:
        return questionary.confirm(prompt, **kwargs).ask()
    except KeyboardInterrupt:
        console.print("\n[dim]Setup cancelled.[/]")
        sys.exit(0)


# ──────────────────────────────────────────────
#  Main entry point
# ──────────────────────────────────────────────

def main() -> None:
    show_welcome()

    # ── Step 1: verify icons ──────────────────────────────────────────────
    _step("Verifying icon rendering")
    console.print(
        "[dim]Below is every icon rtree can display. "
        "They should all look like small glyphs — not boxes or question marks.[/]\n"
    )
    show_all_icons()

    works = _ask("Do all these icons look correct?")
    if works is None:
        return  # questionary returned None (non-TTY)

    if not works:
        show_font_fix_instructions()
        console.print(
            "[dim]Re-run [bold]rtree --onboard[/] after installing the font "
            "to confirm everything looks right.[/]"
        )

    # ── Step 2: optional alias ────────────────────────────────────────────
    _step("Setting up an alias (optional)")
    console.print(
        "[dim]You can alias [bold green]tree[/] → [bold green]rtree[/] so existing "
        "habits and scripts keep working seamlessly.[/]\n"
    )

    wants_alias = _ask("Would you like instructions for aliasing tree → rtree?", default=False)
    if wants_alias is None:
        return

    if wants_alias:
        show_alias_instructions()
    else:
        console.print("[dim]Skipped. Run [bold]rtree --onboard[/] again any time.[/]")

    # ── Step 3: feature overview ──────────────────────────────────────────
    _step("Exploring features")
    show_feature_showcase()

    # ── Done ──────────────────────────────────────────────────────────────
    console.print()
    console.print(Rule(style="dim cyan"))
    console.print(
        Align.center(
            Text.assemble(
                ("🎉  ", "bold"),
                ("Setup complete! ", "bold green"),
                ("Run ", "white"),
                ("rtree", "bold cyan"),
                (" in any directory to get started.\n", "white"),
                ("📚  Docs: ", "dim"),
                ("https://wasi-master.github.io/rich-tree", "link https://wasi-master.github.io/rich-tree cyan"),
                ("  ·  ", "dim"),
                ("🐛  Issues: ", "dim"),
                ("https://github.com/wasi-master/rich-tree/issues", "link https://github.com/wasi-master/rich-tree/issues cyan"),
            )
        )
    )
    console.print()


if __name__ == "__main__":
    main()
