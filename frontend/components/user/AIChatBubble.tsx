import React from "react";
import { Sparkles, User as UserIcon } from "lucide-react";
import { clsx } from "clsx";

export interface AIChatBubbleProps {
  role: "user" | "assistant" | "system";
  content: string;
  timestamp?: string;
  latencyMs?: number;
}

export const AIChatBubble: React.FC<AIChatBubbleProps> = ({
  role,
  content,
  timestamp,
  latencyMs,
}) => {
  const isUser = role === "user";

  return (
    <div className={clsx("flex items-start gap-3 my-3", isUser ? "flex-row-reverse" : "flex-row")}>
      <div
        className={clsx(
          "h-8 w-8 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 mt-1 shadow-sm",
          isUser ? "bg-emerald-600 text-white" : "bg-gradient-to-tr from-emerald-500 to-cyan-500 text-white"
        )}
      >
        {isUser ? <UserIcon className="h-4 w-4" /> : <Sparkles className="h-4 w-4" />}
      </div>

      <div className={clsx("max-w-md space-y-1", isUser ? "items-end text-right" : "items-start")}>
        <div
          className={clsx(
            "p-4 rounded-2xl text-xs leading-relaxed border shadow-sm",
            isUser
              ? "bg-emerald-600/20 border-emerald-500/30 text-emerald-100 rounded-tr-none"
              : "bg-slate-900 border-slate-800 text-slate-200 rounded-tl-none"
          )}
        >
          {content}
        </div>

        <div className="flex items-center gap-2 text-[10px] text-slate-500 px-1">
          {timestamp && <span>{new Date(timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</span>}
          {latencyMs && <span>• Gemini 3.6 Flash ({latencyMs}ms)</span>}
        </div>
      </div>
    </div>
  );
};
