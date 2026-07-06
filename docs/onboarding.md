# Onboarding Wizard

The **rtree onboarding wizard** is an interactive, step-by-step setup guide built right into the CLI. It helps you verify your terminal environment and configure optional convenience features.

---

## Launching the Wizard

```sh
rtree --onboard
```

The wizard guides you through **3 steps** and takes less than a minute to complete.

---

## Step 1 — Verifying Icon Rendering

The wizard displays **all icons** that rich-tree uses in a compact grid. You can immediately see whether your terminal is rendering them correctly.

**What you should see:**

A dense grid of small, distinct glyphs — file icons, folder icons, language logos, etc. Each glyph should be a clear symbol, not a box (`□`) or question mark (`?`).

**If icons look correct:**

Answer `y` (Yes) when asked. The wizard moves on to the next step.

**If icons appear as boxes or question marks:**

Answer `n` (No). The wizard displays detailed instructions for installing and configuring a Nerd Font:

1. Download a Nerd Font from [nerdfonts.com/font-downloads](https://www.nerdfonts.com/font-downloads)  
   *Recommended: JetBrainsMono, CaskaydiaCove, or FiraCode Nerd Font*
2. Install the font on your system
3. In your terminal settings, change the font to the installed Nerd Font
4. Re-run `rtree --onboard` to verify

You can also patch your own existing font using the [Nerd Fonts patcher](https://github.com/ryanoasis/nerd-fonts#font-patcher).

---

## Step 2 — Setting Up an Alias (Optional)

This step lets you alias the classic `tree` command to `rtree`, so existing habits and scripts that use `tree` automatically benefit from rich-tree's features.

When prompted, answer:
- `y` — to see shell-specific alias instructions
- `n` — to skip (you can always re-run `rtree --onboard` later)

**Shell-specific instructions provided:**

### Bash / Zsh

```bash
# Add to ~/.bashrc or ~/.zshrc
alias tree="rtree"

# Reload your shell
source ~/.bashrc   # or ~/.zshrc
```

### PowerShell (pwsh)

```powershell
# Add to your PowerShell profile ($PROFILE)
New-Alias tree rtree
```

### Windows CMD

```bat
REM Create C:\Windows\System32\tree.bat with:
@echo off
call rtree %*
```

### Fish

```fish
alias tree="rtree"
funcsave tree
```

### Other Shells

For shells not covered above, the wizard suggests searching online for "how to add aliases to [your shell]".

---

## Step 3 — Feature Showcase

The wizard displays a formatted table of all available flags with short descriptions and usage examples:

| Flag | Description | Example |
|------|-------------|---------|
| `--show-size / -ss` | Show file sizes | `rtree -ss` |
| `--show-modified / -sm` | Show last-modified timestamps | `rtree -sm` |
| `--show-created / -sc` | Show creation timestamps | `rtree -sc` |
| `--show-accessed / -sa` | Show last-accessed timestamps | `rtree -sa` |
| `--show-git / -sg` | Overlay git status on each file | `rtree -sg` |
| `--depth / -d` | Limit tree depth | `rtree -d 3` |
| `--exclude / -e` | Exclude folders (comma-separated) | `rtree -e dist,build` |
| `--ignore-dot / -id` | Hide dotfiles | `rtree -id` |
| `--all / -a` | Show hidden & git-ignored files | `rtree -a` |
| `--export-html / -o` | Save tree as an HTML file | `rtree -o out.html` |

---

## Completing the Wizard

After step 3, the wizard displays a completion message with links to:

- 📚 **Documentation:** https://wasi-master.github.io/rich-tree  
- 🐛 **Issue Tracker:** https://github.com/wasi-master/rich-tree/issues

---

## Re-running the Wizard

You can re-run the wizard at any time:

```sh
rtree --onboard
```

This is useful after:
- Installing a new Nerd Font to verify icons now render correctly
- Switching to a new terminal emulator
- Setting up rich-tree on a new machine

---

## Keyboard Shortcuts During the Wizard

| Key | Action |
|-----|--------|
| `y` / `Enter` | Confirm / Yes |
| `n` | No / Skip |
| `Ctrl+C` | Cancel the wizard and exit |
