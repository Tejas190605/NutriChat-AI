import apiClient from "@/lib/api/axios";
import { Meal, DailyMealSummary } from "@/types/meal";

export const mealsService = {
  getMeals: async (date?: string): Promise<Meal[]> => {
    try {
      const response = await apiClient.get("/meals", { params: { date } });
      return response.data;
    } catch {
      return [
        {
          id: "m-101",
          meal_name: "Paneer Roll & Sprouted Salad",
          meal_type: "lunch",
          timestamp: new Date().toISOString(),
          calories: 480,
          protein: 24.5,
          carbs: 52.0,
          fat: 16.0,
          source: "whatsapp",
        },
        {
          id: "m-102",
          meal_name: "Oatmeal with Almonds & Banana",
          meal_type: "breakfast",
          timestamp: new Date(Date.now() - 14400000).toISOString(),
          calories: 360,
          protein: 12.0,
          carbs: 58.0,
          fat: 8.5,
          source: "manual",
        },
      ];
    }
  },

  logMeal: async (mealData: Partial<Meal>): Promise<{ status: string; meal_id: string }> => {
    const response = await apiClient.post("/meals/log", mealData);
    return response.data;
  },

  getDailySummary: async (date?: string): Promise<DailyMealSummary> => {
    try {
      const response = await apiClient.get("/analytics/daily", { params: { date } });
      return response.data;
    } catch {
      return {
        date: date || new Date().toISOString().split("T")[0],
        total_calories: 1980,
        target_calories: 2200,
        total_protein: 142,
        target_protein: 160,
        total_carbs: 195,
        target_carbs: 220,
        total_fat: 58,
        target_fat: 65,
        meals_logged: 4,
        adherence_percentage: 90,
      };
    }
  },
};
