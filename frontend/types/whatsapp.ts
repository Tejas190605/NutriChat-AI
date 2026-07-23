export interface WhatsAppSession {
  id: string;
  wa_id: string;
  phone_number: string;
  user_name: string;
  onboarding_state: "NEW" | "GOAL_SETTING" | "METRICS_INPUT" | "COMPLETE";
  last_interaction: string;
  message_count: number;
}

export interface WebhookActivity {
  id: string;
  message_id: string;
  event_type: "messages" | "statuses";
  sender_wa_id: string;
  timestamp: string;
  status: "received" | "processed" | "failed";
  error_detail?: string;
}

export interface WhatsAppMessageLog {
  id: string;
  wa_id: string;
  direction: "inbound" | "outbound";
  message_type: "text" | "image" | "audio" | "document";
  body?: string;
  media_url?: string;
  timestamp: string;
  status: "delivered" | "read" | "sent" | "failed";
}
