"use client";

import React, { useEffect, useState } from "react";
import { visionService } from "@/services/vision.service";
import { FoodImage, BarcodeScan } from "@/types/vision";
import { DataTable, Column } from "@/components/data/DataTable";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { Eye, QrCode, Scan, CheckCircle2, FileText } from "lucide-react";
import Image from "next/image";

export default function VisionPage() {
  const [images, setImages] = useState<FoodImage[]>([]);
  const [barcodes, setBarcodes] = useState<BarcodeScan[]>([]);

  useEffect(() => {
    const load = async () => {
      const imgList = await visionService.getFoodImages();
      const bcList = await visionService.getBarcodeScans();
      setImages(imgList);
      setBarcodes(bcList);
    };
    load();
  }, []);

  const barcodeColumns: Column<BarcodeScan>[] = [
    { header: "Barcode GTIN", accessorKey: "barcode", className: "font-mono font-bold text-cyan-400" },
    { header: "Product Match", accessorKey: "product_name", className: "font-semibold text-white" },
    { header: "Scanned Time", cell: (item) => new Date(item.scanned_at).toLocaleString() },
    {
      header: "Status",
      cell: (item) => (
        <Badge variant={item.status === "matched" ? "success" : "error"}>
          {item.status.toUpperCase()}
        </Badge>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between p-6 rounded-2xl glass-card border border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Eye className="h-6 w-6 text-emerald-400" /> Computer Vision & OCR Analysis Pipeline
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Food photo segmentation bounding boxes, OCR nutrition facts extraction, and GTIN barcode scans.
          </p>
        </div>
        <Badge variant="success">Cloudinary & Google Vision Ready</Badge>
      </div>

      {/* Uploaded Food Image Cards Gallery */}
      <div className="space-y-3">
        <h3 className="text-sm font-bold text-white flex items-center gap-2">
          <Scan className="h-4 w-4 text-emerald-400" /> Uploaded Meal Photos & Vision Annotations
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {images.map((img) => (
            <Card key={img.id} className="p-5 border border-slate-800 space-y-4">
              <div className="flex gap-4">
                <div className="relative h-28 w-28 rounded-xl overflow-hidden border border-slate-700 flex-shrink-0 bg-slate-900">
                  <Image src={img.image_url} alt="Food Upload" fill className="object-cover" />
                </div>
                <div className="space-y-1.5 flex-1 text-xs">
                  <div className="flex justify-between items-center">
                    <span className="font-mono text-slate-400">ID: {img.id}</span>
                    <Badge variant="success" className="capitalize">{img.status}</Badge>
                  </div>

                  {img.predictions && img.predictions.length > 0 && (
                    <div className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800 space-y-1">
                      <p className="font-bold text-emerald-400">{img.predictions[0].label}</p>
                      <p className="text-slate-300">Confidence: {(img.predictions[0].confidence * 100).toFixed(0)}%</p>
                      <p className="text-slate-400">{img.predictions[0].calories} kcal ({img.predictions[0].portion})</p>
                    </div>
                  )}
                </div>
              </div>

              {img.ocr_result && (
                <div className="p-3 rounded-xl bg-slate-900/50 border border-slate-800/80 text-xs space-y-1">
                  <div className="flex items-center gap-1.5 text-cyan-400 font-semibold">
                    <FileText className="h-3.5 w-3.5" /> OCR Extracted Text
                  </div>
                  <p className="text-slate-300 italic">&quot;{img.ocr_result.extracted_text}&quot;</p>
                </div>
              )}
            </Card>
          ))}
        </div>
      </div>

      {/* Barcode Scans History */}
      <DataTable title="GTIN Barcode Scanning Telemetry" columns={barcodeColumns} data={barcodes} keyExtractor={(b) => b.id} />
    </div>
  );
}
