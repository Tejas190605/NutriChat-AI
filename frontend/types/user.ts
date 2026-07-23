export type ActivityLevel = "sedentary" | "lightly_active" | "moderately_active" | "very_active" | "extra_active";
export type PrimaryGoal = "weight_loss" | "weight_gain" | "maintain" | "muscle_gain" | "health";

export interface UserProfile {
  id: string;
  user_id: string;
  age: number;
  gender: "male" | "female" | "other";
  height_cm: number;
  current_weight_kg: number;
  target_weight_kg: number;
  activity_level: ActivityLevel;
  primary_goal: PrimaryGoal;
  dietary_preferences?: string[];
  allergies?: string[];
  created_at: string;
}

export interface UserGoal {
  id: string;
  user_id: string;
  daily_calories_target: number;
  protein_grams_target: number;
  carbs_grams_target: number;
  fat_grams_target: number;
  water_ml_target: number;
}

export interface User {
  id: string;
  email: string;
  full_name: string;
  phone_number?: string;
  role: string;
  is_active: boolean;
  created_at: string;
  profile?: UserProfile;
  goals?: UserGoal;
}
