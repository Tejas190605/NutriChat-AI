"use client";

import React, { useState } from "react";
import { Bell } from "lucide-react";
import { Dropdown } from "../ui/dropdown";

export const NotificationCenter: React.FC = () => {
  const [unreadCount] = useState(2);

  const notificationItems = [
    {
      id: "1",
      label: "🎉 Daily Calorie Target Achieved!",
      onClick: () => {},
    },
    {
      id: "2",
      label: "⚠️ Weight Plateau Detected: Check Coaching",
      onClick: () => {},
    },
  ];

  return (
    <Dropdown
      trigger={
        <button className="relative rounded-lg border border-slate-800 bg-slate-900/80 p-2 text-slate-400 hover:text-white transition-colors cursor-pointer">
          <Bell className="h-4 w-4" />
          {unreadCount > 0 && (
            <span className="absolute -top-1 -right-1 flex h-4 w-4 items-center justify-center rounded-full bg-emerald-500 text-[10px] font-bold text-white shadow-glow">
              {unreadCount}
            </span>
          )}
        </button>
      }
      items={notificationItems}
    />
  );
};
