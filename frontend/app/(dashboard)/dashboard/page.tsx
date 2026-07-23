"use client";

import React from "react";
import { StatsCard } from "@/components/ui/stats-card";
import { ChartCard } from "@/components/ui/chart-card";
import { Badge } from "@/components/ui/badge";
import { Activity, Flame, Scale, HeartPulse, BrainCircuit } from "lucide-react";
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip } from "recharts";

const sampleCalorieData = [
  { day: "Mon", calories: 2100 },
  { day: "Tue", calories: 1950 },
  { day: "Wed", calories: 2200 },
  { day: "Thu", calories: 1850 },
  { day: "Fri", calories: 2050 },
  { day: "Sat", calories: 2300 },
  { day: "Sun", calories: 1980 },
];

export default function DashboardOverviewPage() {
  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-6 rounded-2xl glass-card border border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-white">System Telemetry Overview</h2>
          <p className="text-xs text-slate-400 mt-1">
            Real-time compliance scores, weight forecasting, and AI WhatsApp message pipelines.
          </p>
        </div>
        <Badge variant="success" className="px-3 py-1 text-xs">
          Engine Healthy (0.1.9)
        </Badge>
      </div>

      {/* KPI Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatsCard
          title="Daily Calories Target"
          value="1,980 kcal"
          subtitle="Goal: 2,200 kcal"
          trend={{ value: "90% Goal", isPositive: true }}
          icon={Flame}
          iconColor="text-amber-400"
        />
        <StatsCard
          title="Current Weight"
          value="74.2 kg"
          subtitle="Target: 70.0 kg"
          trend={{ value: "-0.4 kg this wk", isPositive: true }}
          icon={Scale}
          iconColor="text-emerald-400"
        />
        <StatsCard
          title="US Navy Body Fat"
          value="18.5 %"
          subtitle="Category: Fitness"
          trend={{ value: "-0.2%", isPositive: true }}
          icon={HeartPulse}
          iconColor="text-cyan-400"
        />
        <StatsCard
          title="Adherence Score"
          value="94.2 %"
          subtitle="14 Days Active"
          trend={{ value: "+2.1%", isPositive: true }}
          icon={Activity}
          iconColor="text-purple-400"
        />
      </div>

      {/* Analytics Chart & AI Coaching Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <ChartCard
          title="Weekly Calorie Intake Trend"
          description="Daily caloric consumption over the last 7 days"
          className="lg:col-span-2"
        >
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={sampleCalorieData}>
              <defs>
                <linearGradient id="colorCalories" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.4} />
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                </linearGradient>
              </defs>
              <XAxis dataKey="day" stroke="#64748b" fontSize={12} tickLine={false} />
              <YAxis stroke="#64748b" fontSize={12} tickLine={false} />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#0f172a",
                  borderColor: "#1e293b",
                  borderRadius: "8px",
                  color: "#f8fafc",
                }}
              />
              <Area
                type="monotone"
                dataKey="calories"
                stroke="#10b981"
                strokeWidth={2}
                fillOpacity={1}
                fill="url(#colorCalories)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </ChartCard>

        {/* AI Insights Card */}
        <div className="p-5 rounded-xl glass-card border border-slate-800 flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 text-emerald-400 text-sm font-semibold mb-3">
              <BrainCircuit className="h-5 w-5" /> AI Coaching Intelligence
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              &quot;Your protein intake has averaged 142g over the past 3 days. To accelerate lean muscle retention during your 350 kcal deficit, consider swapping evening snacks with Greek yogurt or a whey shake.&quot;
            </p>
          </div>
          <div className="mt-6 pt-4 border-t border-slate-800 flex items-center justify-between text-xs">
            <span className="text-slate-500">Generated 2h ago</span>
            <Badge variant="info">Plateau Risk: Low</Badge>
          </div>
        </div>
      </div>
    </div>
  );
}
