# System-Wide Installation Guide

This document explains the best ways to install the `mdparser` CLI tool system-wide so it can be used from anywhere.

## Current Setup

The project is already configured with:
- `pyproject.toml` with entry point: `mdparser = "mdparser.cli:main"`
- UV package management
- Python 3.8+ requirement

## Installation Options

### Option 1: UV Tool Install (Recommended) ⭐⭐⭐

**Best for**: CLI tools, system-wide access, isolated tool management

#### With Editable Install (`-e`) - Links to Source Code

```bash
cd mdparser
uv tool install -e .
uv tool update-shell
```

**How it works:**
- ✅ **Creates a LINK/REFERENCE back to your source code** (not a copy)
- ✅ Changes to your code are immediately reflected (no reinstall needed)
- ✅ UV creates an isolated environment for the tool
- ✅ Installs the `mdparser` command to `~/.local/share/uv/tools`
- ✅ The installed tool points back to your source directory

**What gets installed:**
- The command executable (`mdparser`) in UV's tools directory
- A link/reference to your source code (via `.pth` file or similar)
- Dependencies (mistletoe) in an isolated environment

**If you move/delete the source directory:**
- ❌ The tool will break (since it references the original location)
- You'll need to reinstall or update the path

#### Without Editable Install - Makes a Copy

```bash
cd mdparser
uv tool install .
uv tool update-shell
```

**How it works:**
- ✅ **Makes a COPY of your code** to UV's tool directory
- ❌ Changes to source code require reinstallation to take effect
- ✅ Tool works even if you move/delete the original source
- ✅ Good for production/stable versions

**What gets installed:**
- A copy of your package code in UV's tool environment
- The command executable (`mdparser`)
- Dependencies in an isolated environment

**Pros of Editable Install (`-e`):**
- ✅ Changes reflect immediately (great for development)
- ✅ No reinstallation needed for code changes
- ✅ Saves disk space (no copy)
- ✅ Always uses latest code

**Cons of Editable Install (`-e`):**
- ❌ Tool breaks if source directory is moved/deleted
- ❌ Requires source directory to exist

**Pros of Regular Install (no `-e`):**
- ✅ Tool works independently of source location
- ✅ Good for production/stable versions
- ✅ Can delete source after installation

**Cons of Regular Install (no `-e`):**
- ❌ Must reinstall for every code change
- ❌ Takes more disk space (full copy)

**Recommendation:**
- **Development**: Use `uv tool install -e .` (editable)
- **Production**: Use `uv tool install .` (copy)

**To verify editable install:**
```bash
# After installing with -e, make a test change to cli.py
# Then run mdparser --help - changes should appear immediately
```

**To verify regular install:**
```bash
# After installing without -e, make a change to cli.py
# Run mdparser --help - changes won't appear until reinstall
```

**Pros:**
- ✅ **Designed specifically for CLI tools** - UV's tool management system
- ✅ Editable install (`-e`) - changes reflect immediately
- ✅ Isolated tool environment - doesn't interfere with other Python projects
- ✅ Automatic PATH management with `uv tool update-shell`
- ✅ Fast installation with UV
- ✅ Easy to list/uninstall tools: `uv tool list`, `uv tool uninstall mdparser`
- ✅ Works with your Python version management (asdf)
- ✅ Better than `uv pip install` for CLI tools

**To verify:**
```bash
uv tool list                    # Should show mdparser
which mdparser                  # Should show path in UV tools dir
mdparser --help                 # Should work from anywhere
```

**To uninstall:**
```bash
uv tool uninstall mdparser
```

**To upgrade:**
```bash
uv tool install -e . --force    # For editable
# or
uv tool install . --force       # For regular install
```

**Note:** If `mdparser` command is not found after installation, run `uv tool update-shell` to update your shell configuration.

---

### Option 2: UV Pip Editable Install

**Best for**: Development when you want it in your Python environment

```bash
cd mdparser
uv pip install -e .
```

**Pros:**
- Changes to code are immediately available (editable install - links to source)
- Uses UV's fast package management
- Installs to UV's managed Python environment
- Entry point `mdparser` becomes available system-wide
- Respects your Python version management (asdf)

**How it works:**
- Creates a link/reference to your source code (editable install)
- Installs the `mdparser` command to Python's bin directory
- UV manages the Python environment automatically

