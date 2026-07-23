"use client";

import React, { useEffect, useState } from "react";
import { whatsappService } from "@/services/whatsapp.service";
import { WhatsAppSession, WebhookActivity, WhatsAppMessageLog } from "@/types/whatsapp";
import { DataTable, Column } from "@/components/data/DataTable";
import { StatsCard } from "@/components/ui/stats-card";
import { Badge } from "@/components/ui/badge";
import { Tabs } from "@/components/ui/tabs";
import { MessageSquare, ShieldCheck, Activity, Users, ArrowUpRight, ArrowDownLeft } from "lucide-react";

export default function WhatsAppPage() {
  const [activeTab, setActiveTab] = useState("sessions");
  const [sessions, setSessions] = useState<WhatsAppSession[]>([]);
  const [activities, setActivities] = useState<WebhookActivity[]>([]);
  const [logs, setLogs] = useState<WhatsAppMessageLog[]>([]);

  useEffect(() => {
    const load = async () => {
      const s = await whatsappService.getSessions();
      const a = await whatsappService.getWebhookActivities();
      const l = await whatsappService.getMessageLogs();
      setSessions(s);
      setActivities(a);
      setLogs(l);
    };
    load();
  }, []);

  const sessionColumns: Column<WhatsAppSession>[] = [
    { header: "User Name", accessorKey: "user_name", className: "font-semibold text-white", sortable: true },
    { header: "WhatsApp ID (wa_id)", accessorKey: "wa_id", className: "font-mono text-cyan-400" },
    { header: "Phone Number", accessorKey: "phone_number" },
    {
      header: "Onboarding State",
      cell: (item) => (
        <Badge variant={item.onboarding_state === "COMPLETE" ? "success" : "warning"}>
          {item.onboarding_state}
        </Badge>
      ),
    },
    { header: "Messages Count", accessorKey: "message_count", className: "text-emerald-400 font-bold" },
    { header: "Last Activity", cell: (item) => new Date(item.last_interaction).toLocaleString() },
  ];

  const activityColumns: Column<WebhookActivity>[] = [
    { header: "Meta Message ID", accessorKey: "message_id", className: "font-mono text-xs text-slate-400" },
    { header: "Sender WA ID", accessorKey: "sender_wa_id", className: "font-mono text-cyan-400" },
    { header: "Event Field", accessorKey: "event_type" },
    { header: "Received Time", cell: (item) => new Date(item.timestamp).toLocaleString() },
    {
      header: "Signature Check",
      cell: (item) => (
        <Badge variant={item.status === "processed" ? "success" : "error"}>
          {item.status === "processed" ? "HMAC SHA256 OK" : "FAILED"}
        </Badge>
      ),
    },
  ];

  const logColumns: Column<WhatsAppMessageLog>[] = [
    {
      header: "Direction",
      cell: (item) => (
        <span className="flex items-center gap-1 font-semibold">
          {item.direction === "inbound" ? (
            <ArrowDownLeft className="h-4 w-4 text-emerald-400" />
          ) : (
            <ArrowUpRight className="h-4 w-4 text-cyan-400" />
          )}
          {item.direction.toUpperCase()}
        </span>
      ),
    },
    { header: "Sender WA ID", accessorKey: "wa_id", className: "font-mono text-cyan-400" },
    { header: "Message Body", accessorKey: "body", className: "text-slate-200" },
    { header: "Type", accessorKey: "message_type" },
    { header: "Timestamp", cell: (item) => new Date(item.timestamp).toLocaleTimeString() },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between p-6 rounded-2xl glass-card border border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <MessageSquare className="h-6 w-6 text-emerald-400" /> Meta WhatsApp Cloud API Integration
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Real-time webhook events status, HMAC SHA-256 signature verification, and onboarding state machine sessions.
          </p>
        </div>
        <Badge variant="success">Webhook Active</Badge>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <StatsCard title="Active Onboarding Sessions" value={`${sessions.length} Users`} icon={Users} iconColor="text-emerald-400" />
        <StatsCard title="Webhook Requests Today" value="1,840" subtitle="0 Failures" icon={Activity} iconColor="text-cyan-400" />
        <StatsCard title="HMAC Signature Verification" value="100 %" subtitle="SHA-256 Validated" icon={ShieldCheck} iconColor="text-purple-400" />
      </div>

      <Tabs
        tabs={[
          { id: "sessions", label: "Active State Sessions", icon: Users },
          { id: "activities", label: "Webhook Diagnostics", icon: Activity },
          { id: "logs", label: "Message Logs", icon: MessageSquare },
        ]}
        activeTab={activeTab}
        onChange={setActiveTab}
      />

      {activeTab === "sessions" && (
        <DataTable title="WhatsApp User Onboarding State Sessions" columns={sessionColumns} data={sessions} keyExtractor={(s) => s.id} />
      )}
      {activeTab === "activities" && (
        <DataTable title="Meta Webhook Security & Execution Logs" columns={activityColumns} data={activities} keyExtractor={(a) => a.id} />
      )}
      {activeTab === "logs" && (
        <DataTable title="Inbound & Outbound WhatsApp Messages" columns={logColumns} data={logs} keyExtractor={(l) => l.id} />
      )}
    </div>
  );
}
