# Features

rich-tree is packed with features that go far beyond the classic `tree` command. This page explains each feature in detail.

---

## 🗂️ Icons

Every file and directory is displayed with a visually distinct **Nerd Font icon** and matching **color**. Icons are selected based on:

1. **Exact filename match** (e.g., `README.md` → book icon, `Dockerfile` → Docker whale)
2. **File extension match** (e.g., `.py` → Python snake, `.rs` → Rust gear)
3. **Folder name match** (e.g., `src` → source icon, `docs` → document icon)
4. **Fallback** — a generic file or folder icon

Over **220 file type extensions** and **40+ named folders and files** are covered.  
See the full [Icon System reference](icons.md).

---

## 🎨 Colors

Every icon has an associated color chosen to match the language or tool it represents:

| Color | Examples |
|-------|---------|
| Python blue `#4b8bbe` | `.py`, `.pyc` |
| JavaScript yellow `#e7d535` | `.js`, `.mjs` |
| TypeScript blue `#3a73be` | `.ts`, `.tsx` |
| Rust orange `#e64619` | `.rs`, `.rlib` |
| HTML orange `#f06529` | `.htm`, `.html`, `.xhtml` |
| CSS blue `#375ee2` | `.css` |
| Go cyan `#27a3ca` | `.go` |
| Markdown blue `#50a4f2` | `.md`, `.markdown` |

Dimmed colors are used for hidden, gitignored, or `__dunder__` directories to visually differentiate them from regular content.

---

## 🔗 Clickable File Links

File names in the tree are **clickable hyperlinks** in terminals that support OSC 8 hyperlinks (e.g., iTerm2, Kitty, Wezterm, GNOME Terminal, Windows Terminal).

Clicking a filename opens the file in your system's default application.

The root directory label is also a clickable link to the directory itself.

---

## 📊 File Metadata

You can display extra information alongside each file with these flags:

### File Size (`--show-size` / `-ss`)

Shows human-readable file size in decimal format:

```
main.py (12.4 kB)
data.csv (1.2 MB)
```

Sizes are colored **blue** for regular files, and dimmed for hidden/ignored files.

### Creation Time (`--show-created` / `-sc`)

Shows when the file was created:

```
main.py (created: 2024-01-15 09:23:41)
```

Colored **cyan**.

### Modification Time (`--show-modified` / `-sm`)

Shows when the file was last modified:

```
main.py (modified: 2024-06-30 14:55:12)
```

Colored **green**.

### Access Time (`--show-accessed` / `-sa`)

Shows when the file was last accessed:

```
main.py (accessed: 2024-07-01 08:10:44)
```

Colored **yellow**.

### Combining Metadata Flags

All metadata flags can be combined:

```sh
rtree -ss -sc -sm -sa
```

Output:
```
main.py (12.4 kB, created: 2024-01-15 09:23:41, modified: 2024-06-30 14:55:12, accessed: 2024-07-01 08:10:44)
```

Timestamps use the format `YYYY-MM-DD HH:MM:SS` in local time.

---

## 🌿 Git Status Overlay

Run `rtree --show-git` (or `-sg`) to overlay **git status** on every file in the tree. This is incredibly useful for quickly seeing what's changed in a project.

```sh
rtree -sg
```

Output example:
```
📂 project
├── 🐍 main.py [M]      ← modified
├── 📄 new_feature.py [A]  ← staged/added
├── 📄 old.py [D]       ← deleted
└── 📄 scratch.py [??]  ← untracked
```

**Status code colors:**

| Status | Code | Color | Description |
|--------|------|-------|-------------|
| Modified | `M` | Yellow | File changed but not staged, or staged changes |
| Added | `A` | Green | New file staged for commit |
| Deleted | `D` | Red | File deleted |
| Untracked | `??` | Magenta | New file, not tracked by git |
| Renamed | `R` | Green | File renamed |
| Copied | `C` | Green | File copied |
| Unmerged | `U` | Red | Merge conflict |

**Requirements:**
- `git` must be installed and on your `PATH`
- The target directory must be inside a git repository

If git is not available or the directory is not a git repo, the flag is silently ignored (no error is shown).

**How it works:**

