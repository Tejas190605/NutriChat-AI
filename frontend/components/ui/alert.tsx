import React from "react";
import { AlertCircle, CheckCircle2, AlertTriangle, Info } from "lucide-react";
import { clsx } from "clsx";

export interface AlertProps {
  variant?: "success" | "error" | "warning" | "info";
  title: string;
  children?: React.ReactNode;
  className?: string;
}

const icons = {
  success: CheckCircle2,
  error: AlertCircle,
  warning: AlertTriangle,
  info: Info,
};

const variants = {
  success: "bg-emerald-950/40 border-emerald-800/50 text-emerald-300",
  error: "bg-rose-950/40 border-rose-800/50 text-rose-300",
  warning: "bg-amber-950/40 border-amber-800/50 text-amber-300",
  info: "bg-cyan-950/40 border-cyan-800/50 text-cyan-300",
};

export const Alert: React.FC<AlertProps> = ({ variant = "info", title, children, className }) => {
  const Icon = icons[variant];
  return (
    <div className={clsx("flex items-start gap-3 p-4 rounded-xl border", variants[variant], className)}>
      <Icon className="h-5 w-5 flex-shrink-0 mt-0.5" />
      <div>
        <h5 className="text-sm font-semibold">{title}</h5>
        {children && <div className="text-xs opacity-90 mt-1">{children}</div>}
      </div>
    </div>
  );
};
