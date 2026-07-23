"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/contexts/AuthContext";
import { useNotification } from "@/contexts/NotificationContext";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuth();
  const { addToast } = useNotification();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      await login({ username, password });
      addToast({
        type: "success",
        title: "Welcome back!",
        description: "Authenticated successfully.",
      });
    } catch (err: any) {
      addToast({
        type: "error",
        title: "Authentication Failed",
        description: err.response?.data?.detail || "Invalid credentials provided.",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="p-6 border border-slate-800">
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          label="Email or Phone Number"
          type="text"
          placeholder="admin@nutrichat.ai"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />

        <Input
          label="Password"
          type="password"
          placeholder="••••••••"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <Button type="submit" isLoading={isLoading} className="w-full mt-2">
          Sign In
        </Button>
      </form>
    </Card>
  );
}
