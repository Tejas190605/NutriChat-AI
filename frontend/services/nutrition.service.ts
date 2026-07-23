import apiClient from "@/lib/api/axios";
import { FoodItem, FoodCategory, Ingredient, BarcodeProduct, RestaurantMenu } from "@/types/nutrition";

export const nutritionService = {
  getFoods: async (search = ""): Promise<FoodItem[]> => {
    try {
      const response = await apiClient.get("/nutrition/foods", { params: { search } });
      return response.data;
    } catch {
      return [
        {
          id: "f-1",
          name: "Paneer Tikka",
          category_name: "Indian Special",
          calories: 320,
          protein: 18.5,
          carbs: 8.0,
          fat: 22.0,
          serving_size: "1 plate (200g)",
          serving_weight_g: 200,
          is_verified: true,
        },
        {
          id: "f-2",
          name: "Roti (Whole Wheat)",
          category_name: "Breads",
          calories: 120,
          protein: 3.5,
          carbs: 22.0,
          fat: 1.2,
          serving_size: "1 roti (40g)",
          serving_weight_g: 40,
          is_verified: true,
        },
        {
          id: "f-3",
          name: "Greek Yogurt (Plain)",
          category_name: "Dairy",
          calories: 130,
          protein: 17.0,
          carbs: 6.0,
          fat: 4.0,
          serving_size: "1 cup (170g)",
          serving_weight_g: 170,
          is_verified: true,
        },
      ];
    }
  },

  getCategories: async (): Promise<FoodCategory[]> => {
    try {
      const response = await apiClient.get("/nutrition/categories");
      return response.data;
    } catch {
      return [
        { id: "c-1", name: "Indian Special", description: "Traditional curries and paneer dishes", item_count: 42 },
        { id: "c-2", name: "Breads & Grains", description: "Rotis, parathas, and rice", item_count: 28 },
        { id: "c-3", name: "Dairy & Eggs", description: "Milk, curd, paneer, eggs", item_count: 35 },
      ];
    }
  },

  getIngredients: async (): Promise<Ingredient[]> => {
    try {
      const response = await apiClient.get("/nutrition/ingredients");
      return response.data;
    } catch {
      return [
        { id: "i-1", name: "Cottage Cheese (Paneer)", calories_per_100g: 265, protein_per_100g: 18, carbs_per_100g: 3, fat_per_100g: 20 },
        { id: "i-2", name: "Whole Wheat Flour", calories_per_100g: 340, protein_per_100g: 13, carbs_per_100g: 72, fat_per_100g: 2.5 },
      ];
    }
  },

  getBarcodeProducts: async (): Promise<BarcodeProduct[]> => {
    try {
      const response = await apiClient.get("/nutrition/barcodes");
      return response.data;
    } catch {
      return [
        {
          id: "b-1",
          barcode: "8901058000123",
          product_name: "Amul Protein Lassi",
          brand: "Amul",
          nutrition: { calories: 110, protein: 15.0, carbs: 12.0, fat: 0.5 },
        },
      ];
    }
  },

  getRestaurantMenus: async (): Promise<RestaurantMenu[]> => {
    try {
      const response = await apiClient.get("/nutrition/menus");
      return response.data;
    } catch {
      return [
        { id: "m-1", restaurant_name: "Haldiram's", item_name: "Chole Bhature", price: 180, calories: 750, protein: 18, carbs: 85, fat: 38 },
      ];
    }
  },
};
