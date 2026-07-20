# Changelog

All notable changes to **rich-tree** are documented here.

This project follows [Semantic Versioning](https://semver.org/).

## [1.1.0] — 2026-07-20

### Added

- 📁 **Compact Folders (Squashing)**: Automatically squash single nested subdirectories into a single line (like VS Code compact folders). Enabled by default.
- 🎛️ **`--compact` / `--no-compact` (`--squash` / `--no-squash`, `-c`)**: Flags to toggle folder compacting on or off.

---

## [1.0.0] — Initial Release

### Added

- 🌳 **Beautiful directory tree** rendered with [Rich](https://github.com/Textualize/rich)
- 🎨 **Nerd Font icons** for 220+ file extensions and 40+ named files/folders
- 🎨 **Per-type colors** — each file type has a visually distinct, brand-accurate color
- 🔗 **Clickable file links** via OSC 8 hyperlinks (supported terminals: iTerm2, Kitty, Wezterm, etc.)
- 📊 **File size display** (`--show-size` / `-ss`)
- 🕐 **File timestamp display**:
  - Creation time (`--show-created` / `-sc`)
  - Modification time (`--show-modified` / `-sm`)
  - Access time (`--show-accessed` / `-sa`)
- 🌿 **Git status overlay** (`--show-git` / `-sg`) — shows `M`, `A`, `D`, `??`, `R`, `C`, `U` status
- 🙈 **gitignore parsing** — reads `.gitignore` files hierarchically at every directory level
- 📁 **Depth control** (`--depth` / `-d`) — limit recursion depth
- 🚫 **Custom exclusions** (`--exclude` / `-e`) — comma-separated list of names to skip
- 🔸 **Dotfile hiding** (`--ignore-dot` / `-id`) — hide files and folders starting with `.`
- 👁️ **Show all** (`--all` / `-a`) — override all filtering
- 🚫 **Disable gitignore** (`--no-gitignore`) — bypass `.gitignore` rules
- 🌐 **HTML export** (`--export-html` / `-o`) — save fully styled tree as HTML
- 📐 **Width control** (`--width` / `-w`) — fit output to N characters
- 🔤 **Soft wrap** (`--soft`) — enable soft text wrapping
- 🧙 **Interactive onboarding wizard** (`--onboard`):
  - Icon rendering verification
  - Shell-specific alias setup instructions (bash, zsh, fish, PowerShell, CMD)
  - Feature showcase table
- 🖥️ **Cross-platform** — works on Windows, macOS, and Linux
- 🪟 **Windows hidden file detection** — uses Win32 API (`FILE_ATTRIBUTE_HIDDEN`)
- 📋 **Sorted output** — directories first, then files, each group sorted case-insensitively
- ⚡ **Live status** — progress indicator while the tree is being built
- 🛡️ **Graceful error handling** — permission errors and missing stats are silently skipped
- 🖨️ **Rich-formatted help** — `--help` output rendered with colors and formatting

---

## Roadmap

Planned for future releases:

- [ ] Configuration file support (`~/.config/rtree/config.toml`)
- [ ] Per-project configuration (`.rtree.toml`)
- [ ] Auto-run onboarding wizard on first use
- [ ] GitHub Pages documentation site with live demo
- [ ] Automated test suite

---

*See [GitHub Issues](https://github.com/wasi-master/rich-tree/issues) for the full list of planned features and known bugs.*
