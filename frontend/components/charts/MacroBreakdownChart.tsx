"use client";

import React from "react";
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip, Legend } from "recharts";
import { ChartCard } from "../ui/chart-card";

export interface MacroBreakdownChartProps {
  protein: number;
  carbs: number;
  fat: number;
  title?: string;
  className?: string;
}

const COLORS = ["#10b981", "#06b6d4", "#a855f7"];

export const MacroBreakdownChart: React.FC<MacroBreakdownChartProps> = ({
  protein,
  carbs,
  fat,
  title = "Macronutrient Distribution",
  className,
}) => {
  const data = [
    { name: "Protein (g)", value: protein },
    { name: "Carbs (g)", value: carbs },
    { name: "Fat (g)", value: fat },
  ];

  return (
    <ChartCard title={title} description="Ratio split between Protein, Carbs, and Fats" className={className}>
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie data={data} cx="50%" cy="50%" innerRadius={55} outerRadius={80} paddingAngle={4} dataKey="value">
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              backgroundColor: "#0f172a",
              borderColor: "#1e293b",
              borderRadius: "8px",
              color: "#f8fafc",
            }}
          />
          <Legend wrapperStyle={{ color: "#94a3b8", fontSize: "12px" }} />
        </PieChart>
      </ResponsiveContainer>
    </ChartCard>
  );
};