rich-tree runs `git status --porcelain -z` from the git repository root and builds a mapping of file paths to status codes. Renamed/copied files (which have two paths in the output) are correctly handled.

---

## 🙈 Smart Filtering

### gitignore Parsing

By default, rich-tree reads `.gitignore` files at every level of the tree and hides matched files — just like git itself does.

- Multiple `.gitignore` files (at different directory levels) are stacked and applied hierarchically.
- Supports negation patterns (`!`)
- Supports directory-only patterns (trailing `/`)
- Supports root-anchored patterns (leading `/`)
- Supports glob wildcards (`*`, `?`, `**`)

To disable gitignore filtering:

```sh
rtree --no-gitignore
```

### Dotfile Hiding

By default, dotfiles (files/folders starting with `.`) that are **not** in the "important dotfiles" whitelist are hidden. Use `--ignore-dot` to also hide the whitelisted ones, or `--all` to show everything.

**Important dotfiles that are never hidden by default:**

| File | Purpose |
|------|---------|
| `.gitignore` | Git ignore rules |
| `.gitattributes` | Git attributes |
| `.editorconfig` | Editor configuration |
| `.env` | Environment variables |
| `.env.example` | Environment variable template |
| `.env.local` | Local environment overrides |
| `.env.development` | Development environment |
| `.env.production` | Production environment |
| `.npmrc` | npm configuration |
| `.babelrc` | Babel configuration |
| `.eslintrc` | ESLint configuration |
| `.eslintrc.json` | ESLint configuration (JSON) |
| `.prettierrc` | Prettier configuration |
| `.vscodeignore` | VS Code extension ignore |

### Custom Exclusions (`--exclude` / `-e`)

Exclude specific folder or file names by providing a comma-separated list. The default exclusion list is `venv,node_modules,.git,.history`.

```sh
rtree -e dist,build,__pycache__
```

> Note: Specifying `--exclude` replaces the entire default list. To keep defaults and add more, include them explicitly:
> ```sh
> rtree -e venv,node_modules,.git,.history,dist,build
> ```

### Show Everything (`--all` / `-a`)

Override all filtering (hidden files, gitignore rules) and show every file:

```sh
rtree --all
rtree -a
```

---

## 📁 Depth Control

Limit how many levels deep the tree recurses with `--depth` / `-d`:

```sh
rtree -d 1      # only immediate children
rtree -d 2      # two levels deep
rtree -d 3      # three levels deep
```

A depth of `-1` (default) means unlimited recursion.

---

## 🌐 HTML Export

Save the tree as a self-contained HTML file with all colors and styles preserved:

```sh
rtree -o output.html
rtree --export-html /tmp/project-snapshot.html
```

The HTML file can be:
- Opened in any web browser
- Shared with teammates who don't have rich-tree installed
- Embedded in documentation or reports

---

## 📐 Output Formatting

### Width Control (`--width` / `-w`)

Force the output to fit within a specific number of characters:

```sh
rtree -w 100
```

### Soft Wrap (`--soft`)

Enable soft (word-boundary) text wrapping instead of truncating at the terminal edge:

```sh
rtree --soft
```

---

## 🧙 Onboarding Wizard

Run the interactive setup wizard for guided configuration:

```sh
rtree --onboard
```

The wizard covers:
1. **Icon verification** — displays all icons to check Nerd Font rendering
2. **Alias setup** — provides shell-specific instructions to alias `tree` → `rtree`
3. **Feature showcase** — an overview of all available flags

See the full [Onboarding Wizard guide](onboarding.md).

---

## 🗄️ Sorting

Directories always appear before files in each level. Within each group (directories and files separately), entries are sorted case-insensitively by name.

---

## 🛡️ Error Handling

- Directories with **permission errors** are silently skipped (no crash).
- Files that can't be `stat()`-ed for metadata are skipped gracefully.
- `git status` errors (no git, not a repo) are silently ignored.
- Pretty Rich tracebacks are installed for any unexpected errors.

---

## ⚡ Performance

- rich-tree uses `os.scandir()` for fast directory iteration.
- A **live status indicator** (`Preparing…` / `Processing [file]`) is shown while the tree is being built.
- Git status is fetched once per run with a single `git status --porcelain -z` call.
- `.gitignore` files are parsed lazily as directories are traversed.
