# Getting Started

## Requirements

| Requirement | Minimum | Notes |
|-------------|---------|-------|
| Python | 3.6+ | Tested on 3.6 – 3.10 |
| Nerd Font | Any Nerd Font v3 | Required for icons to render correctly |
| OS | Any | Windows, macOS, Linux |

> **Tip:** If you skip installing a Nerd Font, the tree still works but icons will appear as squares or question marks. Run `rtree --onboard` to get guided setup help.

---

## Installation

### From PyPI (recommended)

```sh
pip install rich-tree
```

### From GitHub (latest development version)

```sh
pip install git+https://github.com/wasi-master/rich-tree
```

### With pipx (isolated, recommended for CLI tools)

```sh
pipx install rich-tree
```

Or run it without installing at all:

```sh
pipx run rich-tree .
```

---

## First Run

Once installed, you can immediately run:

```sh
rtree
```

This displays the tree for the **current directory**.

To display a specific directory:

```sh
rtree /path/to/directory
```

Or using `python -m`:

```sh
python -m rtree /path/to/directory
```

---

## Nerd Font Setup

rich-tree uses **Nerd Fonts** for its beautiful icon set. You need to:

1. Download a Nerd Font from [nerdfonts.com/font-downloads](https://www.nerdfonts.com/font-downloads)  
   *(Recommended: JetBrainsMono Nerd Font, CaskaydiaCove, or FiraCode Nerd Font)*
2. Install the font on your system.
3. Set your terminal's font to the installed Nerd Font.

Run the onboarding wizard to check if your icons are rendering correctly:

```sh
rtree --onboard
```

If icons show as boxes or `?`, follow the instructions in the [Onboarding Wizard](onboarding.md) guide.

---

## Aliasing `tree` to `rtree`

You can alias the classic `tree` command to `rtree` so existing habits and scripts keep working.

### Bash / Zsh

Add this line to `~/.bashrc` or `~/.zshrc`:

```sh
alias tree="rtree"
```

Then reload your shell:

```sh
source ~/.bashrc   # or ~/.zshrc
```

### Fish

```fish
alias tree="rtree"
funcsave tree
```

### PowerShell

Add to your [PowerShell profile](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_profiles):

```powershell
New-Alias tree rtree
```

### Windows CMD

Create a file `tree.bat` in `C:\Windows\System32` with content:

```bat
@echo off
call rtree %*
```

> **Tip:** The interactive onboarding wizard (`rtree --onboard`) provides shell-specific alias instructions automatically.

---

## Dependencies

rich-tree depends on these Python packages (installed automatically):

| Package | Purpose |
|---------|---------|
| [`rich`](https://github.com/Textualize/rich) | Beautifully formatted terminal output, tree widget |
| [`click`](https://click.palletsprojects.com/) | CLI argument/option parsing |
| [`rich-click`](https://github.com/ewels/rich-click) | Rich-formatted `--help` output |
| [`questionary`](https://github.com/tmbo/questionary) | Interactive prompts in the onboarding wizard |
| [`shellingham`](https://github.com/sarugaku/shellingham) | Detects the active shell for alias instructions |

---

## Next Steps

- Read the [CLI Reference](cli-reference.md) to learn all available flags.
- Explore [Features](features.md) for in-depth explanations of each capability.
- Run `rtree --onboard` for a guided interactive setup.
