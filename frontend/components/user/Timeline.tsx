import React from "react";
import { Clock } from "lucide-react";

export interface TimelineItem {
  id: string;
  title: string;
  subtitle: string;
  timestamp: string;
  type?: "meal" | "weight" | "coaching";
}

export interface TimelineProps {
  items: TimelineItem[];
}

export const Timeline: React.FC<TimelineProps> = ({ items }) => {
  return (
    <div className="relative pl-6 space-y-6 before:absolute before:left-2 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-800">
      {items.map((item) => (
        <div key={item.id} className="relative group">
          <div className="absolute -left-[22px] top-1 h-3 w-3 rounded-full bg-emerald-500 ring-4 ring-slate-950" />
          <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1">
            <div className="flex items-center justify-between">
              <h5 className="text-xs font-bold text-white">{item.title}</h5>
              <span className="text-[10px] text-slate-500 flex items-center gap-1">
                <Clock className="h-3 w-3" /> {new Date(item.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
              </span>
            </div>
            <p className="text-xs text-slate-400">{item.subtitle}</p>
          </div>
        </div>
      ))}
    </div>
  );
};
