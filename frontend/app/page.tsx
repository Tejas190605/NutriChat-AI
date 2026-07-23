import Link from "next/link";
import { Navbar } from "@/components/layout/navbar";
import { Footer } from "@/components/layout/footer";
import { Button } from "@/components/ui/button";
import { Sparkles, MessageSquare, Activity, ShieldCheck, Zap } from "lucide-react";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />

      {/* Hero Section */}
      <main className="flex-1 flex flex-col items-center justify-center text-center px-4 py-20 relative overflow-hidden bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950">
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-emerald-500/30 bg-emerald-500/10 text-emerald-400 text-xs font-semibold mb-6">
          <Sparkles className="h-3.5 w-3.5" /> Autonomous AI Coaching & Nutrition Engine
        </div>

        <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight max-w-4xl text-white">
          Healthy eating as simple as sending a <span className="bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">WhatsApp message</span>
        </h1>

        <p className="mt-6 text-base sm:text-lg text-slate-400 max-w-2xl">
          Log meals effortlessly, analyze nutrition from food photos, estimate US Navy body fat %, and receive real-time coaching intelligence.
        </p>

        <div className="mt-8 flex items-center gap-4">
          <Link href="/dashboard">
            <Button size="lg" className="px-8 shadow-glow">
              Launch Admin Dashboard
            </Button>
          </Link>
          <Link href="/login">
            <Button variant="outline" size="lg">
              Sign In
            </Button>
          </Link>
        </div>

        {/* Feature Cards Grid */}
        <div className="mt-20 grid grid-cols-1 sm:grid-cols-3 gap-6 max-w-5xl w-full text-left">
          <div className="p-6 rounded-2xl glass-card border border-slate-800">
            <div className="p-3 rounded-xl bg-emerald-500/10 text-emerald-400 w-fit mb-4">
              <MessageSquare className="h-6 w-6" />
            </div>
            <h3 className="text-base font-bold text-white">WhatsApp Integration</h3>
            <p className="mt-2 text-xs text-slate-400">
              Conversational onboarding state machine and media processing via Meta Cloud API webhooks.
            </p>
          </div>

          <div className="p-6 rounded-2xl glass-card border border-slate-800">
            <div className="p-3 rounded-xl bg-cyan-500/10 text-cyan-400 w-fit mb-4">
              <Activity className="h-6 w-6" />
            </div>
            <h3 className="text-base font-bold text-white">Analytics & Body Fat</h3>
            <p className="mt-2 text-xs text-slate-400">
              US Navy Body Fat calculations, daily macro totals, weight trend forecasts, and plateau warning alerts.
            </p>
          </div>

          <div className="p-6 rounded-2xl glass-card border border-slate-800">
            <div className="p-3 rounded-xl bg-purple-500/10 text-purple-400 w-fit mb-4">
              <Zap className="h-6 w-6" />
            </div>
            <h3 className="text-base font-bold text-white">AI Orchestration</h3>
            <p className="mt-2 text-xs text-slate-400">
              Powered by Gemini 3.6 Vision & LLM engines with fallback providers and safety guardrails.
            </p>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
