import apiClient from "@/lib/api/axios";

export interface WeightTrajectoryPoint {
  date: string;
  actual?: number;
  predicted: number;
}

export interface HabitItem {
  id: string;
  name: string;
  streak: number;
  completed_today: boolean;
}

export const analyticsService = {
  getDailyAnalytics: async () => {
    try {
      const response = await apiClient.get("/analytics/daily");
      return response.data;
    } catch {
      return {
        calories: 1980,
        protein: 142,
        carbs: 195,
        fat: 58,
        water_ml: 2500,
        compliance: 94,
      };
    }
  },

  getWeightPredictions: async (): Promise<WeightTrajectoryPoint[]> => {
    try {
      const response = await apiClient.get("/analytics/predictions");
      return response.data;
    } catch {
      return [
        { date: "2026-07-17", actual: 75.2, predicted: 75.2 },
        { date: "2026-07-19", actual: 74.8, predicted: 74.9 },
        { date: "2026-07-21", actual: 74.4, predicted: 74.5 },
        { date: "2026-07-23", actual: 74.2, predicted: 74.2 },
        { date: "2026-07-25", predicted: 73.9 },
        { date: "2026-07-27", predicted: 73.6 },
        { date: "2026-07-29", predicted: 73.3 },
      ];
    }
  },

  getHabits: async (): Promise<HabitItem[]> => {
    return [
      { id: "h-1", name: "Log 3 Meals Daily", streak: 14, completed_today: true },
      { id: "h-2", name: "Reach 140g Protein", streak: 5, completed_today: true },
      { id: "h-3", name: "Drink 2.5L Water", streak: 8, completed_today: false },
    ];
  },
};
