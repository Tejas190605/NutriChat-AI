# Design System Specifications (system.md)

This specification defines the colors, typography, spacing scales, and UI component standards for the NutriChat AI Admin Dashboard.

---

## 1. Color Palette (Modern Dark-Mode Focused)

To convey health, precision, and modern SaaS vibes, we establish a premium glassmorphic dark-mode palette utilizing curated HSL colors.

| Color Variable | HSL Token | UI Role |
| :--- | :--- | :--- |
| `--background` | `hsl(222, 47%, 6%)` | Overall page backdrop |
| `--card` | `hsl(222, 47%, 10%)` | Glass containers backgrounds |
| `--card-border` | `hsl(217, 32%, 18%)` | Container boundaries border |
| `--primary` | `hsl(150, 84%, 38%)` | Health Emerald primary actions |
| `--primary-foreground`| `hsl(150, 100%, 96%)` | Text inside primary buttons |
| `--accent` | `hsl(190, 90%, 45%)` | Cyan micro-indicators / chart lines |
| `--warning` | `hsl(38, 92%, 50%)` | Calorie limits boundary alerts |
| `--destructive` | `hsl(0, 84%, 60%)` | Warning logs / log deletions |
| `--text-main` | `hsl(210, 40%, 98%)` | High-contrast body text |
| `--text-muted` | `hsl(215, 20%, 65%)` | Captions, labels, timestamps |

---

## 2. Typography

We import Google Fonts (`Outfit` for titles, `Inter` for tables and inputs) to deliver a modern, clean interface.

*   **Font Weights**:
    *   `Light`: 300 | `Regular`: 400 | `Medium`: 500 | `SemiBold`: 600 | `Bold`: 700
*   **Scale Limits**:
    *   `Display Title`: `Outfit` | `3rem` (48px) | `leading-none` | `font-bold`
    *   `Heading 1`: `Outfit` | `2.25rem` (36px) | `leading-tight` | `font-semibold`
    *   `Heading 2`: `Outfit` | `1.5rem` (24px) | `leading-snug` | `font-medium`
    *   `Body Main`: `Inter` | `1rem` (16px) | `leading-relaxed` | `font-regular`
    *   `Caption Muted`: `Inter` | `0.875rem` (14px) | `leading-normal` | `font-light`

---

## 3. Spacing System (4px-Based Grid)

We utilize standard tailwind utilities mapped to a 4px (0.25rem) increment:

| Token | Rem Value | Pixel Value | Typical Application |
| :--- | :--- | :--- | :--- |
| `space-1` | `0.25rem` | 4px | Small line spacing |
| `space-2` | `0.5rem` | 8px | Button padding-x, items gaps |
| `space-4` | `1.0rem` | 16px | Container padding, grid gap |
| `space-6` | `1.5rem` | 24px | Page sections margins |
| `space-8` | `2.0rem` | 32px | Massive panels outer boundaries |

---

## 4. Components & Iconography

*   **Icon Library**: Lucide Icons exclusively. Use uniform sizes:
    *   *Toolbar Buttons*: 16px (`w-4 h-4`)
    *   *Card Title Icons*: 20px (`w-5 h-5`)
    *   *KPI Hero Icons*: 24px (`w-6 h-6`)
*   **Standard Component Tokens**:
    *   *Rounded Corners*: Dashboard containers use `rounded-xl` (12px), buttons use `rounded-lg` (8px).
    *   *Borders*: Standard border: `border border-slate-800`.
    *   *BGs*: Glass containers use `bg-slate-900/60 backdrop-blur-md`.

---

## 5. Motion & Animation (Framer Motion)

Define standard transition metrics to ensure micro-animations feel sleek:

*   **Standard Transition Easing**: `easeInOut` or spring values:
    *   *Spring config*: `type: "spring", stiffness: 300, damping: 30`
*   **Transition Speeds**:
    *   *Hover states*: 0.15s (150ms) fade transitions.
    *   *Modal slide-in*: 0.3s (300ms) with `y: [50, 0]` translation limits.
    *   *Sidebar toggle*: 0.25s (250ms) layout width change.

---

## 6. Accessibility (WCAG 2.2 AA Checklist)

*   [ ] **Color Contrast**: Maintain a minimum contrast ratio of **4.5:1** for body text and **3:1** for visual indicators.
*   [ ] **Keyboard Focus**: Focus ring `focus:ring-2 focus:ring-emerald-500` visible on all interactive tags when focused.
*   [ ] **Aria Attributes**: Include `aria-label` or `aria-labelledby` on widgets, buttons, and custom charts elements.
*   [ ] **Document Headings**: Maintain semantic headers flow order (`h1` -> `h2` -> `h3`). Do not skip hierarchy steps.
*   [ ] **Screen Reader Support**: Use semantic tags (`<header>`, `<nav>`, `<main>`, `<footer>`, `<aside>`).
