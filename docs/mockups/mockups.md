# Visual Design Mockups (mockups.md)

This specification defines the high-fidelity styling tokens, responsive grids, borders, shadow rules, hover properties, and animation triggers for the NutriChat AI screens.

---

## 1. Visual Styling Principles

To align with a premium HealthTech look, we apply a glassmorphic aesthetic to all dashboard elements:

*   **Containers Background**: `bg-slate-950/60 backdrop-blur-lg`
*   **Borders**: `border border-slate-800`
*   **Shadows**: `shadow-xl shadow-black/20`
*   **Hover states**: Elevate borders and background opacities when hover action triggers:
    `hover:border-emerald-500/40 hover:bg-slate-900/80 transition-all duration-200`

---

## 2. Page Specific Visual Specs

### Landing Page Hero Card
*   *Background*: Deep radial gradient starting at primary HSL color matching emerald to absolute black background.
    *   *Classes*: `bg-gradient-to-tr from-slate-950 via-slate-900 to-emerald-950/20`
*   *Buttons Call-To-Action*: Emerald buttons transition to cyan highlight on hover.
    *   *Classes*: `bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg px-6 py-3 font-semibold shadow-md shadow-emerald-900/30 transition-all active:scale-95`

### KPI Cards Dashboard
*   *Layout Grid*: Responsive cards grid scaling with screen widths:
    *   *Classes*: `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6`
*   *Metrics Typography*: Bold large numerals utilizing `Outfit` font:
    *   *Classes*: `text-3xl font-bold tracking-tight text-white mt-2`
*   *Border Highlight*: Top boundary of each card features a subtle gradient line:
    *   *Classes*: `h-1 w-full bg-gradient-to-r from-emerald-500 to-cyan-500 rounded-t-xl`

### Dashboard Interactive Charts
*   *Visuals*: Custom recharts containers wrapped in responsive panels:
    *   *Chart grid lines*: `stroke-slate-800`
    *   *Calorie target line*: Dashed orange line `stroke-amber-500 stroke-dasharray="5 5"`
    *   *Log intake bars*: Solid emerald gradient `fill="url(#emerald-gradient)"`

---

## 3. Responsive Strategy & Breakpoints

We utilize mobile-first responsive grids. The NextJS dashboard renders cleanly on all viewports:

*   **Mobile view (`< 768px`)**:
    *   Sidebar folds into a compact top header panel or overlay sheet (`drawer`).
    *   Grids collapse to `grid-cols-1` with padding-x set to `px-4`.
*   **Tablet view (`768px` to `1024px`)**:
    *   Sidebar shows icons only (`w-16`).
    *   Grids scale to `grid-cols-2`.
*   **Desktop view (`> 1024px`)**:
    *   Sidebar locks at full width (`w-64`).
    *   Grids expand to full columns mapping (`grid-cols-3` or `grid-cols-4`).
