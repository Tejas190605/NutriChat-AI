"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Utensils,
  BrainCircuit,
  LineChart,
  MessageSquare,
  ShieldCheck,
  Settings,
  Sparkles,
} from "lucide-react";
import { clsx } from "clsx";

export const navItems = [
  { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { label: "Nutrition & Meals", href: "/dashboard/nutrition", icon: Utensils },
  { label: "AI Coach & WhatsApp", href: "/dashboard/ai-coach", icon: BrainCircuit },
  { label: "Analytics & Telemetry", href: "/dashboard/analytics", icon: LineChart },
  { label: "Conversations Log", href: "/dashboard/conversations", icon: MessageSquare },
  { label: "Admin Operations", href: "/admin", icon: ShieldCheck, adminOnly: true },
  { label: "Settings", href: "/dashboard/settings", icon: Settings },
];

export const Sidebar: React.FC = () => {
  const pathname = usePathname();

  return (
    <aside className="w-64 flex-shrink-0 border-r border-slate-800 bg-slate-950/80 backdrop-blur-xl flex flex-col justify-between h-screen sticky top-0 z-40">
      <div>
        {/* Brand Header */}
        <div className="flex items-center gap-3 px-6 h-16 border-b border-slate-800/80">
          <div className="h-9 w-9 rounded-xl bg-gradient-to-tr from-emerald-500 to-cyan-500 flex items-center justify-center text-white shadow-glow">
            <Sparkles className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-base font-bold tracking-tight text-white">NutriChat AI</h1>
            <p className="text-[10px] font-medium text-emerald-400 uppercase tracking-widest">Autonomous Agent</p>
          </div>
        </div>

        {/* Navigation Links */}
        <nav className="p-4 space-y-1.5">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href || (item.href !== "/dashboard" && pathname.startsWith(item.href));

            return (
              <Link
                key={item.href}
                href={item.href}
                className={clsx(
                  "flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all duration-200",
                  isActive
                    ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 shadow-sm"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-900/60"
                )}
              >
                <Icon className={clsx("h-4 w-4", isActive ? "text-emerald-400" : "text-slate-400")} />
                {item.label}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Footer Info */}
      <div className="p-4 border-t border-slate-800/80 text-[11px] text-slate-500">
        <div className="flex items-center justify-between">
          <span>Engine v0.1.9</span>
          <span className="inline-flex items-center gap-1 text-emerald-400 font-medium">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" /> Online
          </span>
        </div>
      </div>
    </aside>
  );
};
