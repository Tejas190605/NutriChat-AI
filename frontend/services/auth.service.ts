import { apiClient } from "@/lib/api/axios";
import { User, AuthTokens } from "@/types/auth";

export interface LoginPayload {
  username: string; // or email
  password: string;
}

export interface RegisterPayload {
  email: string;
  password: string;
  full_name: string;
  phone_number?: string;
}

export const authService = {
  async login(payload: LoginPayload): Promise<{ user: User; tokens: AuthTokens }> {
    const formData = new URLSearchParams();
    formData.append("username", payload.username);
    formData.append("password", payload.password);

    const response = await apiClient.post("/auth/login", formData, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });
    return response.data;
  },

  async register(payload: RegisterPayload): Promise<User> {
    const response = await apiClient.post("/auth/register", payload);
    return response.data;
  },

  async getMe(): Promise<User> {
    const response = await apiClient.get("/auth/me");
    return response.data;
  },

  async logout(): Promise<void> {
    try {
      await apiClient.post("/auth/logout");
    } finally {
      if (typeof window !== "undefined") {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
      }
    }
  },
};
