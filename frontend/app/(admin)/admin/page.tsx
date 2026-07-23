"use client";

import React from "react";
import { StatsCard } from "@/components/ui/stats-card";
import { Table, Column } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { ShieldCheck, Users, Server, Database, Activity } from "lucide-react";

interface SystemServiceStatus {
  service: string;
  type: string;
  status: "healthy" | "degraded" | "down";
  latency: string;
}

const services: SystemServiceStatus[] = [
  { service: "FastAPI Backend API", type: "REST Server", status: "healthy", latency: "18ms" },
  { service: "PostgreSQL Database", type: "Relational DB", status: "healthy", latency: "4ms" },
  { service: "Redis Cache Cluster", type: "Session & Limits", status: "healthy", latency: "1ms" },
  { service: "Celery Workers", type: "Background Queue", status: "healthy", latency: "42ms" },
  { service: "WhatsApp Cloud API", type: "Meta Webhook", status: "healthy", latency: "120ms" },
  { service: "Gemini AI Engine", type: "LLM Provider", status: "healthy", latency: "380ms" },
];

export default function AdminPage() {
  const columns: Column<SystemServiceStatus>[] = [
    { header: "Service Name", accessorKey: "service", className: "font-semibold text-white" },
    { header: "Infrastructure Layer", accessorKey: "type" },
    {
      header: "Status",
      cell: (item) => (
        <Badge variant={item.status === "healthy" ? "success" : "error"}>
          {item.status.toUpperCase()}
        </Badge>
      ),
    },
    { header: "Response Latency", accessorKey: "latency", className: "text-emerald-400 font-mono" },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between p-6 rounded-2xl glass-card border border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <ShieldCheck className="h-6 w-6 text-emerald-400" /> Admin Control Operations
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            System status monitoring, user management, and API worker health telemetry.
          </p>
        </div>
        <Badge variant="info" className="px-3 py-1">SuperAdmin Access</Badge>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatsCard title="Total Registered Users" value="1,248" trend={{ value: "+12 today", isPositive: true }} icon={Users} />
        <StatsCard title="Backend Uptime SLA" value="99.98 %" trend={{ value: "Target 99.9%", isPositive: true }} icon={Server} iconColor="text-cyan-400" />
        <StatsCard title="Database Connections" value="14 / 100" subtitle="Pool Healthy" icon={Database} iconColor="text-purple-400" />
        <StatsCard title="Webhook Requests" value="18,420" trend={{ value: "0 Failed", isPositive: true }} icon={Activity} iconColor="text-emerald-400" />
      </div>

      <div className="space-y-3">
        <h3 className="text-sm font-semibold text-slate-300">Infrastructure Services Health</h3>
        <Table columns={columns} data={services} keyExtractor={(s) => s.service} />
      </div>
    </div>
  );
}
