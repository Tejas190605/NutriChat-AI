import React from "react";
import { Target, Edit2 } from "lucide-react";

export interface GoalCardProps {
  title: string;
  value: string | number;
  unit?: string;
  description?: string;
  onEdit?: () => void;
}

export const GoalCard: React.FC<GoalCardProps> = ({
  title,
  value,
  unit,
  description,
  onEdit,
}) => {
  return (
    <div className="p-4 rounded-xl glass-card border border-slate-800 flex items-center justify-between gap-4">
      <div className="flex items-center gap-3">
        <div className="p-2.5 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          <Target className="h-5 w-5" />
        </div>
        <div>
          <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">{title}</h4>
          <p className="text-lg font-extrabold text-white">
            {value} {unit && <span className="text-xs font-normal text-slate-400">{unit}</span>}
          </p>
          {description && <p className="text-[11px] text-slate-500">{description}</p>}
        </div>
      </div>

      {onEdit && (
        <button onClick={onEdit} className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors">
          <Edit2 className="h-4 w-4" />
        </button>
      )}
    </div>
  );
};
