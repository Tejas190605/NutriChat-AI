"use client";

import React, { useEffect, useState } from "react";
import { mealsService } from "@/services/meals.service";
import { Meal, DailyMealSummary } from "@/types/meal";
import { DataTable, Column } from "@/components/data/DataTable";
import { StatsCard } from "@/components/ui/stats-card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Modal } from "@/components/ui/modal";
import { Input } from "@/components/ui/input";
import { Utensils, Plus, Flame, Activity, Calendar } from "lucide-react";

export default function MealsPage() {
  const [meals, setMeals] = useState<Meal[]>([]);
  const [summary, setSummary] = useState<DailyMealSummary | null>(null);
  const [isLogModalOpen, setIsLogModalOpen] = useState(false);

  const [mealName, setMealName] = useState("");
  const [calories, setCalories] = useState("");
  const [protein, setProtein] = useState("");
  const [carbs, setCarbs] = useState("");
  const [fat, setFat] = useState("");

  const loadData = async () => {
    const m = await mealsService.getMeals();
    const s = await mealsService.getDailySummary();
    setMeals(m);
    setSummary(s);
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleLogMeal = async (e: React.FormEvent) => {
    e.preventDefault();
    const newMeal: Meal = {
      id: `m-log-${Date.now()}`,
      meal_name: mealName,
      meal_type: "lunch",
      timestamp: new Date().toISOString(),
      calories: Number(calories) || 300,
      protein: Number(protein) || 20,
      carbs: Number(carbs) || 35,
      fat: Number(fat) || 10,
      source: "manual",
    };
    setMeals([newMeal, ...meals]);
    setIsLogModalOpen(false);
    setMealName("");
    setCalories("");
    setProtein("");
    setCarbs("");
    setFat("");
  };

  const columns: Column<Meal>[] = [
    { header: "Meal Description", accessorKey: "meal_name", className: "font-semibold text-white", sortable: true },
    {
      header: "Type",
      cell: (item) => (
        <Badge variant="info" className="capitalize">
          {item.meal_type || "Meal"}
        </Badge>
      ),
    },
    { header: "Logged Time", cell: (item) => new Date(item.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }) },
    { header: "Calories", accessorKey: "calories", className: "text-amber-400 font-bold", sortable: true },
    { header: "Protein (g)", accessorKey: "protein", sortable: true },
    { header: "Carbs (g)", accessorKey: "carbs" },
    { header: "Fat (g)", accessorKey: "fat" },
    {
      header: "Source Channel",
      cell: (item) => (
        <Badge variant={item.source === "whatsapp" ? "success" : "warning"}>
          {item.source?.toUpperCase() || "MANUAL"}
        </Badge>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-6 rounded-2xl glass-card border border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Utensils className="h-6 w-6 text-emerald-400" /> Meal Logging & Daily Macro Breakdown
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Review food logs, daily caloric budgets, and WhatsApp automated meal entries.
          </p>
        </div>
        <Button size="sm" onClick={() => setIsLogModalOpen(true)}>
          <Plus className="h-4 w-4 mr-1.5" /> Log Meal Manually
        </Button>
      </div>

      {summary && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <StatsCard title="Daily Calorie Budget" value={`${summary.total_calories} / ${summary.target_calories} kcal`} icon={Flame} iconColor="text-amber-400" />
          <StatsCard title="Protein Consumed" value={`${summary.total_protein} / ${summary.target_protein} g`} icon={Activity} iconColor="text-emerald-400" />
          <StatsCard title="Carbohydrates" value={`${summary.total_carbs} / ${summary.target_carbs} g`} icon={Calendar} iconColor="text-cyan-400" />
          <StatsCard title="Dietary Fats" value={`${summary.total_fat} / ${summary.target_fat} g`} icon={Utensils} iconColor="text-purple-400" />
        </div>
      )}

      <DataTable title="Daily Meal Logs History" columns={columns} data={meals} keyExtractor={(m) => m.id} searchPlaceholder="Filter meals..." />

      <Modal isOpen={isLogModalOpen} onClose={() => setIsLogModalOpen(false)} title="Log New Meal Entry">
        <form onSubmit={handleLogMeal} className="space-y-4">
          <Input label="Meal Name" placeholder="e.g., Grilled Chicken Rice Bowl" value={mealName} onChange={(e) => setMealName(e.target.value)} required />
          <div className="grid grid-cols-2 gap-3">
            <Input label="Calories (kcal)" type="number" placeholder="450" value={calories} onChange={(e) => setCalories(e.target.value)} required />
            <Input label="Protein (g)" type="number" placeholder="32" value={protein} onChange={(e) => setProtein(e.target.value)} required />
            <Input label="Carbs (g)" type="number" placeholder="48" value={carbs} onChange={(e) => setCarbs(e.target.value)} required />
            <Input label="Fat (g)" type="number" placeholder="12" value={fat} onChange={(e) => setFat(e.target.value)} required />
          </div>
          <div className="flex justify-end gap-3 pt-3">
            <Button type="button" variant="outline" onClick={() => setIsLogModalOpen(false)}>Cancel</Button>
            <Button type="submit">Log Meal</Button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
