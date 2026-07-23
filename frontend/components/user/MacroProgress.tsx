import React from "react";
import { clsx } from "clsx";

export interface MacroProgressProps {
  label: string;
  current: number;
  target: number;
  unit?: string;
  color?: "emerald" | "cyan" | "amber" | "purple";
  className?: string;
}

const colorMap = {
  emerald: "bg-emerald-500 text-emerald-400",
  cyan: "bg-cyan-500 text-cyan-400",
  amber: "bg-amber-500 text-amber-400",
  purple: "bg-purple-500 text-purple-400",
};

export const MacroProgress: React.FC<MacroProgressProps> = ({
  label,
  current,
  target,
  unit = "g",
  color = "emerald",
  className,
}) => {
  const percentage = Math.min(100, Math.round((current / (target || 1)) * 100));

  return (
    <div className={clsx("space-y-1.5", className)}>
      <div className="flex justify-between text-xs font-semibold">
        <span className="text-slate-300">{label}</span>
        <span className="text-white">
          {current} <span className="text-slate-500">/ {target} {unit}</span> ({percentage}%)
        </span>
      </div>
      <div className="h-2 w-full bg-slate-900 rounded-full overflow-hidden border border-slate-800">
        <div
          className={clsx("h-full transition-all duration-500 rounded-full", colorMap[color].split(" ")[0])}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};