**To verify:**
```bash
which mdparser
mdparser --help
```

**To uninstall:**
```bash
uv pip uninstall mdparser
```

---

### Option 3: UV Regular Install

**Best for**: Production use, stable version

```bash
cd mdparser
uv pip install .
```

**Pros:**
- Installs a stable copy (not editable)
- Uses UV's fast package management
- Entry point available system-wide
- Good for production deployments

**Cons:**
- Code changes require reinstallation
- Less convenient for development
- Makes a copy of your code

**To uninstall:**
```bash
uv pip uninstall mdparser
```

---

### Option 4: UV with Virtual Environment

**Best for**: Isolated installation, multiple projects

```bash
cd mdparser
uv venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows
uv pip install -e .
```

**Pros:**
- Isolated environment
- No conflicts with other Python packages
- Can have multiple versions

**Cons:**
- Need to activate virtual environment to use
- Not truly "system-wide" unless you add venv/bin to PATH

**To make it system-wide:**
Add to your shell config (`~/.zshrc` or `~/.bashrc`):
```bash
export PATH="/path/to/mdparser/.venv/bin:$PATH"
```

---

### Option 5: Build and Install Distribution Package

**Best for**: Distribution to others, production deployment

```bash
cd mdparser
uv build                    # Creates dist/mdparser-0.1.0.tar.gz
uv pip install dist/mdparser-0.1.0.tar.gz
```

**Pros:**
- Creates distributable package
- Can be shared with others
- Standard Python packaging

**Cons:**
- More steps
- Requires rebuilding for updates
- Makes a copy (not editable)

---

## Recommended Approach

**For your use case (CLI tool + system-wide access):**

```bash
cd mdparser
uv tool install -e .        # Editable install - links to source
uv tool update-shell
```

**Or for production:**

```bash
cd mdparser
uv tool install .           # Regular install - makes a copy
uv tool update-shell
```

This gives you:
- ✅ System-wide `mdparser` command
- ✅ Editable install (changes reflect immediately) - **if using `-e`**
- ✅ Fast UV package management
- ✅ Isolated tool environment (doesn't interfere with other projects)
- ✅ Automatic PATH management
- ✅ Easy tool management (`uv tool list`, `uv tool uninstall`)
- ✅ Respects your Python version (asdf)

**Why `uv tool` over `uv pip install`:**
- `uv tool` is specifically designed for CLI tools
- Better isolation and management
- Built-in PATH management
- Easier to see what tools you have installed

## Understanding Editable vs Regular Installs

### Editable Install (`-e` flag)
- **Links/References** your source code
- Changes are immediately available
- Source directory must exist
- Best for development

### Regular Install (no `-e`)
- **Copies** your code to installation location
- Changes require reinstallation
- Works independently of source location
- Best for production

## Verification After Installation

```bash
# Check if command is available
which mdparser

# Test the command
mdparser --help

# Test with a file
mdparser tests/sample-doc.md --headings 2

# For editable install: make a change and verify it's reflected
# Edit mdparser/cli.py, then run mdparser --help
# Changes should appear immediately
```

## Troubleshooting

### Command not found after installation

1. **Check UV's bin directory:**
   ```bash
   uv tool dir              # Shows tools directory
   echo $PATH | grep -i uv
   ```

2. **Update shell configuration:**
   ```bash
   uv tool update-shell
   # Then restart your terminal or run: source ~/.zshrc
   ```

3. **For asdf users:**
   UV respects asdf's Python shims, so `mdparser` should be available if Python is in PATH.

### Editable install not reflecting changes

1. **Verify it's editable:**
   ```bash
   uv tool list -v          # Should show editable flag
   ```

2. **Check source path:**
   The installed tool should reference your source directory

3. **Reinstall if needed:**
   ```bash
   uv tool install -e . --force
   ```

### Multiple Python versions

If you have multiple Python versions, ensure you're installing to the correct one:
```bash
python3 --version  # Check current version
uv tool install -e . --python python3.11  # Specify version if needed
```

## Uninstallation

```bash
uv tool uninstall mdparser
```

## Updating

**For editable installs (`-e`):**
- Updates are automatic - just edit the code!
- No reinstallation needed

**For regular installs:**
```bash
uv tool install . --force
```
