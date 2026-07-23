"use client";

import React from "react";
import { Meal } from "@/types/meal";
import { Badge } from "../ui/badge";
import { Flame, Clock, MoreVertical } from "lucide-react";
import Image from "next/image";

export interface MealCardProps {
  meal: Meal;
  onEdit?: (meal: Meal) => void;
  onDelete?: (mealId: string) => void;
}

export const MealCard: React.FC<MealCardProps> = ({ meal, onEdit, onDelete }) => {
  return (
    <div className="p-4 rounded-xl glass-card border border-slate-800 flex items-center justify-between gap-4 hover:border-slate-700 transition-colors">
      <div className="flex items-center gap-4 min-w-0">
        {meal.image_url ? (
          <div className="relative h-14 w-14 rounded-lg overflow-hidden flex-shrink-0 border border-slate-700">
            <Image src={meal.image_url} alt={meal.meal_name} fill className="object-cover" />
          </div>
        ) : (
          <div className="h-14 w-14 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 flex-shrink-0">
            <Flame className="h-6 w-6" />
          </div>
        )}

        <div className="min-w-0 space-y-1">
          <div className="flex items-center gap-2">
            <h4 className="text-sm font-bold text-white truncate">{meal.meal_name}</h4>
            <Badge variant="info" className="capitalize text-[10px]">
              {meal.meal_type || "Meal"}
            </Badge>
          </div>

          <div className="flex items-center gap-3 text-xs text-slate-400">
            <span className="flex items-center gap-1 font-semibold text-amber-400">
              <Flame className="h-3.5 w-3.5" /> {meal.calories} kcal
            </span>
            <span>P: {meal.protein}g</span>
            <span>C: {meal.carbs}g</span>
            <span>F: {meal.fat}g</span>
          </div>

          <p className="text-[10px] text-slate-500 flex items-center gap-1">
            <Clock className="h-3 w-3" /> {new Date(meal.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
            <span className="ml-2 uppercase text-emerald-400 font-medium">via {meal.source || "manual"}</span>
          </p>
        </div>
      </div>

      {(onEdit || onDelete) && (
        <div className="flex items-center gap-2">
          {onEdit && (
            <button onClick={() => onEdit(meal)} className="text-xs text-slate-400 hover:text-white p-1">
              Edit
            </button>
          )}
          {onDelete && (
            <button onClick={() => onDelete(meal.id)} className="text-xs text-rose-400 hover:text-rose-300 p-1">
              Delete
            </button>
          )}
        </div>
      )}
    </div>
  );
};
