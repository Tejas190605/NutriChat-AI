import type { Metadata } from "next";
import "./globals.css";
import { AppProviders } from "@/providers/AppProviders";
import { ToastContainer } from "@/components/ui/toast";

export const metadata: Metadata = {
  title: "NutriChat AI - Autonomous Health & Nutrition Intelligence",
  description: "AI-driven nutrition tracking, body composition analytics, and conversational coaching via WhatsApp & Next.js Admin Dashboard.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="bg-slate-950 text-slate-100 min-h-screen flex flex-col font-sans">
        <AppProviders>
          {children}
          <ToastContainer />
        </AppProviders>
      </body>
    </html>
  );
}
