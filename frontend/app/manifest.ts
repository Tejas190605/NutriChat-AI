import { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "NutriChat AI - Autonomous Health & Nutrition Coach",
    short_name: "NutriChat AI",
    description: "AI-driven nutrition tracking, body composition analytics, and conversational coaching via WhatsApp & Next.js PWA.",
    start_url: "/dashboard/home",
    display: "standalone",
    background_color: "#020617",
    theme_color: "#10b981",
    icons: [
      {
        src: "/icon-192.png",
        sizes: "192x192",
        type: "image/png",
      },
      {
        src: "/icon-512.png",
        sizes: "512x512",
        type: "image/png",
      },
    ],
    shortcuts: [
      {
        name: "Log Meal",
        short_name: "Log Meal",
        description: "Quick log a meal entry",
        url: "/dashboard/meals",
      },
      {
        name: "AI Health Coach",
        short_name: "AI Coach",
        description: "Consult your AI Health Coach",
        url: "/dashboard/ai-coach",
      },
      {
        name: "AI Photo Analysis",
        short_name: "Photo Analysis",
        description: "Analyze food photo with vision AI",
        url: "/dashboard/meal-analysis",
      },
    ],
  };
}
