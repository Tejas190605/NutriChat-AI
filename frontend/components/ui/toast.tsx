"use client";

import React from "react";
import { useNotification, ToastType } from "@/contexts/NotificationContext";
import { CheckCircle2, AlertCircle, AlertTriangle, Info, X } from "lucide-react";
import { clsx } from "clsx";

const icons: Record<ToastType, React.FC<{ className?: string }>> = {
  success: CheckCircle2,
  error: AlertCircle,
  warning: AlertTriangle,
  info: Info,
};

const styles: Record<ToastType, string> = {
  success: "bg-emerald-950/80 border-emerald-800/60 text-emerald-200",
  error: "bg-rose-950/80 border-rose-800/60 text-rose-200",
  warning: "bg-amber-950/80 border-amber-800/60 text-amber-200",
  info: "bg-cyan-950/80 border-cyan-800/60 text-cyan-200",
};

export const ToastContainer: React.FC = () => {
  const { toasts, removeToast } = useNotification();

  return (
    <div className="fixed bottom-5 right-5 z-50 flex flex-col gap-2.5 max-w-sm w-full">
      {toasts.map((toast) => {
        const Icon = icons[toast.type];
        return (
          <div
            key={toast.id}
            className={clsx(
              "flex items-start gap-3 p-4 rounded-xl border backdrop-blur-md shadow-lg animate-in slide-in-from-bottom-5 duration-200",
              styles[toast.type]
            )}
          >
            <Icon className="h-5 w-5 flex-shrink-0 mt-0.5" />
            <div className="flex-1">
              <h4 className="text-sm font-semibold">{toast.title}</h4>
              {toast.description && <p className="text-xs opacity-90 mt-0.5">{toast.description}</p>}
            </div>
            <button onClick={() => removeToast(toast.id)} className="opacity-70 hover:opacity-100 p-0.5">
              <X className="h-4 w-4" />
            </button>
          </div>
        );
      })}
    </div>
  );
};
