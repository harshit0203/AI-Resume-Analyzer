"use client";

import {
  PolarAngleAxis,
  PolarGrid,
  Radar,
  RadarChart,
  ResponsiveContainer,
} from "recharts";

export interface RadarDatum {
  axis: string;
  value: number;
}

export function SkillRadar({ data }: { data: RadarDatum[] }) {
  return (
    <ResponsiveContainer width="100%" height={280}>
      <RadarChart data={data} outerRadius="72%">
        <PolarGrid stroke="var(--border)" />
        <PolarAngleAxis
          dataKey="axis"
          tick={{ fill: "var(--muted-foreground)", fontSize: 11 }}
        />
        <Radar
          dataKey="value"
          stroke="var(--primary)"
          fill="var(--primary)"
          fillOpacity={0.35}
          strokeWidth={2}
        />
      </RadarChart>
    </ResponsiveContainer>
  );
}
