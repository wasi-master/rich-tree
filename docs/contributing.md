# Contributing

Thank you for your interest in contributing to **rich-tree**! Contributions of all kinds are welcome — bug reports, feature requests, icon additions, documentation improvements, and code changes.

---

## 🐛 Reporting Bugs

Please open a [GitHub Issue](https://github.com/wasi-master/rich-tree/issues) and include:

- Your operating system and terminal emulator
- Python version (`python --version`)
- rich-tree version (`rtree --version`)
- Steps to reproduce the issue
- Expected behavior vs. actual behavior
- Relevant error messages or screenshots

---

## 💡 Requesting Features

Open a [GitHub Issue](https://github.com/wasi-master/rich-tree/issues) with the label `enhancement`. Describe:

- The problem you're trying to solve
- Your proposed solution (if you have one)
- Any alternatives you've considered

---

## 🛠️ Development Setup

### 1. Fork & Clone

```sh
# Fork on GitHub, then:
git clone https://github.com/YOUR_USERNAME/rich-tree.git
cd rich-tree
```

### 2. Create a Virtual Environment

```sh
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
pip install -e .   # install rtree in editable mode
```

### 4. Verify Installation

```sh
rtree --version
rtree --help
rtree .
```

---

## 📁 Project Structure

```
rich-tree/
├── rtree/               # Main package
│   ├── __init__.py      # Version definition
│   ├── __main__.py      # CLI entry point (click commands)
│   ├── core.py          # Core tree-walking and rendering logic
│   ├── _icons.py        # Icon and color definitions
│   └── onboarding.py    # Interactive onboarding wizard
├── docs/                # Documentation
├── demo/                # Demo assets
├── setup.cfg            # Package metadata and entry points
├── setup.py             # Minimal setup.py shim
├── requirements.txt     # Development/runtime dependencies
├── README.md            # Project README (published to PyPI)
└── LICENSE              # MIT License
```

### Key Modules

| Module | Responsibility |
|--------|---------------|
| `__main__.py` | CLI definition via `click`. Parses flags, constructs `Options`, calls `walk_directory`. |
| `core.py` | All tree-building logic: directory scanning, icon/color resolution, gitignore parsing, git status fetching, metadata formatting. |
| `_icons.py` | Pure data — dictionaries mapping file extensions, named files, and folder names to icon glyphs and colors. |
| `onboarding.py` | Interactive wizard using `questionary` and `rich` for font verification, alias instructions, and feature showcase. |

---

## 🎨 Adding Icons

The most common contribution is adding icons for new file types or folders. Edit [`rtree/_icons.py`](../rtree/_icons.py).

### Adding a File Extension Icon

Add an entry to the `icons` dict:

```python
icons = {
    # ...existing entries...
    "yourext": {"icon": "NERD_FONT_GLYPH", "color": "#hexcolor"},
}
```

### Adding a Named File Icon

Add an entry to the `named_icons` dict (use the lowercase filename):

```python
named_icons = {
    # ...existing entries...
    "yourfile.cfg": {"icon": "NERD_FONT_GLYPH", "color": "#hexcolor"},
}
```

### Adding a Folder Icon

Add an entry to the `folder_icons` dict (use the lowercase folder name):

```python
folder_icons = {
    # ...existing entries...
    "myfolder": {"icon": "NERD_FONT_GLYPH", "color": "#hexcolor"},
}
```

### Finding Nerd Font Glyphs

Browse the full icon collection at [nerdfonts.com/cheat-sheet](https://www.nerdfonts.com/cheat-sheet). Copy the glyph character directly.

You can also search by name using the VS Code extension **Nerd Font Symbols**.

### Icon Color Guidelines

- Use the **official brand color** of the language/tool where available.
- Use `#hex` format for custom colors.
- Named Rich colors (`"blue"`, `"magenta"`, etc.) are acceptable for simple colors.
- Avoid colors that are too similar to neighboring icon colors (contrast matters!).

---

## 🔧 Making Code Changes

### Code Style

- Follow existing code style (no external formatter configured — just be consistent).
- Add type annotations to new functions where practical.
- Keep functions focused — prefer small, single-purpose functions.

### Adding a New CLI Flag

1. Add the `@click.option(...)` decorator to `cli()` in `__main__.py`.
2. Add the corresponding parameter to the `cli()` function signature.
3. Pass it to `Options(...)`.
4. Use `getattr(options, "your_flag", default)` in `core.py` to read the option safely.

### Testing Changes

Currently, rich-tree does not have an automated test suite. Manual testing:

```sh
# Run against the project itself
rtree .

# Test specific flags
rtree -ss -sm -sg -d 2 .

# Test onboarding
rtree --onboard

# Test HTML export
rtree -o /tmp/test.html && open /tmp/test.html
```

---

## 📤 Submitting a Pull Request

1. Create a feature branch: `git checkout -b feat/my-feature`
2. Make your changes with clear, descriptive commit messages.
3. Verify everything works manually.
4. Push to your fork: `git push origin feat/my-feature`
5. Open a Pull Request on GitHub against the `main` branch.
6. Describe your changes in the PR description.

---

## 📋 Code of Conduct

Be respectful and constructive. See [CODE_OF_CONDUCT.md](https://github.com/wasi-master/rich-tree/blob/main/CODE_OF_CONDUCT.md) for details.

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the [MIT License](../LICENSE).
