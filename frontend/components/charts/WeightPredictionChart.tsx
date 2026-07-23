"use client";

import React from "react";
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, Legend } from "recharts";
import { ChartCard } from "../ui/chart-card";

export interface WeightDataPoint {
  date: string;
  actual?: number;
  predicted: number;
}

export interface WeightPredictionChartProps {
  data: WeightDataPoint[];
  title?: string;
  className?: string;
}

export const WeightPredictionChart: React.FC<WeightPredictionChartProps> = ({
  data,
  title = "Weight Trend & AI Forecast Trajectory",
  className,
}) => {
  return (
    <ChartCard title={title} description="Actual body weight vs estimated 14-day trajectory forecast" className={className}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <XAxis dataKey="date" stroke="#64748b" fontSize={12} tickLine={false} />
          <YAxis stroke="#64748b" fontSize={12} tickLine={false} domain={["dataMin - 1", "dataMax + 1"]} />
          <Tooltip
            contentStyle={{
              backgroundColor: "#0f172a",
              borderColor: "#1e293b",
              borderRadius: "8px",
              color: "#f8fafc",
            }}
          />
          <Legend wrapperStyle={{ color: "#94a3b8", fontSize: "12px" }} />
          <Line type="monotone" dataKey="actual" name="Logged Weight (kg)" stroke="#10b981" strokeWidth={3} dot={{ r: 4 }} />
          <Line type="monotone" dataKey="predicted" name="Predicted Trajectory (kg)" stroke="#06b6d4" strokeWidth={2} strokeDasharray="5 5" />
        </LineChart>
      </ResponsiveContainer>
    </ChartCard>
  );
};
