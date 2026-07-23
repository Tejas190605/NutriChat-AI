import apiClient from "@/lib/api/axios";
import { WhatsAppSession, WebhookActivity, WhatsAppMessageLog } from "@/types/whatsapp";

export const whatsappService = {
  getSessions: async (): Promise<WhatsAppSession[]> => {
    try {
      const response = await apiClient.get("/whatsapp/admin/sessions");
      return response.data;
    } catch {
      return [
        {
          id: "ws-1",
          wa_id: "919876543210",
          phone_number: "+91 9876543210",
          user_name: "Tejas Parmar",
          onboarding_state: "COMPLETE",
          last_interaction: "2026-07-23T14:22:00Z",
          message_count: 48,
        },
        {
          id: "ws-2",
          wa_id: "14155552671",
          phone_number: "+1 4155552671",
          user_name: "Sarah Jenkins",
          onboarding_state: "GOAL_SETTING",
          last_interaction: "2026-07-23T11:05:00Z",
          message_count: 6,
        },
      ];
    }
  },

  getWebhookActivities: async (): Promise<WebhookActivity[]> => {
    try {
      const response = await apiClient.get("/whatsapp/admin/health");
      return response.data;
    } catch {
      return [
        {
          id: "wh-1",
          message_id: "wamid.HBgLMTIzNDU2Nzg5MFVVAAYg...",
          event_type: "messages",
          sender_wa_id: "919876543210",
          timestamp: "2026-07-23T14:22:00Z",
          status: "processed",
        },
        {
          id: "wh-2",
          message_id: "wamid.HBgLMTIzNDU2Nzg5TVVVAAYg...",
          event_type: "messages",
          sender_wa_id: "14155552671",
          timestamp: "2026-07-23T11:05:00Z",
          status: "processed",
        },
      ];
    }
  },

  getMessageLogs: async (): Promise<WhatsAppMessageLog[]> => {
    return [
      {
        id: "ml-1",
        wa_id: "919876543210",
        direction: "inbound",
        message_type: "text",
        body: "I ate 2 rotis and paneer tikka for lunch",
        timestamp: "2026-07-23T14:22:00Z",
        status: "read",
      },
      {
        id: "ml-2",
        wa_id: "919876543210",
        direction: "outbound",
        message_type: "text",
        body: "Logged! 440 kcal (22g P / 44g C / 18g F). You have 1,540 kcal remaining today.",
        timestamp: "2026-07-23T14:22:02Z",
        status: "delivered",
      },
    ];
  },
};
