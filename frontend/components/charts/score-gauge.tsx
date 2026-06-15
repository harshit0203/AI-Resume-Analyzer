"use client";

import { RadialBar, RadialBarChart, PolarAngleAxis, ResponsiveContainer } from "recharts";

import { cn } from "@/lib/utils";

function gaugeColor(score: number) {
  if (score >= 80) return "oklch(0.72 0.17 155)";
  if (score >= 60) return "oklch(0.8 0.15 85)";
  return "oklch(0.65 0.2 20)";
}

export function ScoreGauge({
  score,
  size = 180,
  label = "ATS Score",
}: {
  score: number;
  size?: number;
  label?: string;
}) {
  const value = Math.round(score);
  const data = [{ name: label, value, fill: gaugeColor(value) }];

  return (
    <div className="relative" style={{ width: size, height: size }}>
      <ResponsiveContainer width="100%" height="100%">
        <RadialBarChart
          innerRadius="72%"
          outerRadius="100%"
          data={data}
          startAngle={220}
          endAngle={-40}
        >
          <PolarAngleAxis type="number" domain={[0, 100]} tick={false} />
          <RadialBar background={{ fill: "var(--secondary)" }} dataKey="value" cornerRadius={20} />
        </RadialBarChart>
      </ResponsiveContainer>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className={cn("text-4xl font-semibold tabular-nums")} style={{ color: gaugeColor(value) }}>
          {value}
        </span>
        <span className="text-xs text-muted-foreground">{label}</span>
      </div>
    </div>
  );
}
