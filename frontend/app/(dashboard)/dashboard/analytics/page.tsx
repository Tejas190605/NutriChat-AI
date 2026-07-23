"use client";

import React, { useEffect, useState } from "react";
import { analyticsService, WeightTrajectoryPoint, HabitItem } from "@/services/analytics.service";
import { WeightPredictionChart } from "@/components/charts/WeightPredictionChart";
import { StatsCard } from "@/components/ui/stats-card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { LineChart, Activity, HeartPulse, Flame, Award, CheckCircle2 } from "lucide-react";

export default function AnalyticsPage() {
  const [predictions, setPredictions] = useState<WeightTrajectoryPoint[]>([]);
  const [habits, setHabits] = useState<HabitItem[]>([]);

  // US Navy Body Fat Calculator State
  const [waist, setWaist] = useState("82");
  const [neck, setNeck] = useState("38");
  const [height, setHeight] = useState("175");
  const [calculatedBf, setCalculatedBf] = useState<number | null>(18.2);

  useEffect(() => {
    const load = async () => {
      const p = await analyticsService.getWeightPredictions();
      const h = await analyticsService.getHabits();
      setPredictions(p);
      setHabits(h);
    };
    load();
  }, []);

  const calculateNavyBodyFat = () => {
    const w = Number(waist);
    const n = Number(neck);
    const h = Number(height);

    if (w > 0 && n > 0 && h > 0 && w > n) {
      // Male US Navy Body Fat Formula
      // 86.010 * log10(waist - neck) - 70.041 * log10(height) + 36.76
      const bf = 86.01 * Math.log10(w - n) - 70.041 * Math.log10(h) + 36.76;
      setCalculatedBf(Math.max(5, Math.min(50, Number(bf.toFixed(1)))));
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-6 rounded-2xl glass-card border border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <LineChart className="h-6 w-6 text-emerald-400" /> Analytics, Telemetry & Forecasting
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            US Navy Body Fat %, weight trend prediction trajectory, and habits adherence telemetry.
          </p>
        </div>
      </div>

      {/* KPI Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <StatsCard title="Current Weight" value="74.2 kg" subtitle="Goal: 70.0 kg" icon={Activity} iconColor="text-emerald-400" />
        <StatsCard title="US Navy Body Fat" value={`${calculatedBf || 18.2} %`} subtitle="Fitness Category" icon={HeartPulse} iconColor="text-cyan-400" />
        <StatsCard title="Weekly Deficit Average" value="380 kcal / day" subtitle="On Track" icon={Flame} iconColor="text-amber-400" />
      </div>

      {/* Trajectory Prediction Chart */}
      <WeightPredictionChart data={predictions} />

      {/* Body Fat Calculator & Habits Tracker */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* US Navy Calculator Card */}
        <Card className="p-5 border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <HeartPulse className="h-5 w-5 text-cyan-400" /> US Navy Body Fat % Estimator
            </h3>
            {calculatedBf && <Badge variant="success">{calculatedBf}% Body Fat</Badge>}
          </div>

          <div className="grid grid-cols-3 gap-3">
            <Input label="Waist (cm)" type="number" value={waist} onChange={(e) => setWaist(e.target.value)} />
            <Input label="Neck (cm)" type="number" value={neck} onChange={(e) => setNeck(e.target.value)} />
            <Input label="Height (cm)" type="number" value={height} onChange={(e) => setHeight(e.target.value)} />
          </div>

          <Button size="sm" className="w-full" onClick={calculateNavyBodyFat}>
            Calculate Body Fat %
          </Button>
        </Card>

        {/* Habits & Streaks */}
        <Card className="p-5 border border-slate-800 space-y-4">
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <Award className="h-5 w-5 text-amber-400" /> Daily Habits & Compliance Streaks
          </h3>
          <div className="space-y-3">
            {habits.map((habit) => (
              <div key={habit.id} className="flex items-center justify-between p-3 rounded-xl bg-slate-900/60 border border-slate-800">
                <div className="flex items-center gap-3">
                  <CheckCircle2 className={`h-5 w-5 ${habit.completed_today ? "text-emerald-400" : "text-slate-600"}`} />
                  <div>
                    <p className="text-xs font-semibold text-white">{habit.name}</p>
                    <p className="text-[11px] text-slate-400">{habit.streak} Days Active Streak</p>
                  </div>
                </div>
                <Badge variant={habit.completed_today ? "success" : "info"}>
                  {habit.completed_today ? "DONE TODAY" : "PENDING"}
                </Badge>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}
