import React from "react";
import { Scale, TrendingDown } from "lucide-react";
import { Button } from "../ui/button";

export interface WeightCardProps {
  currentWeight: number;
  targetWeight: number;
  weeklyDelta?: string;
  onLogWeight?: () => void;
}

export const WeightCard: React.FC<WeightCardProps> = ({
  currentWeight,
  targetWeight,
  weeklyDelta = "-0.4 kg this week",
  onLogWeight,
}) => {
  return (
    <div className="p-5 rounded-2xl glass-card border border-slate-800 space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 text-emerald-400 font-bold text-sm">
          <Scale className="h-5 w-5" /> Weight Progress
        </div>
        <span className="inline-flex items-center gap-1 text-xs text-emerald-400 font-medium">
          <TrendingDown className="h-3.5 w-3.5" /> {weeklyDelta}
        </span>
      </div>

      <div className="flex items-center justify-between">
        <div>
          <p className="text-2xl font-extrabold text-white">{currentWeight} <span className="text-xs font-normal text-slate-400">kg</span></p>
          <p className="text-xs text-slate-500">Target Goal: {targetWeight} kg</p>
        </div>

        {onLogWeight && (
          <Button variant="outline" size="sm" onClick={onLogWeight}>
            Update Weight
          </Button>
        )}
      </div>
    </div>
  );
};
