"use client";

import React, { useEffect, useState } from "react";
import { StatsCard } from "@/components/ui/stats-card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { CalorieTrendChart } from "@/components/charts/CalorieTrendChart";
import { MacroBreakdownChart } from "@/components/charts/MacroBreakdownChart";
import { DataTable, Column } from "@/components/data/DataTable";
import { mealsService } from "@/services/meals.service";
import { Meal } from "@/types/meal";
import { Activity, Flame, Scale, HeartPulse, BrainCircuit, MessageSquare, Zap, Plus, RefreshCw } from "lucide-react";

export default function DashboardOverviewPage() {
  const [meals, setMeals] = useState<Meal[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchMeals = async () => {
    setLoading(true);
    try {
      const data = await mealsService.getMeals();
      setMeals(data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMeals();
  }, []);

  const sampleCalorieData = [
    { day: "Mon", calories: 2100 },
    { day: "Tue", calories: 1950 },
    { day: "Wed", calories: 2200 },
    { day: "Thu", calories: 1850 },
    { day: "Fri", calories: 2050 },
    { day: "Sat", calories: 2300 },
    { day: "Sun", calories: 1980 },
  ];

  const mealColumns: Column<Meal>[] = [
    { header: "Meal Name", accessorKey: "meal_name", className: "font-semibold text-white", sortable: true },
    {
      header: "Category",
      cell: (item) => (
        <Badge variant="info" className="capitalize">
          {item.meal_type || "Meal"}
        </Badge>
      ),
    },
    { header: "Calories", accessorKey: "calories", className: "text-amber-400 font-bold", sortable: true },
    { header: "Protein (g)", accessorKey: "protein", sortable: true },
    { header: "Carbs (g)", accessorKey: "carbs" },
    { header: "Fat (g)", accessorKey: "fat" },
    {
      header: "Source",
      cell: (item) => (
        <Badge variant={item.source === "whatsapp" ? "success" : "warning"}>
          {item.source || "Manual"}
        </Badge>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header & Quick Actions */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-6 rounded-2xl glass-card border border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Zap className="h-6 w-6 text-emerald-400" /> Autonomous Health & Nutrition Overview
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Live compliance tracking, weight forecasting, AI coaching engine, and Meta WhatsApp integration telemetry.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" size="sm" onClick={fetchMeals} isLoading={loading}>
            <RefreshCw className="h-4 w-4 mr-1.5" /> Refresh
          </Button>
          <Button size="sm">
            <Plus className="h-4 w-4 mr-1.5" /> Quick Log Meal
          </Button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatsCard
          title="Daily Calories"
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

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <CalorieTrendChart data={sampleCalorieData} className="lg:col-span-2" />
        <MacroBreakdownChart protein={142} carbs={195} fat={58} />
      </div>

      {/* AI & WhatsApp Intelligence Panels */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="p-5 rounded-2xl glass-card border border-slate-800 space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <BrainCircuit className="h-5 w-5 text-emerald-400" /> AI Coach Recommendation
            </h3>
            <Badge variant="info">Plateau Risk: Low</Badge>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            &quot;Your protein intake has averaged 142g over the past 3 days. To accelerate lean muscle retention during your 350 kcal deficit, consider swapping evening snacks with Greek yogurt or a whey shake.&quot;
          </p>
          <div className="pt-2 text-[11px] text-slate-500">Model: Gemini 3.6 Flash | Latency: 320ms</div>
        </div>

        <div className="p-5 rounded-2xl glass-card border border-slate-800 space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <MessageSquare className="h-5 w-5 text-cyan-400" /> WhatsApp Cloud API Pipeline
            </h3>
            <Badge variant="success">Webhook Active</Badge>
          </div>
          <div className="space-y-2 text-xs text-slate-300">
            <div className="flex justify-between py-1 border-b border-slate-800">
              <span>Active Sessions:</span>
              <strong className="text-white">12 Users</strong>
            </div>
            <div className="flex justify-between py-1 border-b border-slate-800">
              <span>Messages Processed Today:</span>
              <strong className="text-white">142 Inbound</strong>
            </div>
            <div className="flex justify-between py-1">
              <span>HMAC SHA-256 Verification:</span>
              <span className="text-emerald-400 font-semibold">100% Passed</span>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Meals Table */}
      <DataTable
        title="Recent Meal Logs"
        columns={mealColumns}
        data={meals}
        keyExtractor={(m) => m.id}
        searchPlaceholder="Search recent meals..."
      />
    </div>
  );
}
