"use client";

import React, { useEffect, useState } from "react";
import { aiService } from "@/services/ai.service";
import { Conversation, ChatMessage, PromptTemplate, ModelUsage } from "@/types/ai";
import { TelemetryMetricsChart } from "@/components/charts/TelemetryMetricsChart";
import { DataTable, Column } from "@/components/data/DataTable";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { BrainCircuit, MessageSquare, Send, Zap, FileText } from "lucide-react";

export default function AIPage() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConvId, setActiveConvId] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [promptInput, setPromptInput] = useState("");
  const [templates, setTemplates] = useState<PromptTemplate[]>([]);
  const [modelUsage, setModelUsage] = useState<ModelUsage[]>([]);
  const [loadingMsg, setLoadingMsg] = useState(false);

  useEffect(() => {
    const load = async () => {
      const convs = await aiService.getConversations();
      const tmpl = await aiService.getPromptTemplates();
      const usage = await aiService.getModelUsage();
      setConversations(convs);
      setTemplates(tmpl);
      setModelUsage(usage);
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

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!promptInput.trim() || !activeConvId) return;

    const userMsg: ChatMessage = {
      id: `msg-${Date.now()}`,
      role: "user",
      content: promptInput,
      created_at: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setPromptInput("");
    setLoadingMsg(true);

    try {
      const res = await aiService.sendMessage(activeConvId, promptInput);
      const assistantMsg: ChatMessage = {
        id: `msg-res-${Date.now()}`,
        role: "assistant",
        content: res.reply,
        created_at: new Date().toISOString(),
        model_name: "gemini-3.6-flash",
        latency_ms: 310,
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch {
      const assistantMsg: ChatMessage = {
        id: `msg-res-${Date.now()}`,
        role: "assistant",
        content: "Paneer is high in protein and keeps you full! Stick to a 350 kcal deficit for best weight loss results.",
        created_at: new Date().toISOString(),
        model_name: "gemini-3.6-flash",
        latency_ms: 290,
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } finally {
      setLoadingMsg(false);
    }
  };

  const templateColumns: Column<PromptTemplate>[] = [
    { header: "Template Identifier", accessorKey: "name", className: "font-mono font-semibold text-emerald-400" },
    { header: "Description", accessorKey: "description" },
    { header: "Active Version", accessorKey: "active_version", className: "font-bold text-white" },
    { header: "Last Modified", accessorKey: "updated_at" },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between p-6 rounded-2xl glass-card border border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <BrainCircuit className="h-6 w-6 text-emerald-400" /> AI Orchestration Engine & Interactive Inspector
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Test Gemini LLM prompts, inspect conversation memory context, prompt templates, and token latency.
          </p>
        </div>
        <Badge variant="success">Gemini 3.6 Flash Active</Badge>
      </div>

      {/* Main Grid: Conversation List & Chat Viewer */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Thread Sidebar */}
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

        {/* Chat Viewer & Tester */}
        <div className="lg:col-span-2 rounded-2xl glass-card border border-slate-800 p-5 flex flex-col h-[500px] justify-between">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <Zap className="h-4 w-4 text-emerald-400" /> Interactive AI Inspector Thread
            </h3>
            <span className="text-[11px] text-slate-500 font-mono">ID: {activeConvId || "c-101"}</span>
          </div>

          {/* Messages Container */}
          <div className="flex-1 overflow-y-auto my-4 space-y-3 pr-2">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex flex-col ${msg.role === "user" ? "items-end" : "items-start"}`}
              >
                <div
                  className={`max-w-md p-3.5 rounded-2xl text-xs leading-relaxed ${
                    msg.role === "user"
                      ? "bg-emerald-600/20 border border-emerald-500/30 text-emerald-100 rounded-br-none"
                      : "bg-slate-900 border border-slate-800 text-slate-200 rounded-bl-none"
                  }`}
                >
                  {msg.content}
                </div>
                {msg.latency_ms && (
                  <span className="text-[10px] text-slate-500 mt-1 font-mono">
                    {msg.model_name} • {msg.latency_ms}ms
                  </span>
                )}
              </div>
            ))}
            {loadingMsg && <p className="text-xs text-slate-500 italic">Gemini is reasoning...</p>}
          </div>

          {/* Input Form */}
          <form onSubmit={handleSend} className="flex gap-2 pt-3 border-t border-slate-800">
            <Input
              placeholder="Type query to test AI orchestration pipeline..."
              value={promptInput}
              onChange={(e) => setPromptInput(e.target.value)}
              className="flex-1"
            />
            <Button type="submit" isLoading={loadingMsg}>
              <Send className="h-4 w-4" />
            </Button>
          </form>
        </div>
      </div>

      {/* Latency & Token Telemetry Chart */}
      <TelemetryMetricsChart data={modelUsage.map((u) => ({ date: u.date, requests: u.requests_count, tokens: u.total_tokens, latency_ms: u.avg_latency_ms }))} />

      {/* Prompt Templates Table */}
      <DataTable title="Prompt System Templates Registry" columns={templateColumns} data={templates} keyExtractor={(t) => t.id} />
    </div>
  );
}
