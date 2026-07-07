# Icon System

rich-tree uses [Nerd Fonts](https://www.nerdfonts.com/) to display beautiful icons next to every file and folder in the tree. This page documents all supported icons and how the icon selection system works.

---

## How Icon Selection Works

Icons are resolved in the following priority order:

1. **Named file match** — The filename (lowercased) is looked up in the named icons table. This covers special files like `README.md`, `Dockerfile`, `package.json`, etc.
2. **Extension match** — If no named match is found, the file extension (lowercased, after the last `.`) is looked up in the extension icons table.
3. **Fallback** — If neither match, a generic file icon is used.

For **directories**, the directory name (lowercased) is looked up in the folder icons table. If not found, the default folder icon is used.

---

## Default Icons

| Type | Icon | Color |
|------|------|-------|
| Default file | `nf-fa-file` | `#50a4f2` (blue) |
| Default folder | `nf-fa-folder` | `#f9d64d` (yellow) |

---

## Named Folder Icons

These folder names get a special icon instead of the generic folder icon:

| Folder Name | Description |
|-------------|-------------|
| `.github` | GitHub Actions / workflows |
| `.config` / `config` | Configuration |
| `build` | Build output |
| `dist` | Distribution output |
| `media` / `image` / `images` / `img` | Images and media |
| `asset` / `assets` | Project assets |
| `.vscode` / `vscode` | VS Code settings |
| `test` / `tests` / `__tests__` | Test suites |
| `src` / `source` / `sources` | Source code |
| `lib` / `libs` | Libraries |
| `doc` / `docs` | Documentation |
| `bin` / `scripts` | Executables and scripts |
| `.git` / `git` | Git repository data |
| `public` | Public web assets |
| `temp` / `tmp` | Temporary files |

---

## Named File Icons

These exact filenames (case-insensitive) get a special icon:

| Filename | Icon type | Description |
|----------|-----------|-------------|
| `LICENSE` / `LICENCE` | License | Open source license |
| `README` / `README.md` | Book | Documentation |
| `CONTRIBUTING` / `CONTRIBUTING.md` | Handshake | Contributing guide |
| `CODE_OF_CONDUCT` / `CODE_OF_CONDUCT.md` | Heart | Code of conduct |
| `yarn.lock` | Yarn | Yarn lockfile |
| `package.json` | Node.js | npm package manifest |
| `package-lock.json` | Node.js | npm lockfile |
| `requirements.txt` | Python | Python dependencies |
| `Pipfile` / `Pipfile.lock` | Python | Pipenv files |
| `.gitignore` | Git | Git ignore rules |
| `.gitattributes` | Git | Git attributes |
| `Dockerfile` / `.dockerfile` | Docker | Docker image definition |
| `docker-compose.yml` / `docker-compose.yaml` | Docker | Docker Compose config |
| `.dockerignore` | Docker | Docker ignore rules |
| `.vscodeignore` | VS Code | VS Code extension ignore |
| `tasks.json` | VS Code | VS Code tasks |
| `.htaccess` | Apache | Apache config |
| `webpack.js` | Webpack | Webpack bundler config |
| `karma.conf.js` | Test | Karma test runner |
| `gruntfile.js` | Grunt | Grunt build tool |
| `gulpfile.js` | Gulp | Gulp build tool |
| `brunch-config.js` | Brunch | Brunch build tool |
| `eslintrc.js` | ESLint | ESLint config |
| `bower.json` | Bower | Bower package manager |
| `.env` / `.env.*` | Env | Environment variables |
| `go.mod` / `go.sum` | Go | Go module files |
| `Cargo.toml` | Rust | Rust package manifest |
| `pyproject.toml` | Python | Python project config |
| `.editorconfig` | Editor | Editor configuration |
| `AndroidManifest.xml` | Android | Android app manifest |
| `.gemfile` | Ruby | Gemfile |
| `nuget.config` | NuGet | NuGet configuration |
| `.npmrc` | npm | npm config |
| `.babelrc` | Babel | Babel config |
| `.prettierrc` | Prettier | Prettier config |

---

## Extension Icons by Category

### Web

| Extension | Language/Type |
|-----------|--------------|
| `.html`, `.htm`, `.xhtml` | HTML |
| `.css` | CSS |
| `.scss`, `.sass` | Sass/SCSS |
| `.less` | Less |
| `.styl` | Stylus |
| `.svg` | SVG |
| `.js`, `.mjs` | JavaScript |
| `.jsx` | JSX (React) |
| `.ts` | TypeScript |
| `.tsx` | TSX (React + TypeScript) |
| `.vue` | Vue.js |
| `.elm` | Elm |
| `.ejs` | EJS templates |
| `.pug` | Pug templates |
| `.haml` | HAML templates |
| `.jade` | Jade templates |
| `.hbs`, `.mustache` | Handlebars / Mustache |
| `.twig` | Twig templates |

### Python

| Extension | Description |
|-----------|-------------|
| `.py` | Python source |
| `.pyc` | Python bytecode |
| `.pyo` | Python optimized bytecode |
| `.pyd` | Python extension module |
| `.ipynb` | Jupyter notebook |

### Systems / Compiled

| Extension | Language |
|-----------|---------|
| `.c`, `.cp` | C |
| `.cpp`, `.cxx`, `.cc` | C++ |
| `.h`, `.hpp`, `.hxx` | C/C++ headers |
| `.cs` | C# |
| `.java` | Java |
| `.go` | Go |
| `.rs`, `.rlib` | Rust |
| `.swift` | Swift |
| `.d` | D |
| `.hs`, `.lhs` | Haskell |
| `.ml`, `.mli` | OCaml |
| `.scala` | Scala |
| `.dart` | Dart / Flutter |
| `.kt`, `.kts` | Kotlin |
| `.lua` | Lua |
| `.r` | R |
| `.jl` | Julia |

### Scripting / Shell

| Extension | Shell |
|-----------|-------|
| `.sh` | Generic shell |
| `.bash` | Bash |
| `.zsh` | Zsh |
| `.fish` | Fish |
| `.ksh` | Korn shell |
| `.csh` | C shell |
| `.awk` | AWK |
| `.ps1` | PowerShell |
| `.bat` | Windows Batch |
| `.wsf` | Windows Script File |

### Functional / Lisp

| Extension | Language |
|-----------|---------|
| `.clj`, `.cljc`, `.cljs`, `.edn` | Clojure |
| `.erl`, `.hrl` | Erlang |
| `.ex`, `.exs`, `.eex` | Elixir |
| `.fs`, `.fsi`, `.fsx`, `.fsscript` | F# |
| `.pl`, `.pm`, `.t` | Perl |
| `.rb` | Ruby |
| `.coffee` | CoffeeScript |
| `.php` | PHP |
| `.vim` | Vim script |

### Data / Config

| Extension | Type |
|-----------|------|
| `.json`, `.jsonc` | JSON |
| `.yml`, `.yaml` | YAML |
| `.xml`, `.xul` | XML |
| `.toml` | TOML |
| `.ini`, `.cfg`, `.conf` | Configuration |
| `.csv`, `.tsv` | Delimited data |
| `.rss` | RSS feed |
| `.vcf` | vCard |

### Database

| Extension | Type |
|-----------|------|
| `.sql` | SQL |
| `.sqlite` | SQLite database |
| `.db`, `.dbf` | Database |
| `.mdb` | Microsoft Access |
| `.sav` | SPSS / game save |
| `.dump` | Database dump |

### Images

| Extension | Format |
|-----------|--------|
| `.jpg`, `.jpeg` | JPEG |
| `.png` | PNG |
| `.gif` | GIF |
| `.bmp` | BMP |
| `.ico` | Icon |
| `.svg` | SVG |
| `.tiff` | TIFF |
| `.heic` | HEIC (Apple) |
| `.webp` | WebP |
| `.avif` | AVIF |

### Audio

| Extension | Format |
|-----------|--------|
| `.mp3`, `.mp2`, `.mpa` | MP3 |
| `.wav` | WAV |
| `.ogg` | Ogg Vorbis |
| `.flac` | FLAC |
| `.aiff` | AIFF |
| `.aac`, `.m4a` | AAC/M4A |
| `.opus` | Opus |
| `.wma` | Windows Media Audio |
| `.mid`, `.midi` | MIDI |

### Video

| Extension | Format |
|-----------|--------|
| `.mp4`, `.m4v` | MPEG-4 |
| `.mkv` | Matroska |
| `.avi` | AVI |
| `.mov` | QuickTime |
| `.wmv` | Windows Media Video |
| `.flv` | Flash Video |
| `.webm` | WebM |
| `.ogv`, `.vob` | Other formats |
| `.mpg`, `.mpeg` | MPEG |
| `.3gp` | 3GP |
| `.hevc`, `.gifv` | Modern formats |

### Documents

| Extension | Format |
|-----------|--------|
| `.pdf` | PDF |
| `.doc`, `.docx` | Microsoft Word |
| `.xls`, `.xlsx` | Microsoft Excel |
| `.ppt`, `.pptx` | Microsoft PowerPoint |
| `.tex` | LaTeX |
| `.md`, `.markdown`, `.rmd` | Markdown |

### Archives / Packages

| Extension | Format |
|-----------|--------|
| `.zip` | ZIP |
| `.tar` | TAR |
| `.gz` | GZIP |
| `.rar` | RAR |
| `.7z` | 7-Zip |
| `.z` | Compress |
| `.deb` | Debian package |
| `.pkg` | macOS package |
| `.dmg` | macOS disk image |
| `.iso`, `.vcd` | Disk images |
| `.cab` | Windows cabinet |

### Executables / Binaries

| Extension | Type |
|-----------|------|
| `.exe`, `.com` | Windows executable |
| `.msi` | Windows installer |
| `.elf` | Linux ELF binary |
| `.app` | macOS app bundle |
| `.apk` | Android APK |
| `.dll` | Windows DLL |
| `.so` | Linux shared library |
| `.o`, `.ko` | Object files |
| `.sys` | System file |
| `.bin`, `.dat` | Binary data |

### 3D / Design

| Extension | Type |
|-----------|------|
| `.blend` | Blender |
| `.obj`, `.fbx`, `.stl` | 3D models |
| `.c4d` | Cinema 4D |
| `.3ds` | 3DS Max |
| `.max` | 3DS Max scene |
| `.mesh` | Mesh data |
| `.ai` | Adobe Illustrator |
| `.psd`, `.psb` | Adobe Photoshop |

### Other

| Extension | Type |
|-----------|------|
| `.log` | Log files |
| `.lock` | Lockfiles |
| `.diff` | Diff/patch files |
| `.map` | Source maps |
| `.eml`, `.email`, `.emlx`, `.msg` | Email files |
| `.oft`, `.ost`, `.pst` | Outlook files |
| `.cer` | Certificate |
| `.cur` | Cursor file |
| `.ink` | Ink file |
| `.fnt`, `.fon`, `.ttf`, `.otf`, `.woff`, `.woff2` | Font files |
| `.bak` | Backup files |
| `.sln`, `.suo` | Visual Studio solution |
| `.pub` | Publisher / public key |
| `.pp` | Puppet manifest |
| `.xul` | XUL |
| `.gradle` | Gradle build |

---

## Visual Styling Rules

- **Regular files** — icon in its designated color, name in default terminal color
- **Hidden files / gitignored files** — icon and name rendered in `dim` style
- **`__dunder__` directories** — rendered in `dim` style
- **Important dotfiles** (whitelisted) — always rendered normally, never dimmed

---

## Adding Custom Icons

The icon data lives in [`rtree/_icons.py`](https://github.com/wasi-master/rich-tree/blob/main/rtree/_icons.py). You can fork the project and add icons to:

- `named_icons` — for exact filename matches
- `icons` — for file extension matches
- `folder_icons` — for directory name matches

Each entry follows the format:

```python
"extension_or_name": {"icon": "NERD_FONT_GLYPH", "color": "#hexcolor or rich_color_name"}
```

See [Contributing](contributing.md) for instructions on submitting icon additions upstream.
