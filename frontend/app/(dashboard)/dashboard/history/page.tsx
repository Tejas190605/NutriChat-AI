"use client";

import React from "react";
import { Timeline, TimelineItem } from "@/components/user/Timeline";
import { History, Calendar } from "lucide-react";

const HISTORY_ITEMS: TimelineItem[] = [
  {
    id: "h-1",
    title: "Logged Lunch: Paneer Roll & Sprouted Salad",
    subtitle: "480 kcal | 24.5g P | 52g C | 16g F (via WhatsApp)",
    timestamp: "2026-07-23T14:22:00Z",
    type: "meal",
  },
  {
    id: "h-2",
    title: "AI Health Coach Consultation",
    subtitle: "Recommended swapping evening snacks to Greek yogurt to boost protein intake.",
    timestamp: "2026-07-23T12:00:00Z",
    type: "coaching",
  },
  {
    id: "h-3",
    title: "Logged Breakfast: Oatmeal with Almonds",
    subtitle: "360 kcal | 12g P | 58g C | 8.5g F (via Manual Logger)",
    timestamp: "2026-07-23T08:30:00Z",
    type: "meal",
  },
  {
    id: "h-4",
    title: "Updated Weight Measurement",
    subtitle: "74.2 kg logged (-0.4 kg from previous week)",
    timestamp: "2026-07-22T07:15:00Z",
    type: "weight",
  },
];

export default function HistoryPage() {
  return (
    <div className="space-y-6 max-w-4xl">
      <div className="flex items-center justify-between p-6 rounded-2xl glass-card border border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <History className="h-6 w-6 text-emerald-400" /> Chronological Activity Audit History
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Audit log timeline of all meal entries, AI consultations, and body weight logs.
          </p>
        </div>
      </div>

      <div className="p-6 rounded-2xl glass-card border border-slate-800 space-y-4">
        <h3 className="text-sm font-bold text-white flex items-center gap-2 mb-4">
          <Calendar className="h-4 w-4 text-emerald-400" /> Recent Events Timeline
        </h3>
        <Timeline items={HISTORY_ITEMS} />
      </div>
    </div>
  );
}
