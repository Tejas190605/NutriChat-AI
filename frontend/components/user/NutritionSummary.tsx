import React from "react";
import { Flame, Activity, Zap, Layers } from "lucide-react";
import { MacroProgress } from "./MacroProgress";

export interface NutritionSummaryProps {
  calories: number;
  targetCalories: number;
  protein: number;
  targetProtein: number;
  carbs: number;
  targetCarbs: number;
  fat: number;
  targetFat: number;
}

export const NutritionSummary: React.FC<NutritionSummaryProps> = ({
  calories,
  targetCalories,
  protein,
  targetProtein,
  carbs,
  targetCarbs,
  fat,
  targetFat,
}) => {
  return (
    <div className="p-5 rounded-2xl glass-card border border-slate-800 space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-bold text-white flex items-center gap-2">
          <Flame className="h-5 w-5 text-amber-400" /> Daily Macro Budget Overview
        </h3>
        <span className="text-xs font-bold text-amber-400">
          {calories} / {targetCalories} kcal
        </span>
      </div>

      <div className="space-y-3">
        <MacroProgress label="Protein" current={protein} target={targetProtein} color="emerald" />
        <MacroProgress label="Carbohydrates" current={carbs} target={targetCarbs} color="cyan" />
        <MacroProgress label="Fats" current={fat} target={targetFat} color="purple" />
      </div>
    </div>
  );
};
