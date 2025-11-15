# Package Name Recommendations

## Current Situation

- **Current name**: `mdparser`
- **PyPI status**: Name is taken (old/inactive package from 2020)
- **Most common names**: All taken on PyPI

## Key Considerations

Since this is primarily for **local/private use** (not necessarily publishing to PyPI), you have flexibility:

1. **For local use**: Any name works - `mdparser` is fine
2. **For potential publishing**: Need unique name or namespace
3. **For discoverability**: Descriptive names help
4. **For typing**: Shorter is better

## Recommendations

### Option 1: Keep `mdparser` (Recommended for Local Use) ⭐⭐⭐

**Pros:**
- ✅ Already established in your codebase
- ✅ Simple, clear, professional
- ✅ Easy to remember and type
- ✅ Works perfectly for local installation
- ✅ Generic enough for discoverability

**Cons:**
- ❌ Taken on PyPI (but old/inactive package)
- ❌ Not unique if you want to publish

**Best for**: Local/private use, internal tools

**Usage**: `mdparser document.md --headings 3`

---

### Option 2: Use Namespace/Scoped Name (If Publishing)

If you want to publish to PyPI, consider:
- `puya-mdparser` (your name + tool)
- `wth-mdparser` (company/org + tool)
- `verge-mdparser` (project-specific)

**Pros:**
- ✅ Unique on PyPI
- ✅ Keeps familiar `mdparser` name
- ✅ Shows ownership/origin

**Cons:**
- ❌ Longer command name
- ❌ Requires namespace setup

---

### Option 3: More Descriptive Names

#### `markdown-extractor-cli`
- Very clear purpose
- Long but descriptive
- Check PyPI availability

#### `md-struct-extract`
- Emphasizes structured extraction
- Clear purpose
- Check PyPI availability

#### `markdown-info-extract`
- Very descriptive
- Long for CLI usage
- Check PyPI availability

---

### Option 4: Creative/Unique Names

Since most `md*` names are taken, consider:

#### `mdsnip` ⭐
- Implies snipping/extracting pieces
- Short (6 chars)
- Memorable
- Check PyPI availability

#### `mdclip` ⭐
- Implies clipping/extracting
- Short (5 chars)
- Clear purpose
- Check PyPI availability

#### `mdtap` ⭐
- Implies tapping into content
- Very short (5 chars)
- Unique
- Check PyPI availability

#### `mdflow` ⭐
- Implies flowing/extracting content
- Modern feel
- Short (6 chars)
- Check PyPI availability

---

## My Top Recommendation

### **Keep `mdparser`** ⭐⭐⭐

**Why:**
1. **Already established** - You've built the whole project with this name
2. **Works for local use** - PyPI name conflict doesn't matter for local installs
3. **Simple and clear** - Easy to understand and remember
4. **Professional** - Generic enough to be discoverable
5. **Easy to type** - Short, no special characters

**If you need to publish later:**
- Use namespace: `yourname-mdparser`
- Or rename at that time (it's just a few config changes)

**If you want something more unique now:**
- `mdsnip` - Short, memorable, implies extraction
- `mdclip` - Clear purpose, easy to type
- `mdtap` - Very short, unique

## Decision Matrix

| Name | Length | Clarity | Uniqueness | Typing Ease | Recommendation |
|------|--------|---------|------------|-------------|----------------|
| `mdparser` | 8 | ⭐⭐⭐ | ⭐ | ⭐⭐⭐ | **Keep it** |
| `mdsnip` | 6 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | Good alternative |
| `mdclip` | 5 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | Good alternative |
| `mdtap` | 5 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | Good alternative |
| `markdown-extractor-cli` | 22 | ⭐⭐⭐ | ⭐⭐ | ⭐ | Too long |

## Final Recommendation

**For your use case (local tool, AI-agent optimized):**

**Keep `mdparser`** - It's:
- ✅ Already working
- ✅ Clear and professional
- ✅ Perfect for local installation
- ✅ Easy to change later if needed

The PyPI name conflict only matters if you plan to publish. For local use with `uv tool install`, any name works perfectly!

