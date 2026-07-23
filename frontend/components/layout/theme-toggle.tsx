"use client";

import React from "react";
import { useTheme } from "@/contexts/ThemeContext";
import { Sun, Moon, Laptop } from "lucide-react";
import { clsx } from "clsx";

export const ThemeToggle: React.FC = () => {
  const { theme, setTheme } = useTheme();

  return (
    <div className="flex items-center gap-1 rounded-lg border border-slate-800 bg-slate-900/80 p-1">
      <button
        onClick={() => setTheme("light")}
        className={clsx(
          "p-1.5 rounded-md transition-colors",
          theme === "light" ? "bg-slate-800 text-amber-400" : "text-slate-400 hover:text-white"
        )}
        title="Light Mode"
      >
        <Sun className="h-4 w-4" />
      </button>
      <button
        onClick={() => setTheme("dark")}
        className={clsx(
          "p-1.5 rounded-md transition-colors",
          theme === "dark" ? "bg-slate-800 text-emerald-400" : "text-slate-400 hover:text-white"
        )}
        title="Dark Mode"
      >
        <Moon className="h-4 w-4" />
      </button>
      <button
        onClick={() => setTheme("system")}
        className={clsx(
          "p-1.5 rounded-md transition-colors",
          theme === "system" ? "bg-slate-800 text-cyan-400" : "text-slate-400 hover:text-white"
        )}
        title="System Preference"
      >
        <Laptop className="h-4 w-4" />
      </button>
    </div>
  );
};
