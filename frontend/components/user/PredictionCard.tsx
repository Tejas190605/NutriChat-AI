import React from "react";
import { TrendingDown, Calendar, CheckCircle2 } from "lucide-react";
import { Badge } from "../ui/badge";

export interface PredictionCardProps {
  targetDate?: string;
  weeklyPaceKg?: number;
  projectedWeightKg?: number;
}

export const PredictionCard: React.FC<PredictionCardProps> = ({
  targetDate = "August 14, 2026",
  weeklyPaceKg = 0.4,
  projectedWeightKg = 70.0,
}) => {
  return (
    <div className="p-5 rounded-2xl glass-card border border-slate-800 space-y-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 text-cyan-400 font-bold text-sm">
          <TrendingDown className="h-5 w-5" /> Weight Target Forecast
        </div>
        <Badge variant="success">On Track</Badge>
      </div>

      <p className="text-xs text-slate-300">
        Based on your current 380 kcal average deficit, you are projected to reach <strong className="text-white">{projectedWeightKg} kg</strong> by:
      </p>

      <div className="p-3 rounded-xl bg-cyan-950/30 border border-cyan-800/40 flex items-center justify-between">
        <div className="flex items-center gap-2 text-cyan-300 font-bold text-sm">
          <Calendar className="h-4 w-4" /> {targetDate}
        </div>
        <span className="text-xs text-slate-400">Pace: ~{weeklyPaceKg} kg/wk</span>
      </div>
    </div>
  );
};
