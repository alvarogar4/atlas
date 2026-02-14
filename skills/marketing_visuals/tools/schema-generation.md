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
3. **Quality check** (MANDATORY - do not skip):

   Read the generated PNG using the `Read` tool and verify ALL of the following before delivering:

   **Layout & spacing:**
   - Content fills the canvas — no more than 5-8% margin on any side
   - Grid/layout is centered both horizontally and vertically
   - Elements are visually connected, not floating in isolation
   - No large empty gaps between content sections

   **Connections & lines:**
   - Every arrow/line actually start from the source and reaches its target element (verify coordinates match)
   - Prefer CSS connections (gradient divs, borders, pseudo-elements with `::before`/`::after`) over SVG paths — SVG coordinates easily desync from CSS-positioned elements
   - If SVG is used: double-check that path start/end points align with the actual rendered position of HTML elements

   **Text readability:**
   - Body text: minimum 13px
   - Headings/titles: minimum 16px
   - Labels on small elements: minimum 11px
   - All text has sufficient contrast against its background (WCAG tests)

   **Visual consistency:**
   - No emojis in professional/technical diagrams — use icons or shapes instead
   - Consistent color usage following the color mapping below
   - Consistent border-radius, padding, and shadow across similar elements

   If ANY check fails: edit HTML/CSS → re-run generator → re-verify. Only deliver when all checks pass.

## Color Mapping

Map visual-identity.md colors to CSS variables:

| Visual Identity Field | CSS Variable                |
| --------------------- | --------------------------- |
| Base 100              | `--bg`                      |
| Base 200              | `--surface`, `--bg-lighter` |
| Base 300              | `--surface-border`          |
| Base 400              | `--muted`                   |
| Title                 | `--foreground`              |
| Content               | `--muted-fg`                |
| Primary               | `--primary`                 |
| Accent                | `--accent`                  |

## Design Patterns

**Box/Card:**

```css
.card {
  background: var(--surface);
  border: 1px solid var(--surface-border);
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
}
```

**Highlighted Box (primary):**

```css
.highlight-box {
  background: linear-gradient(
    135deg,
    var(--primary-dim) 0%,
    var(--primary-glow) 100%
  );
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

**CSS Connections (preferred):**

```css
/* Horizontal connector between elements */
.connector {
  width: 40px;
  height: 2px;
  background: linear-gradient(90deg, var(--primary), var(--primary-glow));
  align-self: center;
  box-shadow: 0 0 6px var(--primary-glow);
}
/* Arrow tip via pseudo-element */
.connector::after {
  content: "";
  position: absolute;
  right: -4px;
  top: -3px;
  border: 4px solid transparent;
  border-left-color: var(--primary-glow);
}
```

**SVG Connections (use only when CSS layout can't express the path):**

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
