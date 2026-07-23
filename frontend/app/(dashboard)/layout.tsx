"use client";

import React, { useEffect } from "react";
import { Sidebar } from "@/components/layout/sidebar";
import { Topbar } from "@/components/layout/topbar";
import { Breadcrumbs } from "@/components/layout/breadcrumbs";
import { BottomNavigation } from "@/components/layout/BottomNavigation";
import { OfflineBanner } from "@/components/pwa/OfflineBanner";
import { PwaInstallPrompt } from "@/components/pwa/PwaInstallPrompt";
import { registerServiceWorker } from "@/lib/pwa/sw-register";
import { SyncEngine } from "@/lib/offline/sync-engine";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    registerServiceWorker();
    SyncEngine.init();
  }, []);

  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 overflow-hidden flex-col">
      <OfflineBanner />
      <div className="flex flex-1 min-h-0 min-w-0 overflow-hidden">
        <div className="hidden sm:block">
          <Sidebar />
        </div>
        <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
          <Topbar />
          <main className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6 pb-24 sm:pb-6">
            <Breadcrumbs />
            {children}
          </main>
        </div>
      </div>
      <BottomNavigation />
      <PwaInstallPrompt />
    </div>
  );
}
