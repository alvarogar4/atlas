# Schema Generation

Generate pixel-perfect diagrams and schemas as PNG images from HTML+CSS.

**Use this for**: Architecture diagrams, flowcharts, comparisons, technical diagrams, data visualizations, UI mockups.

## Workflow

1. **Create HTML file** in `${CONTENT_FOLDER}/resources/{NN}-{name}.html`
2. **Run generator** from skill folder:
   ```bash
   cd ~/.claude/plugins/cache/atlas-marketplace/atlas/*/skills/marketing_visuals/tools/schema-generation-assets
   bun install  # first time only
   bun generate-pngs.mjs ${CONTENT_FOLDER}/resources
   ```
3. **Verify and refine** (MANDATORY - do not skip):
   - Read the generated PNG using the `Read` tool to visually inspect
   - Check for: overlapping elements, inconsistent spacing, alignment issues, truncated text, visual balance
   - If issues found: edit HTML/CSS → re-run generator → re-verify
   - Only deliver when the diagram looks professional and refined

## Color Mapping

Map visual-identity.md colors to CSS variables:

| Visual Identity Field | CSS Variable |
|-----------------------|-------------|
| Base 100 (dark) | `--bg` |
| Base 200 (dark) | `--surface`, `--bg-lighter` |
| Base 300 (dark) | `--surface-border` |
| Base 400 (dark) | `--muted` |
| Title (dark) | `--foreground` |
| Content (dark) | `--muted-fg` |
| Primary (dark) | `--primary` |
| Accent (dark) | `--accent` |

## Design Patterns

**Box/Card:**
```css
.card {
  background: var(--surface);
  border: 1px solid var(--surface-border);
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.3);
}
```

**Highlighted Box (primary):**
```css
.highlight-box {
  background: linear-gradient(135deg, var(--primary-dim) 0%, var(--primary-glow) 100%);
  border: 1px solid var(--primary);
  border-radius: 10px;
}
```

**Glow Effect:**
```css
.glow {
  box-shadow: 0 0 20px var(--primary-glow);
  border: 1px solid var(--primary);
}
```

**SVG Connections:**
```css
.conn-line {
  stroke: var(--primary);
  stroke-width: 2;
  fill: none;
  filter: drop-shadow(0 0 4px var(--primary-glow));
}
```

## File Naming

```
{NN}-{description}.html    # Source HTML
{NN}-{description}.png     # Generated PNG
```

Examples:
- `01-distributed-architecture.html`
- `02-data-flow-diagram.html`
- `03-before-after-comparison.html`
