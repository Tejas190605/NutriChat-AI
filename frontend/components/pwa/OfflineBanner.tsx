"use client";

import React, { useEffect, useState } from "react";
import { WifiOff, RefreshCw } from "lucide-react";
import { NutriChatOfflineDB } from "@/lib/offline/indexeddb";

export const OfflineBanner: React.FC = () => {
  const [isOffline, setIsOffline] = useState(false);
  const [pendingCount, setPendingCount] = useState(0);

  useEffect(() => {
    const handleOnline = () => setIsOffline(false);
    const handleOffline = () => {
      setIsOffline(true);
      NutriChatOfflineDB.getPendingMutations().then((m) => setPendingCount(m.length));
    };

    if (typeof window !== "undefined") {
      setIsOffline(!navigator.onLine);
      window.addEventListener("online", handleOnline);
      window.addEventListener("offline", handleOffline);
    }

    return () => {
      if (typeof window !== "undefined") {
        window.removeEventListener("online", handleOnline);
        window.removeEventListener("offline", handleOffline);
      }
    };
  }, []);

  if (!isOffline) return null;

  return (
    <div className="bg-amber-500/20 border-b border-amber-500/30 text-amber-200 px-4 py-2 text-xs flex items-center justify-between z-50">
      <div className="flex items-center gap-2 font-medium">
        <WifiOff className="h-4 w-4 text-amber-400" />
        <span>Device Offline. Working in offline mode.</span>
      </div>
      {pendingCount > 0 && (
        <span className="text-[11px] font-semibold bg-amber-950/60 px-2 py-0.5 rounded-md text-amber-300">
          {pendingCount} Pending Sync Queue
        </span>
      )}
    </div>
  );
};
