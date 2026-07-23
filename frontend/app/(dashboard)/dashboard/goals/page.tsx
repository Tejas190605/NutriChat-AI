"use client";

import React, { useState } from "react";
import { GoalCard } from "@/components/user/GoalCard";
import { Modal } from "@/components/ui/modal";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useNotification } from "@/contexts/NotificationContext";
import { Target, Flame, Activity, Droplet, Scale } from "lucide-react";

export default function GoalsPage() {
  const { addToast } = useNotification();
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [activeGoal, setActiveGoal] = useState<string | null>(null);

  const [weightGoal, setWeightGoal] = useState("70.0");
  const [calorieGoal, setCalorieGoal] = useState("2200");
  const [proteinGoal, setProteinGoal] = useState("160");
  const [carbsGoal, setCarbsGoal] = useState("220");
  const [fatGoal, setFatGoal] = useState("65");
  const [waterGoal, setWaterGoal] = useState("2500");

  const handleEditClick = (goalName: string) => {
    setActiveGoal(goalName);
    setIsEditModalOpen(true);
  };

  const handleSaveGoal = (e: React.FormEvent) => {
    e.preventDefault();
    setIsEditModalOpen(false);
    addToast({
      type: "success",
      title: "Goal Target Updated",
      description: "Your daily nutrition targets have been recalculated.",
    });
  };

  return (
    <div className="space-y-6 max-w-4xl">
      <div className="flex items-center justify-between p-6 rounded-2xl glass-card border border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Target className="h-6 w-6 text-emerald-400" /> Goal Targets & Nutritional Budgets
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Customize target body weight, daily caloric deficit, macronutrient splits, and hydration goals.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <GoalCard
          title="Target Body Weight"
          value={weightGoal}
          unit="kg"
          description="Goal: Fat loss maintenance (-4.2 kg to go)"
          onEdit={() => handleEditClick("Weight Target")}
        />
        <GoalCard
          title="Daily Calorie Budget"
          value={calorieGoal}
          unit="kcal"
          description="Calculated for 350 kcal daily deficit"
          onEdit={() => handleEditClick("Calorie Target")}
        />
        <GoalCard
          title="Daily Protein Target"
          value={proteinGoal}
          unit="g"
          description="1.8g per kg body weight for muscle retention"
          onEdit={() => handleEditClick("Protein Target")}
        />
        <GoalCard
          title="Daily Carbs Target"
          value={carbsGoal}
          unit="g"
          description="Complex carbohydrates energy budget"
          onEdit={() => handleEditClick("Carbs Target")}
        />
        <GoalCard
          title="Daily Fat Target"
          value={fatGoal}
          unit="g"
          description="Essential healthy fats allowance"
          onEdit={() => handleEditClick("Fat Target")}
        />
        <GoalCard
          title="Daily Water Goal"
          value={waterGoal}
          unit="ml"
          description="Optimal 10 cups hydration target"
          onEdit={() => handleEditClick("Water Target")}
        />
      </div>

      <Modal isOpen={isEditModalOpen} onClose={() => setIsEditModalOpen(false)} title={`Update ${activeGoal || "Goal"}`}>
        <form onSubmit={handleSaveGoal} className="space-y-4">
          {activeGoal === "Weight Target" && (
            <Input label="Target Weight (kg)" type="number" value={weightGoal} onChange={(e) => setWeightGoal(e.target.value)} required />
          )}
          {activeGoal === "Calorie Target" && (
            <Input label="Daily Calories (kcal)" type="number" value={calorieGoal} onChange={(e) => setCalorieGoal(e.target.value)} required />
          )}
          {activeGoal === "Protein Target" && (
            <Input label="Protein Target (g)" type="number" value={proteinGoal} onChange={(e) => setProteinGoal(e.target.value)} required />
          )}
          {activeGoal === "Carbs Target" && (
            <Input label="Carbs Target (g)" type="number" value={carbsGoal} onChange={(e) => setCarbsGoal(e.target.value)} required />
          )}
          {activeGoal === "Fat Target" && (
            <Input label="Fat Target (g)" type="number" value={fatGoal} onChange={(e) => setFatGoal(e.target.value)} required />
          )}
          {activeGoal === "Water Target" && (
            <Input label="Water Target (ml)" type="number" value={waterGoal} onChange={(e) => setWaterGoal(e.target.value)} required />
          )}

          <div className="flex justify-end gap-3 pt-3">
            <Button type="button" variant="outline" onClick={() => setIsEditModalOpen(false)}>Cancel</Button>
            <Button type="submit">Save Target</Button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
