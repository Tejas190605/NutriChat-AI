"use client";

import React from "react";
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip } from "recharts";
import { ChartCard } from "../ui/chart-card";

export interface CalorieDataPoint {
  day: string;
  calories: number;
  target?: number;
}

export interface CalorieTrendChartProps {
  data: CalorieDataPoint[];
  title?: string;
  description?: string;
  className?: string;
}

export const CalorieTrendChart: React.FC<CalorieTrendChartProps> = ({
  data,
  title = "Calorie Consumption Trend",
  description = "Daily intake vs target calorie budget",
  className,
}) => {
  return (
    <ChartCard title={title} description={description} className={className}>
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data}>
          <defs>
            <linearGradient id="calorieGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#10b981" stopOpacity={0.4} />
              <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
            </linearGradient>
          </defs>
          <XAxis dataKey="day" stroke="#64748b" fontSize={12} tickLine={false} />
          <YAxis stroke="#64748b" fontSize={12} tickLine={false} />
          <Tooltip
            contentStyle={{
              backgroundColor: "#0f172a",
              borderColor: "#1e293b",
              borderRadius: "8px",
              color: "#f8fafc",
            }}
          />
          <Area type="monotone" dataKey="calories" stroke="#10b981" strokeWidth={2} fill="url(#calorieGrad)" />
        </AreaChart>
      </ResponsiveContainer>
    </ChartCard>
  );
};
