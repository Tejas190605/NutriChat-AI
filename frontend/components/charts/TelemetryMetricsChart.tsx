"use client";

import React from "react";
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Legend } from "recharts";
import { ChartCard } from "../ui/chart-card";

export interface TelemetryDataPoint {
  date: string;
  requests: number;
  tokens: number;
  latency_ms: number;
}

export interface TelemetryMetricsChartProps {
  data: TelemetryDataPoint[];
  title?: string;
  className?: string;
}

export const TelemetryMetricsChart: React.FC<TelemetryMetricsChartProps> = ({
  data,
  title = "AI Model Engine Telemetry & Latency",
  className,
}) => {
  return (
    <ChartCard title={title} description="Daily API execution requests and average response latency (ms)" className={className}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <XAxis dataKey="date" stroke="#64748b" fontSize={12} tickLine={false} />
          <YAxis stroke="#64748b" fontSize={12} tickLine={false} />
          <Tooltip
            contentStyle={{
              backgroundColor: "#0f172a",
              borderColor: "#1e293b",
              borderRadius: "8px",
              color: "#f8fafc",
            }}
          />
          <Legend wrapperStyle={{ color: "#94a3b8", fontSize: "12px" }} />
          <Bar dataKey="requests" name="Total Requests" fill="#10b981" radius={[4, 4, 0, 0]} />
          <Bar dataKey="latency_ms" name="Avg Latency (ms)" fill="#a855f7" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </ChartCard>
  );
};
