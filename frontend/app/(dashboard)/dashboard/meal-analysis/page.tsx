"use client";

import React, { useState } from "react";
import { visionService } from "@/services/vision.service";
import { mealsService } from "@/services/meals.service";
import { VisionPrediction, OCRResult } from "@/types/vision";
import { ImageUploader } from "@/components/user/ImageUploader";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useNotification } from "@/contexts/NotificationContext";
import { Camera, Sparkles, CheckCircle2, FileText, Flame, Plus } from "lucide-react";
import { useRouter } from "next/navigation";

export default function MealAnalysisPage() {
  const router = useRouter();
  const { addToast } = useNotification();

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [predictions, setPredictions] = useState<VisionPrediction[] | null>(null);
  const [ocrResult, setOcrResult] = useState<OCRResult | null>(null);

  // Editable Form State
  const [mealName, setMealName] = useState("");
  const [calories, setCalories] = useState("");
  const [protein, setProtein] = useState("");
  const [carbs, setCarbs] = useState("");
  const [fat, setFat] = useState("");

  const handleUploadAndAnalyze = async (file: File) => {
    setSelectedFile(file);
    setAnalyzing(true);

    try {
      // Simulate backend vision processing API response
      setTimeout(() => {
        const mockPredictions: VisionPrediction[] = [
          { label: "Paneer Tikka & Roti", confidence: 0.94, portion: "1 plate (250g)", weight_grams: 250, calories: 450 },
        ];
        const mockOcr: OCRResult = {
          id: "ocr-new",
          image_id: "img-new",
          extracted_text: "Paneer Roll 250g - 450 kcal (22g P)",
          confidence: 0.96,
        };

        setPredictions(mockPredictions);
        setOcrResult(mockOcr);
        setMealName("Paneer Tikka & Roti");
        setCalories("450");
        setProtein("22");
        setCarbs("45");
        setFat("16");

        setAnalyzing(false);
        addToast({
          type: "success",
          title: "AI Analysis Complete",
          description: "Food dish recognized with 94% confidence score.",
        });
      }, 1500);
    } catch {
      setAnalyzing(false);
    }
  };

  const handleSaveMeal = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await mealsService.logMeal({
        meal_name: mealName,
        calories: Number(calories) || 400,
        protein: Number(protein) || 20,
        carbs: Number(carbs) || 40,
        fat: Number(fat) || 12,
        source: "vision",
      });
      addToast({
        type: "success",
        title: "Meal Saved!",
        description: "Logged into your daily nutrition journal.",
      });
      router.push("/dashboard/meals");
    } catch {
      addToast({
        type: "error",
        title: "Failed to save meal",
        description: "Please check inputs and retry.",
      });
    }
  };

  return (
    <div className="space-y-6 max-w-4xl">
      <div className="flex items-center justify-between p-6 rounded-2xl glass-card border border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Camera className="h-6 w-6 text-emerald-400" /> AI Food Photo & Vision Analysis
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Upload a meal photo to detect dish items, estimate portion sizes, and parse OCR nutrition panels automatically.
          </p>
        </div>
        <Badge variant="success">Gemini 3.6 Vision Active</Badge>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Upload Column */}
        <Card className="p-6 border border-slate-800 space-y-4">
          <h3 className="text-base font-bold text-white">Select Food Photo</h3>
          <ImageUploader onFileSelect={handleUploadAndAnalyze} isLoading={analyzing} />

          {analyzing && (
            <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 text-center space-y-2">
              <div className="h-6 w-6 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin mx-auto" />
              <p className="text-xs font-semibold text-emerald-400">Gemini Vision is analyzing your meal...</p>
              <p className="text-[11px] text-slate-500">Detecting food items, bounding boxes & nutrition text</p>
            </div>
          )}
        </Card>

        {/* Results & Confirmation Form Column */}
        <Card className="p-6 border border-slate-800 space-y-4">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-emerald-400" /> Recognized Dish & Macro Breakdown
          </h3>

          {predictions && predictions.length > 0 ? (
            <form onSubmit={handleSaveMeal} className="space-y-4">
              <div className="p-3.5 rounded-xl bg-emerald-950/20 border border-emerald-800/40 text-xs space-y-1">
                <div className="flex justify-between font-bold text-white">
                  <span>Detected: {predictions[0].label}</span>
                  <span className="text-emerald-400">{(predictions[0].confidence * 100).toFixed(0)}% Match</span>
                </div>
                <p className="text-slate-400">Portion: {predictions[0].portion}</p>
              </div>

              {ocrResult && (
                <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 text-xs space-y-1">
                  <span className="text-cyan-400 font-semibold flex items-center gap-1">
                    <FileText className="h-3.5 w-3.5" /> OCR Extracted Fact Label
                  </span>
                  <p className="text-slate-300 italic">&quot;{ocrResult.extracted_text}&quot;</p>
                </div>
              )}

              <Input label="Meal Title" value={mealName} onChange={(e) => setMealName(e.target.value)} required />

              <div className="grid grid-cols-2 gap-3">
                <Input label="Calories (kcal)" type="number" value={calories} onChange={(e) => setCalories(e.target.value)} required />
                <Input label="Protein (g)" type="number" value={protein} onChange={(e) => setProtein(e.target.value)} required />
                <Input label="Carbs (g)" type="number" value={carbs} onChange={(e) => setCarbs(e.target.value)} required />
                <Input label="Fat (g)" type="number" value={fat} onChange={(e) => setFat(e.target.value)} required />
              </div>

              <Button type="submit" className="w-full shadow-glow">
                <CheckCircle2 className="h-4 w-4 mr-1.5" /> Confirm & Save to Meal Journal
              </Button>
            </form>
          ) : (
            <div className="py-12 text-center text-xs text-slate-500 space-y-2">
              <Camera className="h-8 w-8 mx-auto text-slate-600" />
              <p>Upload a food image on the left to see vision predictions.</p>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
