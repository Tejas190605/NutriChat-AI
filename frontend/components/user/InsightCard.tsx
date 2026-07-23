import React from "react";
import { BrainCircuit, ThumbsUp, ThumbsDown } from "lucide-react";
import { Badge } from "../ui/badge";

export interface InsightCardProps {
  title?: string;
  content: string;
  plateauRisk?: "Low" | "Moderate" | "High";
  onFeedback?: (type: "like" | "dislike") => void;
}

export const InsightCard: React.FC<InsightCardProps> = ({
  title = "AI Health Coach Insight",
  content,
  plateauRisk = "Low",
  onFeedback,
}) => {
  return (
    <div className="p-5 rounded-2xl glass-card border border-slate-800 space-y-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 text-emerald-400 font-bold text-sm">
          <BrainCircuit className="h-5 w-5" /> {title}
        </div>
        <Badge variant={plateauRisk === "Low" ? "success" : "warning"}>
          Plateau Risk: {plateauRisk}
        </Badge>
      </div>

      <p className="text-xs text-slate-300 leading-relaxed font-normal">
        &quot;{content}&quot;
      </p>

      {onFeedback && (
        <div className="pt-2 border-t border-slate-800 flex items-center justify-between text-[11px] text-slate-500">
          <span>Was this tip helpful?</span>
          <div className="flex items-center gap-2">
            <button onClick={() => onFeedback("like")} className="p-1 hover:text-emerald-400 transition-colors">
              <ThumbsUp className="h-3.5 w-3.5" />
            </button>
            <button onClick={() => onFeedback("dislike")} className="p-1 hover:text-rose-400 transition-colors">
              <ThumbsDown className="h-3.5 w-3.5" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
