import React from "react";
import { Card } from "./card";
import { LucideIcon } from "lucide-react";

export interface StatsCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  trend?: {
    value: string | number;
    isPositive: boolean;
  };
  icon?: LucideIcon;
  iconColor?: string;
}

export const StatsCard: React.FC<StatsCardProps> = ({
  title,
  value,
  subtitle,
  trend,
  icon: Icon,
  iconColor = "text-emerald-400",
}) => {
  return (
    <Card className="flex flex-col justify-between hover:border-slate-700/80 transition-all">
      <div className="flex items-start justify-between">
        <div>
          <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">{title}</span>
          <div className="mt-2 text-2xl font-bold tracking-tight text-white">{value}</div>
        </div>
        {Icon && (
          <div className={`p-2.5 rounded-lg bg-slate-800/80 border border-slate-700/50 ${iconColor}`}>
            <Icon className="h-5 w-5" />
          </div>
        )}
      </div>
      {(subtitle || trend) && (
        <div className="mt-4 flex items-center justify-between text-xs">
          {subtitle && <span className="text-slate-400">{subtitle}</span>}
          {trend && (
            <span
              className={`font-semibold ${trend.isPositive ? "text-emerald-400" : "text-rose-400"}`}
            >
              {trend.isPositive ? "+" : ""}{trend.value}
            </span>
          )}
        </div>
      )}
    </Card>
  );
};
