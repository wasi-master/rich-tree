# CLI Reference

## Synopsis

```
rtree [OPTIONS] [DIRECTORY]
```

`DIRECTORY` defaults to `.` (the current directory) if not specified.

---

## Positional Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `DIRECTORY` | `.` | Path to the directory to visualize. Must be an existing directory. |

**Examples:**

```sh
rtree                         # current directory
rtree /home/user/projects     # absolute path
rtree ../sibling-dir          # relative path
```

---

## Options

### `--version` / `-v`

Print the version number and exit.

```sh
rtree --version
# Output: 0.1.0
```

---

### `--onboard`

Launch the **interactive onboarding wizard**. The wizard:
1. Displays all icons to verify Nerd Font rendering.
2. Optionally shows shell-specific alias setup instructions.
3. Showcases all available CLI flags.

```sh
rtree --onboard
```

See the full [Onboarding Wizard guide](onboarding.md).

---

### `--depth` / `-d`

Limit the recursion depth of the tree.

```
-d INTEGER   (default: -1, meaning unlimited)
```

| Value | Behavior |
|-------|----------|
| `-1` | Unlimited depth (default) |
| `0` | Show only the root (no children) |
| `1` | Show immediate children only |
| `N` | Show N levels deep |

**Examples:**

```sh
rtree -d 2          # two levels deep
rtree --depth 1     # only immediate children
```

---

### `--exclude` / `-e`

Comma-separated list of file and folder **names** to exclude from the tree.

```
-e TEXT   (default: "venv,node_modules,.git,.history")
```

> **Note:** The default exclusion list already hides common noise folders (`venv`, `node_modules`, `.git`, `.history`). Specifying `--exclude` **replaces** the entire default list.

**Examples:**

```sh
rtree -e dist,build                    # exclude dist and build
rtree --exclude venv,node_modules,.git # same as default
rtree -e ""                            # exclude nothing (show everything)
```

---

### `--ignore-dot` / `-id`

Hide all files and directories whose names begin with a period (`.`).

> **Exception:** The following important dotfiles are **never** hidden, even with this flag:
> `.gitignore`, `.gitattributes`, `.editorconfig`, `.env`, `.env.example`,
> `.env.local`, `.env.development`, `.env.production`, `.npmrc`, `.babelrc`,
> `.eslintrc`, `.eslintrc.json`, `.prettierrc`, `.vscodeignore`

```sh
rtree --ignore-dot
rtree -id
```

---

### `--all` / `-a`

Show **all** files, including:
- Hidden files (files/directories starting with `.`)
- Files matched by `.gitignore` rules

By default, hidden and gitignored files are omitted.

```sh
rtree --all
rtree -a
```

---

### `--no-gitignore`

Disable `.gitignore` parsing entirely. All files that would normally be filtered by `.gitignore` rules will be shown.

```sh
rtree --no-gitignore
```

---

### `--show-size` / `-ss`

Display the size of each file in human-readable decimal format (e.g., `1.2 kB`, `3.4 MB`).

```sh
rtree --show-size
rtree -ss
```

Output example:
```
📂 project
├── 🐍 main.py (12.4 kB)
└── 📄 README.md (3.2 kB)
```

---

### `--show-created` / `-sc`

Display the **creation timestamp** of each file in `YYYY-MM-DD HH:MM:SS` format.

```sh
rtree --show-created
rtree -sc
```

Output example:
```
📂 project
├── 🐍 main.py (created: 2024-01-15 09:23:41)
```

> **Note:** On some Linux filesystems, creation time may not be available (it may show the inode change time instead).

---

### `--show-modified` / `-sm`

Display the **last modification timestamp** of each file.

```sh
rtree --show-modified
rtree -sm
```

---

### `--show-accessed` / `-sa`

Display the **last accessed timestamp** of each file.

```sh
rtree --show-accessed
rtree -sa
```

---

### `--show-git` / `-sg`

Overlay **git status indicators** on each file. Requires `git` to be available on your `PATH` and the directory to be inside a git repository.

```sh
rtree --show-git
rtree -sg
```

Status codes shown:

| Code | Color | Meaning |
|------|-------|---------|
| `M` | Yellow | Modified |
| `A` | Green | Added (staged) |
| `D` | Red | Deleted |
| `??` | Magenta | Untracked |
| `R` | Green | Renamed |
| `C` | Green | Copied |
| `U` | Red | Unmerged |

---

### `--export-html` / `-o`

Save the styled tree output as a self-contained **HTML file**. The HTML file preserves all colors and styles.

```
-o PATH / --export-html PATH
```

```sh
rtree -o tree.html
rtree --export-html /tmp/project-tree.html
```

Open the resulting file in any web browser to view the tree.

---

### `--width` / `-w`

Fit the output to a specific number of characters wide.

```
-w SIZE / --width SIZE   (default: terminal width)
```

```sh
rtree -w 120
rtree --width 80
```

Useful when piping to a file or for consistent output on different terminals.

---

### `--soft`

Enable **soft wrapping** of text. By default, rich hard-wraps at the terminal width. With this flag, long lines are allowed to wrap at word boundaries rather than being truncated.

```sh
rtree --soft
```

---

## Combining Options

Options can be freely combined:

```sh
# Show sizes, git status, 3 levels deep, exclude build artifacts
rtree -ss -sg -d 3 -e dist,build,__pycache__

# Show everything including hidden files with timestamps
rtree -a -sm -sc

# Export a styled HTML snapshot of the project
rtree -ss -sg -o snapshot.html
```

---

## Help

```sh
rtree --help
```

The `--help` output is rendered with Rich for an attractive, colorized display.

---

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| Non-zero | Error (e.g., permission denied, invalid path) |
