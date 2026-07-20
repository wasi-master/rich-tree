<div align="center">

# rich-tree

**A beautiful, icon-rich replacement for the classic `tree` command**

[![PyPI version](https://img.shields.io/pypi/v/rich-tree.svg?style=flat-square&color=4b8bbe)](https://pypi.org/project/rich-tree/)
[![Python versions](https://img.shields.io/pypi/pyversions/rich-tree.svg?style=flat-square)](https://pypi.org/project/rich-tree/)
[![License: MIT](https://img.shields.io/pypi/l/rich-tree.svg?style=flat-square&color=2b9f64)](LICENSE)

*Powered by [Rich](https://github.com/Textualize/rich) · [Nerd Fonts](https://www.nerdfonts.com/) · Python*

</div>

---

<div align="center">

> Open [`demo.html`](https://raw.githubusercontent.com/wasi-master/rich-tree/main/demo.html) in a browser for the best preview.

![rich-tree demo screenshot](https://raw.githubusercontent.com/wasi-master/rich-tree/refs/heads/main/screenshot.png)

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📁 **Compact folders** | Squash single nested subdirectories into a single line (enabled by default) |
| 🗂️ **220+ file type icons** | Nerd Font glyphs for every major language and tool |
| 🎨 **Per-type colors** | Brand-accurate colors for every file type |
| 🔗 **Clickable links** | Files are hyperlinks in supported terminals |
| 📊 **File metadata** | Show size, created, modified, and accessed timestamps |
| 🌿 **Git status overlay** | See modified, added, deleted, and untracked files at a glance |
| 🙈 **Smart filtering** | Reads `.gitignore`, hides dotfiles, supports custom exclusion lists |
| 📁 **Depth control** | Limit recursion to N levels |
| 🌐 **HTML export** | Save the styled tree as a shareable HTML file |
| 🧙 **Onboarding wizard** | Interactive setup guide for fonts and aliases |
| 🖥️ **Cross-platform** | Windows, macOS, and Linux |

---

## 📦 Installation

```sh
pip install rich-tree
```

> Requires **Python 3.6+** and a [Nerd Font](https://www.nerdfonts.com/) for icons to render correctly.

**With pipx (recommended for CLI tools):**

```sh
pipx install rich-tree
```

**Run without installing:**

```sh
pipx run rich-tree .
```

**Development version from GitHub:**

```sh
pip install git+https://github.com/wasi-master/rich-tree
```

---

## 🚀 Quick Start

```sh
# Display tree for the current directory
rtree

# Or use the Python module form
python -m rtree

# Show a specific directory
rtree /path/to/project
```

**Run the interactive onboarding wizard** (recommended on first install):

```sh
rtree --onboard
```

This verifies your Nerd Font is set up correctly and walks you through configuration.

---

## 📖 Usage

```
rtree [OPTIONS] [DIRECTORY]
```

`DIRECTORY` defaults to `.` (current directory) if omitted.

### Options

| Flag | Short | Description |
|------|-------|-------------|
| `--compact` / `--no-compact` | `-c` | Squash single nested subdirectories (default: on, alias: `--squash` / `--no-squash`) |
| `--show-size` | `-ss` | Show file sizes |
| `--show-created` | `-sc` | Show creation timestamps |
| `--show-modified` | `-sm` | Show modification timestamps |
| `--show-accessed` | `-sa` | Show last-accessed timestamps |
| `--show-git` | `-sg` | Overlay git status on files |
| `--depth INTEGER` | `-d` | Limit recursion depth (`-1` = unlimited) |
| `--exclude TEXT` | `-e` | Comma-separated names to exclude |
| `--ignore-dot` | `-id` | Hide dotfiles |
| `--all` | `-a` | Show hidden & gitignored files |
| `--no-gitignore` | | Disable `.gitignore` filtering |
| `--export-html PATH` | `-o` | Save output as HTML |
| `--width SIZE` | `-w` | Fit output to N characters wide |
| `--soft` | | Enable soft text wrapping |
| `--onboard` | | Run the interactive setup wizard |
| `--version` | `-v` | Print version and exit |

### Examples

```sh
# Show sizes and git status, 3 levels deep
rtree -ss -sg -d 3

# Show everything — including hidden and gitignored files
rtree --all --no-gitignore

# Exclude build artifacts
rtree -e dist,build,__pycache__

# Export a styled HTML snapshot
rtree -o project-tree.html

# Show all file metadata
rtree -ss -sc -sm -sa

# Shallow view of a project
rtree -d 1 /path/to/project
```

---

## 🧩 Nerd Font Setup

rich-tree uses **Nerd Fonts** for its icon set. You need to:

1. **Download** a Nerd Font from [nerdfonts.com/font-downloads](https://www.nerdfonts.com/font-downloads)  
   *(Recommended: JetBrainsMono Nerd Font, CaskaydiaCove, or FiraCode Nerd Font)*
2. **Install** the font on your system
3. **Set** your terminal's font to the installed Nerd Font

Verify with:

```sh
rtree --onboard
```

If icons appear as `□` or `?`, follow the instructions shown by the wizard.

---

## 🔗 Alias Setup

Replace the classic `tree` command with `rtree` for a better experience everywhere:

**Bash / Zsh** — add to `~/.bashrc` or `~/.zshrc`:

```sh
alias tree="rtree"
```

**PowerShell** — add to your [PowerShell profile](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_profiles):

```powershell
New-Alias tree rtree
```

**Windows CMD** — create `C:\Windows\System32\tree.bat`:

```bat
@echo off
call rtree %*
```

> Run `rtree --onboard` for interactive, shell-specific alias instructions.

---

## 📚 Documentation

Full documentation is available in the [`docs/`](docs/) folder and at the project website:

| Document | Description |
|----------|-------------|
| [Getting Started](docs/getting-started.md) | Installation, requirements, first run |
| [CLI Reference](docs/cli-reference.md) | Every flag and argument explained |
| [Features](docs/features.md) | Deep dive into all features |
| [Icon System](docs/icons.md) | Complete icon and color reference |
| [Onboarding Wizard](docs/onboarding.md) | Interactive setup wizard guide |
| [Configuration](docs/configuration.md) | Defaults, exclusions, gitignore |
| [Contributing](docs/contributing.md) | How to contribute |
| [Changelog](docs/changelog.md) | Release history |

---

## 🛠️ How It Works

```
rtree .
  │
  ├── Reads .gitignore at each level (hierarchical, full spec support)
  ├── Scans directories with os.scandir() (fast, lazy)
  ├── Resolves icon + color for each entry (name → extension → fallback)
  ├── Optionally fetches git status via git status --porcelain -z
  ├── Optionally reads file stat() for size/timestamps
  └── Renders the Rich Tree widget to the terminal
```

**Dependencies:**

| Package | Purpose |
|---------|---------|
| [`rich`](https://github.com/Textualize/rich) | Terminal rendering, Tree widget |
| [`click`](https://click.palletsprojects.com/) | CLI argument parsing |
| [`rich-click`](https://github.com/ewels/rich-click) | Beautiful `--help` output |
| [`questionary`](https://github.com/tmbo/questionary) | Interactive onboarding prompts |
| [`shellingham`](https://github.com/sarugaku/shellingham) | Shell detection for alias instructions |

---

## 🤝 Contributing

Contributions are welcome! The most common contribution is adding icons for new file types.

See [Contributing Guide](docs/contributing.md) for full instructions.

Quick start:

```sh
git clone https://github.com/wasi-master/rich-tree.git
cd rich-tree
pip install -e ".[dev]"
```

---

## 📄 License

[MIT](LICENSE) — © Wasi Master

---

<div align="center">

**[Documentation](docs/index.md)** · **[PyPI](https://pypi.org/project/rich-tree/)** · **[Issues](https://github.com/wasi-master/rich-tree/issues)** · **[Changelog](docs/changelog.md)**

</div>