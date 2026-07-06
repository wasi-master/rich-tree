# rich-tree Documentation

> **rich-tree** (`rtree`) — a beautiful, icon-rich replacement for the classic `tree` command, powered by [Rich](https://github.com/Textualize/rich) and [Nerd Fonts](https://www.nerdfonts.com/).

---

## 📚 Documentation Index

| Page | Description |
|------|-------------|
| [Getting Started](getting-started.md) | Installation, requirements, first run |
| [CLI Reference](cli-reference.md) | Every flag and argument explained |
| [Features](features.md) | Deep dive into all features |
| [Icon System](icons.md) | File & folder icons reference |
| [Onboarding Wizard](onboarding.md) | Interactive setup wizard guide |
| [Configuration](configuration.md) | Defaults, exclusions, gitignore |
| [Contributing](contributing.md) | How to contribute & development setup |
| [Changelog](changelog.md) | Release history |

---

## Quick Start

```sh
# Install from PyPI
pip install rich-tree

# Run in the current directory
rtree

# Run with all features
rtree -ss -sm -sg -d 3 .
```

---

## What is rich-tree?

`rtree` is a Python-based terminal utility that displays a directory tree with:

- 🎨 **Syntax-colored output** for every file type
- 🗂️ **Nerd Font icons** for hundreds of file formats and named folders
- 🔗 **Clickable file links** in terminals that support OSC hyperlinks
- 📊 **File metadata** — size, created/modified/accessed timestamps
- 🌿 **Git status overlay** — see which files are modified, added, or untracked
- 🙈 **Smart filtering** — `.gitignore` parsing, dotfile hiding, custom exclusions
- 📁 **Depth control** — limit how deep the tree recurses
- 🌐 **HTML export** — save the fully styled tree as an HTML file
- 🧙 **Interactive onboarding wizard** — verify fonts and set up aliases

---

## At a Glance

```
rtree [OPTIONS] [DIRECTORY]
```

See the [CLI Reference](cli-reference.md) for the full list of options.

---

*rich-tree is MIT licensed. Source available on [GitHub](https://github.com/wasi-master/rich-tree).*
