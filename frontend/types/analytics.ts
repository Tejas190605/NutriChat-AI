export interface DailyNutritionSummaryData {
  id: string;
  user_id: string;
  summary_date: string;
  total_calories: number;
  total_protein: number;
  total_carbs: number;
  total_fat: number;
  total_fiber: number;
  total_water_ml: number;
  meals_logged_count: number;
  compliance_score: number;
}

export interface PredictionData {
  current_weight_kg: number;
  target_weight_kg: number;
  weekly_change_rate_kg: number;
  projected_completion_date: string;
  days_to_goal: number;
}

export interface BodyFatMetrics {
  bmi: number;
  body_fat_percentage?: number;
  bmr: number;
  tdee: number;
}
