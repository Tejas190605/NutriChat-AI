"use client";

import React, { useEffect, useState } from "react";
import { nutritionService } from "@/services/nutrition.service";
import { FoodItem, FoodCategory, Ingredient, BarcodeProduct, RestaurantMenu } from "@/types/nutrition";
import { DataTable, Column } from "@/components/data/DataTable";
import { Tabs } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Modal } from "@/components/ui/modal";
import { Input } from "@/components/ui/input";
import { Utensils, Plus, CheckCircle2, QrCode, Store, Layers } from "lucide-react";

export default function NutritionPage() {
  const [activeTab, setActiveTab] = useState("foods");
  const [foods, setFoods] = useState<FoodItem[]>([]);
  const [categories, setCategories] = useState<FoodCategory[]>([]);
  const [ingredients, setIngredients] = useState<Ingredient[]>([]);
  const [barcodes, setBarcodes] = useState<BarcodeProduct[]>([]);
  const [menus, setMenus] = useState<RestaurantMenu[]>([]);

  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [newFoodName, setNewFoodName] = useState("");
  const [newCalories, setNewCalories] = useState("");
  const [newProtein, setNewProtein] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      const f = await nutritionService.getFoods();
      const c = await nutritionService.getCategories();
      const i = await nutritionService.getIngredients();
      const b = await nutritionService.getBarcodeProducts();
      const m = await nutritionService.getRestaurantMenus();
      setFoods(f);
      setCategories(c);
      setIngredients(i);
      setBarcodes(b);
      setMenus(m);
    };
    fetchData();
  }, []);

  const handleAddFood = (e: React.FormEvent) => {
    e.preventDefault();
    const newItem: FoodItem = {
      id: `f-new-${Date.now()}`,
      name: newFoodName,
      calories: Number(newCalories) || 200,
      protein: Number(newProtein) || 15,
      carbs: 20,
      fat: 5,
      serving_size: "1 portion (100g)",
      serving_weight_g: 100,
      is_verified: true,
    };
    setFoods([newItem, ...foods]);
    setIsAddModalOpen(false);
    setNewFoodName("");
    setNewCalories("");
    setNewProtein("");
  };

  const foodColumns: Column<FoodItem>[] = [
    { header: "Food Name", accessorKey: "name", className: "font-semibold text-white", sortable: true },
    { header: "Category", accessorKey: "category_name" },
    { header: "Calories", accessorKey: "calories", className: "text-amber-400 font-bold", sortable: true },
    { header: "Protein (g)", accessorKey: "protein", sortable: true },
    { header: "Carbs (g)", accessorKey: "carbs" },
    { header: "Fat (g)", accessorKey: "fat" },
    { header: "Serving Size", accessorKey: "serving_size" },
    {
      header: "Verified",
      cell: (item) => (
        item.is_verified ? (
          <span className="inline-flex items-center gap-1 text-emerald-400 text-xs"><CheckCircle2 className="h-3.5 w-3.5" /> Verified</span>
        ) : null
      ),
    },
  ];

  const categoryColumns: Column<FoodCategory>[] = [
    { header: "Category Name", accessorKey: "name", className: "font-semibold text-white", sortable: true },
    { header: "Description", accessorKey: "description" },
    { header: "Item Count", accessorKey: "item_count", className: "text-emerald-400 font-bold" },
  ];

  const ingredientColumns: Column<Ingredient>[] = [
    { header: "Ingredient Name", accessorKey: "name", className: "font-semibold text-white", sortable: true },
    { header: "Calories / 100g", accessorKey: "calories_per_100g", className: "text-amber-400 font-bold" },
    { header: "Protein / 100g", accessorKey: "protein_per_100g" },
    { header: "Carbs / 100g", accessorKey: "carbs_per_100g" },
    { header: "Fat / 100g", accessorKey: "fat_per_100g" },
  ];

  const barcodeColumns: Column<BarcodeProduct>[] = [
    { header: "Barcode GTIN", accessorKey: "barcode", className: "font-mono text-cyan-400 font-bold", sortable: true },
    { header: "Product Name", accessorKey: "product_name", className: "text-white font-semibold" },
    { header: "Brand", accessorKey: "brand" },
    { header: "Calories", cell: (item) => item.nutrition.calories },
    { header: "Protein (g)", cell: (item) => item.nutrition.protein },
  ];

  const menuColumns: Column<RestaurantMenu>[] = [
    { header: "Restaurant", accessorKey: "restaurant_name", className: "font-semibold text-white" },
    { header: "Item Name", accessorKey: "item_name" },
    { header: "Price (₹)", accessorKey: "price", className: "text-emerald-400 font-bold" },
    { header: "Calories", accessorKey: "calories", className: "text-amber-400" },
    { header: "Protein (g)", accessorKey: "protein" },
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-6 rounded-2xl glass-card border border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Utensils className="h-6 w-6 text-emerald-400" /> Nutrition Database Management
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Manage foods, categories, ingredients, restaurant menus, and barcode lookup database.
          </p>
        </div>
        <Button size="sm" onClick={() => setIsAddModalOpen(true)}>
          <Plus className="h-4 w-4 mr-1.5" /> Add New Food
        </Button>
      </div>

      <Tabs
        tabs={[
          { id: "foods", label: "Foods Library", icon: Utensils },
          { id: "categories", label: "Categories", icon: Layers },
          { id: "ingredients", label: "Ingredients", icon: Utensils },
          { id: "barcodes", label: "Barcode Products", icon: QrCode },
          { id: "menus", label: "Restaurant Menus", icon: Store },
        ]}
        activeTab={activeTab}
        onChange={setActiveTab}
      />

      {activeTab === "foods" && (
        <DataTable title="Verified Food Items" columns={foodColumns} data={foods} keyExtractor={(f) => f.id} />
      )}
      {activeTab === "categories" && (
        <DataTable title="Food Categories" columns={categoryColumns} data={categories} keyExtractor={(c) => c.id} />
      )}
      {activeTab === "ingredients" && (
        <DataTable title="Base Ingredients" columns={ingredientColumns} data={ingredients} keyExtractor={(i) => i.id} />
      )}
      {activeTab === "barcodes" && (
        <DataTable title="Barcode GTIN Registry" columns={barcodeColumns} data={barcodes} keyExtractor={(b) => b.id} />
      )}
      {activeTab === "menus" && (
        <DataTable title="Restaurant Menus" columns={menuColumns} data={menus} keyExtractor={(m) => m.id} />
      )}

      {/* Add Food Modal */}
      <Modal isOpen={isAddModalOpen} onClose={() => setIsAddModalOpen(false)} title="Add Food Item to Database">
        <form onSubmit={handleAddFood} className="space-y-4">
          <Input label="Food Name" placeholder="e.g., Masala Oats" value={newFoodName} onChange={(e) => setNewFoodName(e.target.value)} required />
          <Input label="Calories (kcal)" type="number" placeholder="240" value={newCalories} onChange={(e) => setNewCalories(e.target.value)} required />
          <Input label="Protein (g)" type="number" placeholder="10" value={newProtein} onChange={(e) => setNewProtein(e.target.value)} required />
          <div className="flex justify-end gap-3 pt-3">
            <Button type="button" variant="outline" onClick={() => setIsAddModalOpen(false)}>Cancel</Button>
            <Button type="submit">Save Food Item</Button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
