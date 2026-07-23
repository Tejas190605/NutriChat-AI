export interface FoodCategory {
  id: string;
  name: string;
  description?: string;
  icon_name?: string;
  item_count?: number;
}

export interface FoodItem {
  id: string;
  name: string;
  category_id?: string;
  category_name?: string;
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
  fiber?: number;
  serving_size: string;
  serving_weight_g: number;
  brand?: string;
  is_verified?: boolean;
}

export interface Ingredient {
  id: string;
  name: string;
  calories_per_100g: number;
  protein_per_100g: number;
  carbs_per_100g: number;
  fat_per_100g: number;
  allergens?: string[];
}

export interface BarcodeProduct {
  id: string;
  barcode: string;
  product_name: string;
  brand?: string;
  nutrition: {
    calories: number;
    protein: number;
    carbs: number;
    fat: number;
  };
  image_url?: string;
}

export interface RestaurantMenu {
  id: string;
  restaurant_name: string;
  item_name: string;
  price?: number;
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
}
