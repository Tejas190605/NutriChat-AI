import apiClient from "@/lib/api/axios";
import { UserProfile, SystemConfig } from "@/types/settings";

export const settingsService = {
  getProfile: async (): Promise<UserProfile> => {
    try {
      const response = await apiClient.get("/auth/me");
      return response.data;
    } catch {
      return {
        id: "u-101",
        email: "admin@nutrichat.ai",
        full_name: "Tejas Parmar",
        phone_number: "+91 9876543210",
        role: "admin",
        calorie_target: 2200,
        protein_target: 160,
        carbs_target: 220,
        fat_target: 65,
        created_at: "2026-07-01T10:00:00Z",
      };
    }
  },

  getSystemConfig: async (): Promise<SystemConfig> => {
    return {
      ai_provider: "gemini",
      model_name: "gemini-3.6-flash",
      temperature: 0.4,
      max_tokens: 2048,
      rate_limit_per_min: 60,
      ocr_engine: "google_vision",
      whatsapp_verify_token: "nutrichat_verify_secret_2026",
      cache_ttl_seconds: 3600,
    };
  },

  updateProfile: async (data: Partial<UserProfile>): Promise<UserProfile> => {
    const response = await apiClient.put("/auth/me", data);
    return response.data;
  },
};
