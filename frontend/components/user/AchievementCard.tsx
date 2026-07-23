import React from "react";
import { Award, CheckCircle2, Lock } from "lucide-react";
import { clsx } from "clsx";

export interface AchievementCardProps {
  title: string;
  description: string;
  unlocked: boolean;
  unlockedAt?: string;
  icon?: React.FC<{ className?: string }>;
}

export const AchievementCard: React.FC<AchievementCardProps> = ({
  title,
  description,
  unlocked,
  unlockedAt,
  icon: Icon = Award,
}) => {
  return (
    <div
      className={clsx(
        "p-4 rounded-xl border transition-all flex items-start gap-3.5",
        unlocked
          ? "bg-emerald-950/20 border-emerald-800/40 text-slate-200 shadow-sm"
          : "bg-slate-900/40 border-slate-800/60 opacity-60"
      )}
    >
      <div
        className={clsx(
          "p-2.5 rounded-xl flex-shrink-0 mt-0.5",
          unlocked ? "bg-emerald-500/20 text-emerald-400" : "bg-slate-800 text-slate-500"
        )}
      >
        <Icon className="h-5 w-5" />
      </div>

      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between gap-2">
          <h4 className="text-xs font-bold text-white truncate">{title}</h4>
          {unlocked ? (
            <span className="text-[10px] text-emerald-400 font-semibold flex items-center gap-1">
              <CheckCircle2 className="h-3 w-3" /> Unlocked
            </span>
          ) : (
            <span className="text-[10px] text-slate-500 flex items-center gap-1">
              <Lock className="h-3 w-3" /> Locked
            </span>
          )}
        </div>
        <p className="text-[11px] text-slate-400 mt-1">{description}</p>
        {unlockedAt && <p className="text-[10px] text-slate-500 mt-1">Earned on {unlockedAt}</p>}
      </div>
    </div>
  );
};
