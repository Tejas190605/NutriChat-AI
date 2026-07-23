export interface VisionPrediction {
  label: string;
  confidence: number;
  portion: string;
  weight_grams: number;
  calories: number;
  bounding_box?: {
    x_min: number;
    y_min: number;
    x_max: number;
    y_max: number;
  };
}

export interface OCRResult {
  id: string;
  image_id: string;
  extracted_text: string;
  nutrition_facts?: {
    calories?: number;
    protein_g?: number;
    carbs_g?: number;
    fat_g?: number;
    serving_size?: string;
  };
  confidence: number;
}

export interface FoodImage {
  id: string;
  user_id: string;
  image_url: string;
  status: "uploaded" | "processing" | "analyzed" | "failed";
  uploaded_at: string;
  predictions?: VisionPrediction[];
  ocr_result?: OCRResult;
}

export interface BarcodeScan {
  id: string;
  barcode: string;
  scanned_at: string;
  product_name?: string;
  status: "matched" | "not_found";
}
