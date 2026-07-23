"use client";

import React, { useEffect, useState } from "react";
import { analyticsService, WeightTrajectoryPoint } from "@/services/analytics.service";
import { WeightPredictionChart } from "@/components/charts/WeightPredictionChart";
import { CalorieTrendChart } from "@/components/charts/CalorieTrendChart";
import { StatsCard } from "@/components/ui/stats-card";
import { AchievementCard } from "@/components/user/AchievementCard";
import { Card } from "@/components/ui/card";
import { TrendingUp, Scale, HeartPulse, Flame, Award, Calendar } from "lucide-react";

export default function ProgressPage() {
  const [predictions, setPredictions] = useState<WeightTrajectoryPoint[]>([]);

  useEffect(() => {
    analyticsService.getWeightPredictions().then(setPredictions);
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

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between p-6 rounded-2xl glass-card border border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <TrendingUp className="h-6 w-6 text-emerald-400" /> Goal Progress & Body Metrics
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Track weight trends, caloric deficit trajectory, body measurements history, and milestone badges.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <StatsCard title="Current Weight" value="74.2 kg" subtitle="Goal: 70.0 kg (-4.2 kg left)" icon={Scale} iconColor="text-emerald-400" />
        <StatsCard title="US Navy Body Fat" value="18.5 %" subtitle="-0.2% this week" icon={HeartPulse} iconColor="text-cyan-400" />
        <StatsCard title="Average Weekly Deficit" value="380 kcal / day" subtitle="Target 350-500 kcal" icon={Flame} iconColor="text-amber-400" />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <WeightPredictionChart data={predictions} />
        <CalorieTrendChart data={sampleCalorieData} />
      </div>

      {/* Body Measurements & Badges Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Measurements Log */}
        <Card className="p-5 border border-slate-800 space-y-4">
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <Calendar className="h-5 w-5 text-cyan-400" /> Body Measurements Log History
          </h3>
          <div className="space-y-2 text-xs">
            <div className="flex justify-between py-2 border-b border-slate-800 text-slate-300">
              <span>Waist Circumference</span>
              <strong className="text-white">82 cm (-1.5 cm)</strong>
            </div>
            <div className="flex justify-between py-2 border-b border-slate-800 text-slate-300">
              <span>Chest Circumference</span>
              <strong className="text-white">98 cm</strong>
            </div>
            <div className="flex justify-between py-2 border-b border-slate-800 text-slate-300">
              <span>Hips Circumference</span>
              <strong className="text-white">95 cm</strong>
            </div>
            <div className="flex justify-between py-2 text-slate-300">
              <span>Neck Circumference</span>
              <strong className="text-white">38 cm</strong>
            </div>
          </div>
        </Card>

        {/* Milestone Badges */}
        <div className="space-y-3">
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <Award className="h-5 w-5 text-amber-400" /> Earned Milestones & Badges
          </h3>
          <AchievementCard title="14-Day Tracking Streak" description="Logged meals every day for 14 days" unlocked={true} unlockedAt="July 20, 2026" />
          <AchievementCard title="Protein Master" description="Reached 150g+ protein target for 5 days in a row" unlocked={true} unlockedAt="July 22, 2026" />
        </div>
      </div>
    </div>
  );
}
