"use client";

import React, { useEffect, useState } from "react";
import { settingsService } from "@/services/settings.service";
import { UserProfile } from "@/types/settings";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Avatar } from "@/components/ui/avatar";
import { useNotification } from "@/contexts/NotificationContext";
import { User, Activity, Heart, AlertTriangle, ShieldCheck } from "lucide-react";

export default function ProfilePage() {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const { addToast } = useNotification();

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [activityLevel, setActivityLevel] = useState("moderately_active");
  const [dietaryPref, setDietaryPref] = useState("vegetarian");

  useEffect(() => {
    const load = async () => {
      const p = await settingsService.getProfile();
      setProfile(p);
      setFullName(p.full_name);
      setEmail(p.email);
      setPhone(p.phone_number || "");
    };
    load();
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    addToast({
      type: "success",
      title: "Profile Saved",
      description: "Personal health profile and dietary parameters updated.",
    });
  };

  return (
    <div className="space-y-6 max-w-4xl">
      <div className="flex items-center justify-between p-6 rounded-2xl glass-card border border-slate-800">
        <div className="flex items-center gap-4">
          <Avatar name={fullName || "User"} size="lg" />
          <div>
            <h2 className="text-xl font-bold text-white">{fullName || "Tejas Parmar"}</h2>
            <p className="text-xs text-slate-400">{email || "admin@nutrichat.ai"}</p>
            <Badge variant="success" className="mt-1">Active User Profile</Badge>
          </div>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Personal & Contact Information */}
        <Card className="p-6 border border-slate-800 space-y-4">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <User className="h-5 w-5 text-emerald-400" /> Personal & Contact Information
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <Input label="Full Name" value={fullName} onChange={(e) => setFullName(e.target.value)} required />
            <Input label="Email Address" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
            <Input label="WhatsApp Phone Number" value={phone} onChange={(e) => setPhone(e.target.value)} />
            <Select
              label="Gender"
              value="male"
              onChange={() => {}}
              options={[
                { label: "Male", value: "male" },
                { label: "Female", value: "female" },
                { label: "Other", value: "other" },
              ]}
            />
          </div>
        </Card>

        {/* Health Profile & Physical Parameters */}
        <Card className="p-6 border border-slate-800 space-y-4">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Activity className="h-5 w-5 text-cyan-400" /> Health Profile & Physical Metrics
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <Input label="Age (years)" type="number" defaultValue="28" />
            <Input label="Height (cm)" type="number" defaultValue="175" />
            <Input label="Current Weight (kg)" type="number" defaultValue="74.2" />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <Select
              label="Activity Level"
              value={activityLevel}
              onChange={(e) => setActivityLevel(e.target.value)}
              options={[
                { label: "Sedentary (Little to no exercise)", value: "sedentary" },
                { label: "Lightly Active (1-3 days/wk)", value: "lightly_active" },
                { label: "Moderately Active (3-5 days/wk)", value: "moderately_active" },
                { label: "Very Active (6-7 days/wk)", value: "very_active" },
              ]}
            />
            <Select
              label="Dietary Preference"
              value={dietaryPref}
              onChange={(e) => setDietaryPref(e.target.value)}
              options={[
                { label: "Vegetarian", value: "vegetarian" },
                { label: "Vegan", value: "vegan" },
                { label: "Non-Vegetarian", value: "non_veg" },
                { label: "Eggetarian", value: "eggetarian" },
              ]}
            />
          </div>
        </Card>

        {/* Allergies & Conditions */}
        <Card className="p-6 border border-slate-800 space-y-4">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <AlertTriangle className="h-5 w-5 text-amber-400" /> Allergies & Medical Restrictions
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <Input label="Known Allergies" placeholder="e.g., Peanuts, Lactose, Gluten" defaultValue="Lactose" />
            <Input label="Medical Conditions" placeholder="e.g., Diabetes Type II, PCOS" defaultValue="None" />
          </div>
        </Card>

        <div className="flex justify-end">
          <Button type="submit" size="lg">
            Save Profile & Health Metrics
          </Button>
        </div>
      </form>
    </div>
  );
}
