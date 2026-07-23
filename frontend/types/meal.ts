export interface MealItem {
  id: string;
  food_name: string;
  quantity: number;
  unit: string;
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
}

export interface Meal {
  id: string;
  meal_name: string;
  meal_type?: "breakfast" | "lunch" | "dinner" | "snack";
  timestamp: string;
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
  items?: MealItem[];
  source?: "whatsapp" | "manual" | "vision";
  image_url?: string;
}

export interface DailyMealSummary {
  date: string;
  total_calories: number;
  target_calories: number;
  total_protein: number;
  target_protein: number;
  total_carbs: number;
  target_carbs: number;
  total_fat: number;
  target_fat: number;
  meals_logged: number;
  adherence_percentage: number;
}
