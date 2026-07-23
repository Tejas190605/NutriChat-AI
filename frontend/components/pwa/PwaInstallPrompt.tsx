"use client";

import React, { useEffect, useState } from "react";
import { Download, X } from "lucide-react";
import { Button } from "../ui/button";

export const PwaInstallPrompt: React.FC = () => {
  const [deferredPrompt, setDeferredPrompt] = useState<any>(null);
  const [showPrompt, setShowPrompt] = useState(false);

  useEffect(() => {
    const handleBeforeInstall = (e: Event) => {
      e.preventDefault();
      setDeferredPrompt(e);
      setShowPrompt(true);
    };

    window.addEventListener("beforeinstallprompt", handleBeforeInstall);
    return () => window.removeEventListener("beforeinstallprompt", handleBeforeInstall);
  }, []);

  const handleInstall = async () => {
    if (!deferredPrompt) return;
    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;
    if (outcome === "accepted") {
      setShowPrompt(false);
    }
    setDeferredPrompt(null);
  };

  if (!showPrompt) return null;

  return (
    <div className="fixed bottom-20 sm:bottom-6 left-4 right-4 sm:left-auto sm:right-6 max-w-sm z-50 p-4 rounded-2xl glass-card border border-emerald-500/30 shadow-glass animate-in slide-in-from-bottom-5 duration-300 flex items-center justify-between gap-3">
      <div className="flex items-center gap-3">
        <div className="p-2 rounded-xl bg-emerald-500/20 text-emerald-400">
          <Download className="h-5 w-5" />
        </div>
        <div>
          <h4 className="text-xs font-bold text-white">Install NutriChat AI</h4>
          <p className="text-[11px] text-slate-400">Add app to Home Screen for fast offline access</p>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <Button size="sm" onClick={handleInstall}>
          Install
        </Button>
        <button onClick={() => setShowPrompt(false)} className="text-slate-500 hover:text-slate-300 p-1">
          <X className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
};
