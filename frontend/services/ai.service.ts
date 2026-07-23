import apiClient from "@/lib/api/axios";
import { Conversation, ChatMessage, PromptTemplate, ModelUsage } from "@/types/ai";

export const aiService = {
  getConversations: async (): Promise<Conversation[]> => {
    try {
      const response = await apiClient.get("/ai/conversations");
      return response.data;
    } catch {
      return [
        {
          id: "c-101",
          title: "Daily Nutrition Coaching",
          user_id: "u-101",
          created_at: "2026-07-22T08:00:00Z",
          updated_at: "2026-07-23T14:10:00Z",
          message_count: 8,
          is_active: true,
        },
        {
          id: "c-102",
          title: "Meal Analysis & Swaps",
          user_id: "u-102",
          created_at: "2026-07-21T11:30:00Z",
          updated_at: "2026-07-22T19:45:00Z",
          message_count: 5,
          is_active: false,
        },
      ];
    }
  },

  getConversationHistory: async (conversationId: string): Promise<ChatMessage[]> => {
    try {
      const response = await apiClient.get("/ai/history", { params: { conversation_id: conversationId } });
      return response.data;
    } catch {
      return [
        {
          id: "msg-1",
          role: "user",
          content: "Is paneer good for weight loss?",
          tokens: 12,
          created_at: "2026-07-23T14:00:00Z",
        },
        {
          id: "msg-2",
          role: "assistant",
          content:
            "Paneer is high in protein and keeps you full, but it contains fat. Opt for low-fat paneer or balance your portion sizes to stay within your deficit.",
          tokens: 38,
          created_at: "2026-07-23T14:00:02Z",
          model_name: "gemini-3.6-flash",
          latency_ms: 340,
        },
      ];
    }
  },

  sendMessage: async (conversationId: string, message: string): Promise<{ reply: string }> => {
    const response = await apiClient.post("/ai/chat", { conversation_id: conversationId, message });
    return response.data;
  },

  getPromptTemplates: async (): Promise<PromptTemplate[]> => {
    return [
      { id: "pt-1", name: "coaching_agent", description: "Empathetic daily nutrition & deficit coach", active_version: 3, updated_at: "2026-07-20" },
      { id: "pt-2", name: "vision_meal_analyzer", description: "Food bounding box and calorie estimator", active_version: 2, updated_at: "2026-07-18" },
    ];
  },

  getModelUsage: async (): Promise<ModelUsage[]> => {
    return [
      { date: "2026-07-17", requests_count: 420, prompt_tokens: 124000, completion_tokens: 48000, total_tokens: 172000, avg_latency_ms: 380, error_rate: 0.1 },
      { date: "2026-07-19", requests_count: 580, prompt_tokens: 168000, completion_tokens: 62000, total_tokens: 230000, avg_latency_ms: 350, error_rate: 0.0 },
      { date: "2026-07-21", requests_count: 710, prompt_tokens: 210000, completion_tokens: 79000, total_tokens: 289000, avg_latency_ms: 320, error_rate: 0.2 },
      { date: "2026-07-23", requests_count: 850, prompt_tokens: 254000, completion_tokens: 95000, total_tokens: 349000, avg_latency_ms: 310, error_rate: 0.0 },
    ];
  },
};
