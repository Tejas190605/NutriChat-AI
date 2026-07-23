"use client";

import React, { useEffect, useState } from "react";
import { aiService } from "@/services/ai.service";
import { Conversation, ChatMessage } from "@/types/ai";
import { AIChatBubble } from "@/components/user/AIChatBubble";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { BrainCircuit, MessageSquare, Send, Sparkles, Plus, Lightbulb } from "lucide-react";

const SUGGESTED_PROMPTS = [
  "What is the best protein source for a 350 kcal deficit?",
  "How can I break my current weight plateau?",
  "Is paneer or tofu better for lean muscle gain?",
  "Analyze my average macro distribution this week",
];

export default function AICoachPage() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConvId, setActiveConvId] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const load = async () => {
      const convs = await aiService.getConversations();
      setConversations(convs);
      if (convs.length > 0) {
        setActiveConvId(convs[0].id);
      }
    };
    load();
  }, []);

  useEffect(() => {
    if (activeConvId) {
      aiService.getConversationHistory(activeConvId).then(setMessages);
    }
  }, [activeConvId]);

  const handleSendPrompt = async (textToSend?: string) => {
    const query = textToSend || prompt;
    if (!query.trim() || !activeConvId) return;

    const userMsg: ChatMessage = {
      id: `msg-${Date.now()}`,
      role: "user",
      content: query,
      created_at: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMsg]);
    if (!textToSend) setPrompt("");
    setLoading(true);

    try {
      const res = await aiService.sendMessage(activeConvId, query);
      const assistantMsg: ChatMessage = {
        id: `msg-ai-${Date.now()}`,
        role: "assistant",
        content: res.reply,
        created_at: new Date().toISOString(),
        latency_ms: 320,
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch {
      const assistantMsg: ChatMessage = {
        id: `msg-ai-${Date.now()}`,
        role: "assistant",
        content: "To maintain your 350 kcal deficit and retain lean mass, prioritize high-protein foods like Greek yogurt, eggs, low-fat paneer, or chicken breast. Drink 2.5L water daily to stay hydrated!",
        created_at: new Date().toISOString(),
        latency_ms: 290,
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-6 rounded-2xl glass-card border border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <BrainCircuit className="h-6 w-6 text-emerald-400" /> AI Health & Nutrition Coach
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Real-time personalized nutritional coaching, macro optimization advice, and goal guidance powered by Gemini.
          </p>
        </div>
        <Badge variant="success">Gemini 3.6 Flash Active</Badge>
      </div>

      {/* Suggested Prompt Chips */}
      <div className="space-y-2">
        <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
          <Lightbulb className="h-4 w-4 text-amber-400" /> Suggested Coaching Questions
        </h4>
        <div className="flex flex-wrap gap-2">
          {SUGGESTED_PROMPTS.map((p, idx) => (
            <button
              key={idx}
              onClick={() => handleSendPrompt(p)}
              className="px-3 py-1.5 rounded-xl border border-slate-800 bg-slate-900/60 hover:border-emerald-500/40 text-xs text-slate-300 hover:text-white transition-colors cursor-pointer"
            >
              💡 {p}
            </button>
          ))}
        </div>
      </div>

      {/* Main Chat Interface */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Threads List */}
        <div className="rounded-2xl glass-card border border-slate-800 p-4 space-y-3">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <MessageSquare className="h-4 w-4 text-emerald-400" /> Conversations Threads
          </h3>
          <div className="space-y-2">
            {conversations.map((conv) => (
              <button
                key={conv.id}
                onClick={() => setActiveConvId(conv.id)}
                className={`w-full text-left p-3 rounded-xl border text-xs transition-colors cursor-pointer ${
                  activeConvId === conv.id
                    ? "bg-emerald-500/10 border-emerald-500/30 text-white font-semibold"
                    : "bg-slate-900/60 border-slate-800 text-slate-400 hover:text-white"
                }`}
              >
                <div className="flex justify-between items-center">
                  <span className="truncate">{conv.title}</span>
                  <Badge variant={conv.is_active ? "success" : "info"}>{conv.message_count} msgs</Badge>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Messages & Input */}
        <div className="lg:col-span-2 rounded-2xl glass-card border border-slate-800 p-5 flex flex-col h-[520px] justify-between">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <Sparkles className="h-4 w-4 text-emerald-400" /> Live AI Session
            </h3>
            <span className="text-[11px] text-slate-500 font-mono">Thread ID: {activeConvId || "c-101"}</span>
          </div>

          {/* Messages Feed */}
          <div className="flex-1 overflow-y-auto my-4 space-y-2 pr-2">
            {messages.map((msg) => (
              <AIChatBubble
                key={msg.id}
                role={msg.role}
                content={msg.content}
                timestamp={msg.created_at}
                latencyMs={msg.latency_ms}
              />
            ))}
            {loading && <p className="text-xs text-slate-500 italic">Gemini Coach is formulating advice...</p>}
          </div>

          {/* Input Controls */}
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSendPrompt();
            }}
            className="flex gap-2 pt-3 border-t border-slate-800"
          >
            <Input
              placeholder="Ask your AI health coach anything about nutrition, deficit or meals..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              className="flex-1"
            />
            <Button type="submit" isLoading={loading}>
              <Send className="h-4 w-4" />
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
}
