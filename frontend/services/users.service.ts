import apiClient from "@/lib/api/axios";
import { User } from "@/types/user";

export interface UsersResponse {
  items: User[];
  total: number;
  page: number;
  limit: number;
}

export const usersService = {
  getUsers: async (page = 1, limit = 10, search = ""): Promise<UsersResponse> => {
    try {
      const response = await apiClient.get("/users", { params: { page, limit, search } });
      return response.data;
    } catch {
      // Fallback mock data if server endpoint is initial state
      return {
        items: [
          {
            id: "u-101",
            email: "tejas@nutrichat.ai",
            full_name: "Tejas Parmar",
            phone_number: "+91 9876543210",
            role: "admin",
            is_active: true,
            created_at: "2026-07-01T10:00:00Z",
          },
          {
            id: "u-102",
            email: "sarah@nutrichat.ai",
            full_name: "Sarah Jenkins",
            phone_number: "+1 4155552671",
            role: "user",
            is_active: true,
            created_at: "2026-07-05T14:20:00Z",
          },
          {
            id: "u-103",
            email: "rahul@nutrichat.ai",
            full_name: "Rahul Sharma",
            phone_number: "+91 9123456789",
            role: "user",
            is_active: true,
            created_at: "2026-07-10T09:15:00Z",
          },
        ],
        total: 3,
        page,
        limit,
      };
    }
  },

  getUserById: async (id: string): Promise<User> => {
    try {
      const response = await apiClient.get(`/users/${id}`);
      return response.data;
    } catch {
      return {
        id,
        email: "user@nutrichat.ai",
        full_name: "Demo User",
        phone_number: "+91 9876543210",
        role: "user",
        is_active: true,
        created_at: "2026-07-01T10:00:00Z",
      };
    }
  },
};
