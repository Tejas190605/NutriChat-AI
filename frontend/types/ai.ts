export interface ChatMessage {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  tokens?: number;
  created_at: string;
  model_name?: string;
  latency_ms?: number;
}

export interface Conversation {
  id: string;
  title: string;
  user_id: string;
  created_at: string;
  updated_at: string;
  message_count: number;
  is_active: boolean;
  messages?: ChatMessage[];
}

export interface PromptTemplate {
  id: string;
  name: string;
  description: string;
  active_version?: number;
  updated_at: string;
}

export interface PromptVersion {
  id: string;
  template_id: string;
  version: number;
  system_prompt: string;
  user_prompt_template: string;
  model_name: string;
  temperature: number;
  is_active: boolean;
}

export interface Recommendation {
  id: string;
  user_id: string;
  category: "swap" | "deficit" | "macro_split" | "coaching";
  title: string;
  description: string;
  created_at: string;
  user_feedback?: "liked" | "disliked" | "accepted";
}

export interface ModelUsage {
  date: string;
  requests_count: number;
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
  avg_latency_ms: number;
  error_rate: number;
}
