"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, Utensils, BrainCircuit, TrendingUp, User } from "lucide-react";
import { clsx } from "clsx";

const mobileNavItems = [
  { label: "Home", href: "/dashboard/home", icon: Home },
  { label: "Meals", href: "/dashboard/meals", icon: Utensils },
  { label: "AI Coach", href: "/dashboard/ai-coach", icon: BrainCircuit },
  { label: "Progress", href: "/dashboard/progress", icon: TrendingUp },
  { label: "Profile", href: "/dashboard/profile", icon: User },
];

export const BottomNavigation: React.FC = () => {
  const pathname = usePathname();

  return (
    <nav className="sm:hidden fixed bottom-0 left-0 right-0 h-16 border-t border-slate-800 bg-slate-950/90 backdrop-blur-xl flex items-center justify-around z-40 px-2 pb-safe">
      {mobileNavItems.map((item) => {
        const Icon = item.icon;
        const isActive =
          pathname === item.href || (item.href === "/dashboard/home" && pathname === "/dashboard");

        return (
          <Link
            key={item.href}
            href={item.href}
            className={clsx(
              "flex flex-col items-center justify-center w-full py-1 text-[10px] font-semibold transition-all",
              isActive ? "text-emerald-400 font-bold" : "text-slate-500 hover:text-slate-300"
            )}
          >
            <Icon className={clsx("h-5 w-5 mb-0.5", isActive ? "text-emerald-400" : "text-slate-500")} />
            <span>{item.label}</span>
          </Link>
        );
      })}
    </nav>
  );
};
