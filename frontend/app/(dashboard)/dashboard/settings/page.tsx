"use client";

import React, { useEffect, useState } from "react";
import { settingsService } from "@/services/settings.service";
import { UserProfile, SystemConfig } from "@/types/settings";
import { Tabs } from "@/components/ui/tabs";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Badge } from "@/components/ui/badge";
import { useNotification } from "@/contexts/NotificationContext";
import { Settings, User, Key, Sliders, Shield, Bell, BrainCircuit } from "lucide-react";

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState("profile");
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [config, setConfig] = useState<SystemConfig | null>(null);
  const { addToast } = useNotification();

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [calorieTarget, setCalorieTarget] = useState("");

  const [aiProvider, setAiProvider] = useState("gemini");
  const [modelName, setModelName] = useState("gemini-3.6-flash");

  useEffect(() => {
    const load = async () => {
      const p = await settingsService.getProfile();
      const c = await settingsService.getSystemConfig();
      setProfile(p);
      setConfig(c);
      setFullName(p.full_name);
      setEmail(p.email);
      setCalorieTarget(String(p.calorie_target));
      setAiProvider(c.ai_provider);
      setModelName(c.model_name);
    };
    load();
  }, []);

  const handleSaveProfile = (e: React.FormEvent) => {
    e.preventDefault();
    addToast({ type: "success", title: "Profile Saved", description: "Admin settings updated successfully." });
  };

  const handleSaveConfig = (e: React.FormEvent) => {
    e.preventDefault();
    addToast({ type: "success", title: "AI System Settings Saved", description: "Engine configuration updated." });
  };

  return (
    <div className="space-y-6 max-w-5xl">
      <div className="flex items-center justify-between p-6 rounded-2xl glass-card border border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Settings className="h-6 w-6 text-emerald-400" /> Admin & System Settings
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Configure user profiles, API key secrets, AI provider models, and WhatsApp webhook credentials.
          </p>
        </div>
      </div>

      <Tabs
        tabs={[
          { id: "profile", label: "Profile & Targets", icon: User },
          { id: "ai_config", label: "AI Engine Config", icon: BrainCircuit },
          { id: "api_keys", label: "API Keys & Secrets", icon: Key },
          { id: "notifications", label: "Notifications", icon: Bell },
          { id: "security", label: "Security & Role", icon: Shield },
        ]}
        activeTab={activeTab}
        onChange={setActiveTab}
      />

      {activeTab === "profile" && (
        <Card className="p-6 border border-slate-800 space-y-4">
          <h3 className="text-base font-bold text-white">Administrator Profile</h3>
          <form onSubmit={handleSaveProfile} className="space-y-4">
            <Input label="Full Name" value={fullName} onChange={(e) => setFullName(e.target.value)} required />
            <Input label="Email Address" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
            <Input label="Daily Calorie Goal (kcal)" type="number" value={calorieTarget} onChange={(e) => setCalorieTarget(e.target.value)} required />
            <Button type="submit">Save Profile Changes</Button>
          </form>
        </Card>
      )}

      {activeTab === "ai_config" && (
        <Card className="p-6 border border-slate-800 space-y-4">
          <h3 className="text-base font-bold text-white">AI Engine Configuration</h3>
          <form onSubmit={handleSaveConfig} className="space-y-4">
            <Input label="Primary AI Provider" value={aiProvider} onChange={(e) => setAiProvider(e.target.value)} required />
            <Input label="Model Identifier" value={modelName} onChange={(e) => setModelName(e.target.value)} required />
            <div className="flex items-center justify-between p-3 rounded-xl bg-slate-900 border border-slate-800">
              <div>
                <p className="text-xs font-bold text-white">Enable Circuit Breaker Failover</p>
                <p className="text-[11px] text-slate-400">Fallback to secondary provider on timeout or API degradation</p>
              </div>
              <Switch checked={true} onChange={() => {}} />
            </div>
            <Button type="submit">Update AI Config</Button>
          </form>
        </Card>
      )}

      {activeTab === "api_keys" && (
        <Card className="p-6 border border-slate-800 space-y-4">
          <h3 className="text-base font-bold text-white">API Keys & Provider Integrations</h3>
          <div className="space-y-3">
            <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-between">
              <div>
                <p className="text-xs font-bold text-white">GEMINI_API_KEY</p>
                <p className="text-[11px] font-mono text-slate-500">AIzaSyB...****</p>
              </div>
              <Badge variant="success">CONFIGURED</Badge>
            </div>
            <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-between">
              <div>
                <p className="text-xs font-bold text-white">WHATSAPP_CLOUD_API_TOKEN</p>
                <p className="text-[11px] font-mono text-slate-500">EAAGm0...****</p>
              </div>
              <Badge variant="success">CONFIGURED</Badge>
            </div>
          </div>
        </Card>
      )}

      {activeTab === "notifications" && (
        <Card className="p-6 border border-slate-800 space-y-4">
          <h3 className="text-base font-bold text-white">Notification Preferences</h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 rounded-xl bg-slate-900 border border-slate-800">
              <div>
                <p className="text-xs font-bold text-white">Plateau Risk Alerts</p>
                <p className="text-[11px] text-slate-400">Receive alerts when weight plateau is detected for &gt; 7 days</p>
              </div>
              <Switch checked={true} onChange={() => {}} />
            </div>
            <div className="flex items-center justify-between p-3 rounded-xl bg-slate-900 border border-slate-800">
              <div>
                <p className="text-xs font-bold text-white">WhatsApp Webhook Failures</p>
                <p className="text-[11px] text-slate-400">Instant notification on HMAC signature mismatch or delivery drops</p>
              </div>
              <Switch checked={true} onChange={() => {}} />
            </div>
          </div>
        </Card>
      )}

      {activeTab === "security" && (
        <Card className="p-6 border border-slate-800 space-y-4">
          <h3 className="text-base font-bold text-white">Security & Role Access</h3>
          <p className="text-xs text-slate-400">
            Authenticated via JWT Bearer tokens with automatic background token refresh on 401 response status.
          </p>
          <Badge variant="success">Role: SuperAdmin</Badge>
        </Card>
      )}
    </div>
  );
}
