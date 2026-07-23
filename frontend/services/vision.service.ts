import apiClient from "@/lib/api/axios";
import { FoodImage, BarcodeScan } from "@/types/vision";

export const visionService = {
  getFoodImages: async (): Promise<FoodImage[]> => {
    try {
      const response = await apiClient.get("/vision/images");
      return response.data;
    } catch {
      return [
        {
          id: "img-201",
          user_id: "u-101",
          image_url: "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=400&q=80",
          status: "analyzed",
          uploaded_at: "2026-07-23T12:30:00Z",
          predictions: [
            { label: "Chicken Salad", confidence: 0.94, portion: "1 bowl", weight_grams: 320, calories: 420 },
          ],
          ocr_result: {
            id: "ocr-1",
            image_id: "img-201",
            extracted_text: "Fresh Grilled Chicken Salad 320g",
            confidence: 0.98,
          },
        },
      ];
    }
  },

  getBarcodeScans: async (): Promise<BarcodeScan[]> => {
    return [
      { id: "bs-1", barcode: "8901058000123", scanned_at: "2026-07-23T10:15:00Z", product_name: "Amul Protein Lassi", status: "matched" },
      { id: "bs-2", barcode: "8901030829101", scanned_at: "2026-07-22T18:40:00Z", product_name: "Epigamia Greek Yogurt", status: "matched" },
    ];
  },

  uploadImage: async (file: File): Promise<{ image_id: string; image_url: string }> => {
    const formData = new FormData();
    formData.append("file", file);
    const response = await apiClient.post("/vision/upload", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return response.data;
  },
};
