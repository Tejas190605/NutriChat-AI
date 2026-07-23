"use client";

import React, { useEffect, useState } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { mealsService } from "@/services/meals.service";
import { analyticsService } from "@/services/analytics.service";
import { Meal, DailyMealSummary } from "@/types/meal";
import { NutritionSummary } from "@/components/user/NutritionSummary";
import { WaterTracker } from "@/components/user/WaterTracker";
import { WeightCard } from "@/components/user/WeightCard";
import { MealCard } from "@/components/user/MealCard";
import { InsightCard } from "@/components/user/InsightCard";
import { AchievementCard } from "@/components/user/AchievementCard";
import { PredictionCard } from "@/components/user/PredictionCard";
import { Button } from "@/components/ui/button";
import { Modal } from "@/components/ui/modal";
import { Input } from "@/components/ui/input";
import { Sparkles, Plus, Camera, Flame, Award, Calendar } from "lucide-react";
import Link from "next/link";

export default function UserHomePage() {
  const { user } = useAuth();
  const [summary, setSummary] = useState<DailyMealSummary | null>(null);
  const [meals, setMeals] = useState<Meal[]>([]);
  const [isQuickLogOpen, setIsQuickLogOpen] = useState(false);

  const [mealName, setMealName] = useState("");
  const [calories, setCalories] = useState("");
  const [protein, setProtein] = useState("");

  useEffect(() => {
    const load = async () => {
      const s = await mealsService.getDailySummary();
      const m = await mealsService.getMeals();
      setSummary(s);
      setMeals(m);
    };
    load();
  }, []);

  const handleQuickLog = (e: React.FormEvent) => {
    e.preventDefault();
    const newMeal: Meal = {
      id: `m-quick-${Date.now()}`,
      meal_name: mealName,
      meal_type: "snack",
      timestamp: new Date().toISOString(),
      calories: Number(calories) || 250,
      protein: Number(protein) || 15,
      carbs: 25,
      fat: 8,
      source: "manual",
    };
    setMeals([newMeal, ...meals]);
    setIsQuickLogOpen(false);
    setMealName("");
    setCalories("");
    setProtein("");
  };

  return (
    <div className="space-y-6">
      {/* Welcome Banner */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-6 rounded-2xl glass-card border border-slate-800">
        <div>
          <h2 className="text-2xl font-extrabold text-white">
            Welcome back, <span className="bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">{user?.full_name || "Tejas"}</span> 👋
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            You are on a <strong className="text-emerald-400">14-day tracking streak</strong>. You have 220 kcal remaining today.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Link href="/dashboard/meal-analysis">
            <Button variant="outline" size="sm">
              <Camera className="h-4 w-4 mr-1.5" /> AI Meal Analysis
            </Button>
          </Link>
          <Button size="sm" onClick={() => setIsQuickLogOpen(true)}>
            <Plus className="h-4 w-4 mr-1.5" /> Log Meal
          </Button>
        </div>
      </div>

      {/* Daily Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <NutritionSummary
          calories={summary?.total_calories || 1980}
          targetCalories={summary?.target_calories || 2200}
          protein={summary?.total_protein || 142}
          targetProtein={summary?.target_protein || 160}
          carbs={summary?.total_carbs || 195}
          targetCarbs={summary?.target_carbs || 220}
          fat={summary?.total_fat || 58}
          targetFat={summary?.target_fat || 65}
        />
        <WaterTracker initialMl={1750} targetMl={2500} />
        <WeightCard currentWeight={74.2} targetWeight={70.0} />
      </div>

      {/* AI Coaching & Trajectory Forecast */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <InsightCard
          content="Your protein intake has averaged 142g over the past 3 days. To accelerate lean muscle retention during your 350 kcal deficit, consider swapping evening snacks with Greek yogurt or a whey shake."
          plateauRisk="Low"
        />
        <PredictionCard targetDate="August 14, 2026" weeklyPaceKg={0.4} projectedWeightKg={70.0} />
      </div>

      {/* Today's Meals Timeline & Achievements */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <Flame className="h-5 w-5 text-amber-400" /> Today&apos;s Logged Meals
            </h3>
            <Link href="/dashboard/meals" className="text-xs text-emerald-400 hover:underline">
              View All History →
            </Link>
          </div>

          <div className="space-y-3">
            {meals.slice(0, 3).map((meal) => (
              <MealCard key={meal.id} meal={meal} />
            ))}
          </div>
        </div>

        {/* Badges & Reminders */}
        <div className="space-y-4">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Award className="h-5 w-5 text-amber-400" /> Streaks & Milestones
          </h3>
          <AchievementCard
            title="14-Day Tracking Streak"
            description="Logged every single meal for 14 consecutive days"
            unlocked={true}
            unlockedAt="July 20, 2026"
          />
          <AchievementCard
            title="Protein Master"
            description="Reached 150g+ protein target for 5 days in a row"
            unlocked={true}
            unlockedAt="July 22, 2026"
          />
          <AchievementCard
            title="Hydration Champion"
            description="Reached 2.5L water goal for 7 days"
            unlocked={false}
          />
        </div>
      </div>

      {/* Quick Log Modal */}
      <Modal isOpen={isQuickLogOpen} onClose={() => setIsQuickLogOpen(false)} title="Quick Log Meal Entry">
        <form onSubmit={handleQuickLog} className="space-y-4">
          <Input label="Meal Name" placeholder="e.g., Protein Bar & Coffee" value={mealName} onChange={(e) => setMealName(e.target.value)} required />
          <Input label="Calories (kcal)" type="number" placeholder="250" value={calories} onChange={(e) => setCalories(e.target.value)} required />
          <Input label="Protein (g)" type="number" placeholder="20" value={protein} onChange={(e) => setProtein(e.target.value)} required />
          <div className="flex justify-end gap-3 pt-3">
            <Button type="button" variant="outline" onClick={() => setIsQuickLogOpen(false)}>Cancel</Button>
            <Button type="submit">Log Entry</Button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
