"use client";

import React, { useState } from "react";
import { UploadCloud, Image as ImageIcon, CheckCircle2, AlertCircle } from "lucide-react";
import { Button } from "../ui/button";
import Image from "next/image";

export interface ImageUploaderProps {
  onFileSelect: (file: File) => void;
  isLoading?: boolean;
}

export const ImageUploader: React.FC<ImageUploaderProps> = ({ onFileSelect, isLoading }) => {
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.type.startsWith("image/")) {
      setError("Please select a valid image file (JPEG, PNG, WebP).");
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setError("File size exceeds maximum threshold of 10MB.");
      return;
    }

    setError(null);
    setPreviewUrl(URL.createObjectURL(file));
    onFileSelect(file);
  };

  return (
    <div className="space-y-3">
      <label className="border-2 border-dashed border-slate-800 hover:border-emerald-500/50 rounded-2xl p-6 flex flex-col items-center justify-center cursor-pointer transition-colors bg-slate-950/60 text-center">
        <input type="file" accept="image/*" onChange={handleFileChange} className="hidden" />

        {previewUrl ? (
          <div className="relative h-40 w-40 rounded-xl overflow-hidden border border-slate-700 mb-3">
            <Image src={previewUrl} alt="Meal Upload Preview" fill className="object-cover" />
          </div>
        ) : (
          <div className="p-4 rounded-full bg-emerald-500/10 text-emerald-400 mb-3">
            <UploadCloud className="h-8 w-8" />
          </div>
        )}

        <h4 className="text-sm font-bold text-white">
          {previewUrl ? "Change Selected Image" : "Drop food photo here or click to browse"}
        </h4>
        <p className="text-xs text-slate-500 mt-1">Supports JPG, PNG, WEBP up to 10MB</p>

        {previewUrl && (
          <div className="mt-3 inline-flex items-center gap-1 text-xs text-emerald-400 font-semibold">
            <CheckCircle2 className="h-4 w-4" /> Ready for AI Vision & OCR Extraction
          </div>
        )}
      </label>

      {error && (
        <div className="flex items-center gap-2 text-xs text-rose-400 bg-rose-950/40 border border-rose-800/50 p-3 rounded-xl">
          <AlertCircle className="h-4 w-4 flex-shrink-0" /> {error}
        </div>
      )}
    </div>
  );
};
