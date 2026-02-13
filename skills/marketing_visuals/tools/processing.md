# Image Processing

Process and enhance images for marketing content using CLI tools.

**Use this for**: Cropping photos, removing backgrounds, enhancing brightness/contrast, sharpening, and optimizing file size.

## Setup (First Time Only)

```bash
cd ~/.claude/plugins/cache/atlas-marketplace/atlas/*/skills/marketing_visuals/tools/processing-assets
bun install
```

## Available Tools

Run all commands from the assets directory:

```bash
cd ~/.claude/plugins/cache/atlas-marketplace/atlas/*/skills/marketing_visuals/tools/processing-assets
```

### 1. Crop (`bun crop`)

Crop images by aspect ratio or edge percentages.

```bash
# Aspect ratio (centered, largest possible)
bun crop photo.png --ratio 16:9
bun crop photo.png -r 1:1              # Square

# Edge cropping (percentage from each side)
bun crop photo.png --vertical 10       # 10% from top AND bottom
bun crop photo.png --horizontal 5      # 5% from left AND right
bun crop photo.png --top 15            # 15% from top only
bun crop photo.png --bottom 10         # 10% from bottom only

# Combined
bun crop photo.png -r 16:9 --top 5     # Ratio + edge trim

# Batch processing
bun crop ./images --ratio 4:3

# Custom output
bun crop photo.png -r 16:9 -o hero.png
```

**Output naming**: `{name}-{ratio}.{ext}` or `{name}-cropped.{ext}`

### 2. Remove Background (`bun remove-bg`)

AI-powered background removal. Outputs PNG with transparency.

```bash
# Single file
bun remove-bg photo.png
bun remove-bg photo.png transparent.png  # Custom output

# Batch processing
bun remove-bg ./portraits
```

**Note**: First run downloads ~30MB AI model.

**Output naming**: `{name}_nobg.png`

### 3. Polish (`bun polish`)

Enhance brightness, contrast, saturation, and sharpness.

```bash
# Individual adjustments (1.0 = no change)
bun polish photo.png --brightness 1.1    # 10% brighter
bun polish photo.png --contrast 1.2      # 20% more contrast
bun polish photo.png --saturation 1.3    # 30% more vibrant
bun polish photo.png --sharpen 1.5       # Sharpen (sigma 1.5)

# Auto-enhance (normalize + light sharpen)
bun polish photo.png --auto

# Combine adjustments
bun polish photo.png -b 1.1 -c 1.15 --sharpen 1

# Batch processing
bun polish ./images --auto
```

**Multiplier reference**: 0.5 = 50%, 1.0 = no change, 1.5 = 150%, 2.0 = maximum recommended

**Output naming**: `{name}-polished.{ext}`

### 4. Optimize (`bun optimize`)

Compress and convert images for web.

```bash
# Convert to WebP (default, best compression)
bun optimize photo.png
bun optimize photo.png -q 60             # Lower quality, smaller

# Lossless WebP
bun optimize photo.png --lossless

# Keep original format
bun optimize photo.png --keep-format

# Batch processing
bun optimize ./images
```

**Output naming**: `{name}.webp` or `{name}-optimized.{ext}`

## Common Workflows

### Prepare Portrait for Website

```bash
cd ~/.claude/plugins/cache/atlas-marketplace/atlas/*/skills/marketing_visuals/tools/processing-assets

bun remove-bg portrait.jpg
bun crop portrait_nobg.png -r 1:1
bun polish portrait_nobg-1x1.png --auto
bun optimize portrait_nobg-1x1-polished.png
```

### Prepare Blog Hero Image

```bash
bun crop photo.jpg -r 2:1
bun polish photo-2x1.jpg -b 1.05 -c 1.1 --sharpen 0.8
bun optimize photo-2x1-polished.jpg -q 85
```

## Tips

1. **Order matters**: Remove BG → Crop → Polish → Optimize
2. **Check results visually**: Use Read tool to view output images
3. **Be subtle with polish**: Start with small adjustments (1.05-1.15)
4. **Auto is safe**: `--auto` gives good results for most photos
5. **WebP for web**: Always optimize final images for smaller file sizes
