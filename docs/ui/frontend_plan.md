# Frontend Implementation Plan (frontend_plan.md)

This plan details the file structure, route setups, styling hooks, and state management strategy for building the NutriChat AI Admin Dashboard.

---

## 1. Next.js App Router Structure

We scaffold the dashboard inside the `/frontend` directory matching Next.js App Router guidelines:

```
frontend/
├── app/
│   ├── layout.tsx              # Root HTML wrapper, Google Fonts loader
│   ├── page.tsx                # Landing Page Component
│   ├── globals.css             # Tailwind imports & CSS theme vars
│   ├── auth/
│   │   ├── login/
│   │   │   └── page.tsx        # Login layout component
│   │   └── register/
│   │       └── page.tsx        # Register layout component
│   └── dashboard/
│       ├── layout.tsx          # Panel wrapper containing Sidebar navigation
│       ├── page.tsx            # Overview KPI grid view
│       ├── users/
│       │   └── page.tsx        # Users profiles management
│       ├── meals/
│       │   └── page.tsx        # Meals logs index
│       ├── analytics/
│       │   └── page.tsx        # Charts & report card dashboards
│       ├── feedback/
│       │   └── page.tsx        # Feedback audit log viewer
│       └── settings/
│           └── page.tsx        # System configuration panel
├── components/                 # Reusable UI widgets
│   ├── ui/                     # Custom shadcn wrapper classes (Button, Input, Card)
│   ├── Sidebar.tsx             # Panel Sidebar
│   └── CalorieChart.tsx        # Recharts analytics line/bar widget
└── lib/                        # Helper utils
    ├── api.ts                  # Axios client setup (JWT token interceptors)
    └── utils.ts                # Class merger helper (clsx + tailwind-merge)
```

---

## 2. Authentication & JWT Storage

*   **Cookie Security**: On login, write the JWT access token to standard cookies using `js-cookie` or standard server actions. Set SameSite parameters to prevent CSRF.
*   **Request Interceptor**: Create a standard Axios client instance inside `lib/api.ts` that intercepts requests to inject active authorization headers:
    ```typescript
    api.interceptors.request.use((config) => {
      const token = getAuthToken();
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
    ```
*   **Security Guards (Middleware)**: Set up a Next.js `middleware.ts` at the frontend root to inspect incoming cookies and block unauthenticated attempts from accessing paths under `/dashboard/*`.

---

## 3. Custom UI Widgets Scaffolding

We build custom dashboards widgets using Lucide Icons and Tailwind transitions:

*   **Glassmorphic Card**:
    ```typescript
    // components/ui/GlassCard.tsx
    export function GlassCard({ children, className }: { children: React.ReactNode, className?: string }) {
      return (
        <div className={`bg-slate-900/60 backdrop-blur-md border border-slate-800 rounded-xl p-6 shadow-xl ${className}`}>
          {children}
        </div>
      );
    }
    ```
*   **Motion Page Transitions**: Wrap dashboard pages with Framer Motion layout boundaries:
    ```typescript
    // components/PageWrapper.tsx
    'use client';
    import { motion } from 'framer-motion';
    export default function PageWrapper({ children }: { children: React.ReactNode }) {
      return (
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 15 }}
          transition={{ duration: 0.25 }}
        >
          {children}
        </motion.div>
      );
    }
    ```

---

## 4. Verification Milestone Steps

1.  **Boilerplate Verification**: Run npm build logs checking compile failures.
2.  **Lint Check**: Run local typescript checks using `npm run lint` and verify accessibility warnings inside console audits.
3.  **Unit Tests Validation**: Execute unit tests checking route guards.
