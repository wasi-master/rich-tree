# Configuration

rich-tree is designed to work great out of the box with sensible defaults. All configuration is done through **CLI flags** — there is no configuration file at this time.

> **Note:** A configuration file feature is planned for a future release. See the [TODO](https://github.com/wasi-master/rich-tree/blob/main/TODO.md) for the roadmap.

---

## Default Behavior

When you run `rtree` with no flags, the following defaults apply:

| Setting | Default Value | Description |
|---------|--------------|-------------|
| Directory | `.` (current directory) | The directory to visualize |
| Depth | Unlimited (`-1`) | Full recursive traversal |
| Excluded names | `venv,node_modules,.git,.history` | Common noise folders |
| Dotfiles | Hidden (except important ones) | Files starting with `.` are hidden |
| gitignore | Enabled | `.gitignore` rules are respected |
| File sizes | Not shown | Use `-ss` to enable |
| Timestamps | Not shown | Use `-sc`, `-sm`, `-sa` to enable |
| Git status | Not shown | Use `-sg` to enable |
| HTML export | Disabled | Use `-o PATH` to enable |

---

## Default Exclusion List

By default, these folder/file names are excluded from the tree:

| Name | Reason |
|------|--------|
| `venv` | Python virtual environment |
| `node_modules` | Node.js dependencies |
| `.git` | Git repository internals |
| `.history` | VS Code Local History plugin |

To **override** the exclusion list entirely:

```sh
rtree --exclude dist,build,__pycache__
```

To **keep defaults and add more**, include the defaults explicitly:

```sh
rtree --exclude venv,node_modules,.git,.history,dist,build
```

To **exclude nothing** (show everything except gitignored/hidden):

```sh
rtree --exclude ""
```

---

## Important Dotfiles — Always Shown

These dotfiles are considered "important" and are **never hidden**, even when running with `--ignore-dot`:

```
.gitignore
.gitattributes
.editorconfig
.env
.env.example
.env.local
.env.development
.env.production
.npmrc
.babelrc
.eslintrc
.eslintrc.json
.prettierrc
.vscodeignore
```

These files are always shown with full color and proper icons (not dimmed), even in directories that are otherwise "hidden".

---

## gitignore Configuration

rich-tree loads `.gitignore` files at **every directory level** it traverses and applies rules hierarchically — the same way git does.

### Supported `.gitignore` Syntax

| Pattern | Example | Matches |
|---------|---------|---------|
| Literal name | `build` | Any file or directory named `build` |
| Wildcard | `*.log` | Any `.log` file anywhere |
| Directory-only | `dist/` | Only directories named `dist` |
| Root-anchored | `/output` | Only at the repository root |
| Negation | `!important.log` | Un-ignores the pattern |
| Deep wildcard | `**/temp` | `temp` at any depth |

### Disabling gitignore

```sh
rtree --no-gitignore
```

Disables all `.gitignore` parsing. All files that would normally be filtered are shown.

---

## Combining Configuration

All options compose freely:

```sh
# Full control example:
rtree \
  --depth 4 \
  --exclude venv,node_modules,.git,dist,build \
  --no-gitignore \
  --show-size \
  --show-modified \
  --show-git \
  /path/to/project
```

---

## Shell Aliases for Common Configurations

If you frequently use the same set of flags, consider setting up shell aliases for your most-used configurations:

**Bash / Zsh:**

```bash
# Add to ~/.bashrc or ~/.zshrc

# Quick tree with sizes and git status
alias rtg="rtree -ss -sg"

# Shallow tree (2 levels) with sizes
alias rt2="rtree -d 2 -ss"

# Show everything
alias rta="rtree -a --no-gitignore"
```

**Fish:**

```fish
alias rtg="rtree -ss -sg"
alias rt2="rtree -d 2 -ss"
alias rta="rtree -a --no-gitignore"
```

---

## Planned Configuration Features

The following configuration features are planned for future releases:

- [ ] **Configuration file** (`~/.config/rtree/config.toml` or `.rtreerc`) to persist default flags
- [ ] **Per-project config** (`.rtree.toml` in project root)
- [ ] **Onboarding wizard auto-detection** — run wizard on first use if no config exists

See the [TODO](https://github.com/wasi-master/rich-tree/blob/main/TODO.md) and [GitHub Issues](https://github.com/wasi-master/rich-tree/issues) for updates.
