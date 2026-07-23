"use client";

import React, { useState } from "react";
import { Droplet, Plus, Minus } from "lucide-react";
import { Button } from "../ui/button";

export interface WaterTrackerProps {
  initialMl?: number;
  targetMl?: number;
  onUpdate?: (ml: number) => void;
}

export const WaterTracker: React.FC<WaterTrackerProps> = ({
  initialMl = 1750,
  targetMl = 2500,
  onUpdate,
}) => {
  const [waterMl, setWaterMl] = useState(initialMl);

  const handleAdd = (amount: number) => {
    const next = Math.max(0, waterMl + amount);
    setWaterMl(next);
    onUpdate?.(next);
  };

  const percentage = Math.min(100, Math.round((waterMl / targetMl) * 100));

  return (
    <div className="p-5 rounded-2xl glass-card border border-slate-800 space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 text-cyan-400 font-bold text-sm">
          <Droplet className="h-5 w-5 fill-cyan-400/20" /> Daily Water Hydration
        </div>
        <span className="text-xs font-semibold text-cyan-400">{percentage}% Reached</span>
      </div>

      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-2xl font-extrabold text-white">{waterMl} <span className="text-xs font-normal text-slate-400">ml</span></p>
          <p className="text-xs text-slate-500">Goal: {targetMl} ml ({Math.round(targetMl / 250)} cups)</p>
        </div>

        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={() => handleAdd(-250)}>
            <Minus className="h-4 w-4" />
          </Button>
          <Button size="sm" className="bg-cyan-600 hover:bg-cyan-500 text-white" onClick={() => handleAdd(250)}>
            <Plus className="h-4 w-4 mr-1" /> 250ml
          </Button>
        </div>
      </div>

      <div className="h-2 w-full bg-slate-900 rounded-full overflow-hidden border border-slate-800">
        <div className="h-full bg-cyan-500 transition-all duration-300" style={{ width: `${percentage}%` }} />
      </div>
    </div>
  );
};
