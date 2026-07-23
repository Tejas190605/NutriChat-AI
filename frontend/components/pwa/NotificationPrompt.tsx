"use client";

import React, { useState } from "react";
import { Bell, Check } from "lucide-react";
import { requestNotificationPermission } from "@/lib/notifications/vapid";
import { Button } from "../ui/button";

export const NotificationPrompt: React.FC = () => {
  const [granted, setGranted] = useState(false);

  const handleEnable = async () => {
    const isGranted = await requestNotificationPermission();
    setGranted(isGranted);
  };

  if (granted) return null;

  return (
    <div className="p-4 rounded-xl glass-card border border-slate-800 flex items-center justify-between gap-4">
      <div className="flex items-center gap-3">
        <div className="p-2 rounded-xl bg-cyan-500/20 text-cyan-400">
          <Bell className="h-5 w-5" />
        </div>
        <div>
          <h4 className="text-xs font-bold text-white">Enable Push Reminders</h4>
          <p className="text-[11px] text-slate-400">Get daily meal, water & AI coach updates</p>
        </div>
      </div>
      <Button variant="outline" size="sm" onClick={handleEnable}>
        Enable
      </Button>
    </div>
  );
};
