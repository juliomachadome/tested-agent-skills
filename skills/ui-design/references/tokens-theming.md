# Design tokens and theming

## Contents
1. Three layers
2. W3C DTCG format
3. Naming
4. Scales to define
5. Theming: light, dark, contrast, brand
6. Component states
7. Enforcement

## 1. Three layers
- Primitive: raw values with no meaning (`blue-600`, `space-4`, `radius-8`).
- Semantic: roles that map to primitives (`color-action-primary`, `text-secondary`, `space-inset-card`, `status-danger`).
- Component: decisions for one component (`button-primary-bg`).
Screens and components consume semantic and component tokens only. Rebranding, dark mode and density modes then become a remapping of the semantic layer. The three-layer pattern is common across mature systems (Material, Carbon, Polaris, Primer); treat it as consensus practice, not a standard.

Atomic Design (Frost, 2016) gives the matching component mental model: atoms (label, input, button), molecules (search form), organisms (header), templates (layout with content structure) and pages (templates with real content, used to test the system). Design tokens feed the atoms; pages with real content are where the system is stress-tested. The stages are a way to move between parts and the whole, not a fixed sequence. (https://atomicdesign.bradfrost.com/chapter-2/, read 2026-11-15)

Material's web library uses the same three levels under the names reference, system and component tokens, exposed as CSS custom properties (for example `--md-sys-color-primary`, `--md-sys-typescale-*`, `--md-sys-shape-corner-*`) that can be scoped to override a single component. (Material Web theming docs, read 2026-11-15)

## 2. W3C DTCG format
Design Tokens Format Module 2025.10, a Final Community Group Report dated 28 October 2025 (not a W3C Standard, described as stable). (https://www.designtokens.org/tr/2025.10/format/, read 2026-11-14)
- A token is an object with a required `$value`; the parent key is its name. Optional `$type`, `$description`, `$extensions` (reverse-domain keys recommended; tools must preserve unknown data), `$deprecated` (true, false or a string).
- `$type` may be inherited from the nearest group or from a referenced token; if it cannot be determined the token is invalid. Tools must not guess a type from the value.
- Base types: color, dimension, fontFamily, fontWeight, duration, cubicBezier, number. Composite: strokeStyle, border, transition, shadow, gradient, typography.
- Aliases: curly braces reference a whole token by dotted path, for example `{color.blue.600}`; sub-properties are reached with a JSON Pointer `$ref`.
- Media type `application/design-tokens+json`; recommended extensions `.tokens` and `.tokens.json`. Separate modules exist for color and for theme resolution.

Minimal example:
```json
{
  "color": {
    "$type": "color",
    "blue": { "600": { "$value": "#1d4ed8" } },
    "action": { "primary": { "$value": "{color.blue.600}", "$description": "Primary action background" } }
  },
  "space": { "$type": "dimension", "4": { "$value": "16px" } }
}
```
Generate CSS custom properties (and platform files) from this source with a build step; hand-edited duplicates drift.

## 3. Naming
Name by role, not appearance: `text-secondary` not `gray-500`; `status-danger` not `red`. Names stay valid when values change. Avoid encoding the theme in the name (`text-primary-dark`); themes remap the same name.

## 4. Scales to define
- Space (4 base), type roles (composite: family, size, line height, weight, tracking), color ramps (neutral, action, four statuses), radius (2 to 3 values), elevation (3 levels), border width, opacity, z-index layers, duration (for example 100, 200, 300 ms), easing (2 to 3 curves), breakpoints, target sizes.
- A token should exist only if used in more than one place or if it records a decision; a token per pixel becomes magic numbers with extra steps.

## 5. Theming
- Light, dark and high contrast are different semantic mappings. Dark is not inverted light. Re-verify contrast per mapping (color-contrast.md).
- Brand themes may change brand-role tokens only. Status and severity tokens are locked. Enforce in the token pipeline: a tenant file with a status key fails validation.
- Switch themes with a `data-theme` attribute on the root plus `prefers-color-scheme` and `prefers-contrast` media queries; declare `color-scheme` per theme.
- Density modes (compact, comfortable) remap spacing and row-height tokens, not component code.
- Provide fallbacks (`backdrop-filter` surfaces need a solid fallback and respect `prefers-reduced-transparency`).

## 6. Component states
Every interactive component defines default, hover, focus-visible, pressed, disabled, loading, error (and selected where relevant). A component missing states is not finished. Focus ring by `outline` so it survives forced colors.

## 7. Enforcement
- Lint rule rejecting raw hex colors and off-scale spacing in component code.
- Test that rejects font sizes outside the scale.
- Contrast matrix test over text/background token pairs in every theme.
- Review by `grep` for `#[0-9a-fA-F]{3,8}` where lint does not reach.
- Document tokens with their role and allowed pairings; deprecate with `$deprecated` rather than deleting.

## Sources
- Frost, Atomic Design (2016), https://atomicdesign.bradfrost.com/chapter-2/, read 2026-11-15
- Material Web theming, https://github.com/material-components/material-web/blob/main/docs/theming/README.md, read 2026-11-15
- W3C Design Tokens Community Group, Design Tokens Format Module 2025.10, https://www.designtokens.org/tr/2025.10/format/, read 2026-11-14
- Material Design 3 design tokens overview, https://m3.material.io/foundations/design-tokens/overview (not re-verified)
- MDN prefers-contrast, forced-colors, color-scheme (prior reading, not re-fetched)
