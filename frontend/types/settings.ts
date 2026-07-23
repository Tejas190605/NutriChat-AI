export interface UserProfile {
  id: string;
  email: string;
  full_name: string;
  phone_number?: string;
  role: string;
  calorie_target: number;
  protein_target: number;
  carbs_target: number;
  fat_target: number;
  created_at: string;
}

export interface SystemConfig {
  ai_provider: "gemini" | "openai" | "fallback";
  model_name: string;
  temperature: number;
  max_tokens: number;
  rate_limit_per_min: number;
  ocr_engine: "google_vision" | "tesseract";
  whatsapp_verify_token: string;
  cache_ttl_seconds: number;
}
