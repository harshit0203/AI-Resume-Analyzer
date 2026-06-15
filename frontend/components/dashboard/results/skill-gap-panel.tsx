"use client";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { SkillRadar, type RadarDatum } from "@/components/charts/skill-radar";
import type { SkillGapResult } from "@/lib/types";

export function SkillGapPanel({ result }: { result: SkillGapResult }) {
  const matched = result.matched_skills?.length ?? 0;
  const missing = result.missing_skills?.length ?? 0;
  const total = matched + missing || 1;

  const radarData: RadarDatum[] = [
    { axis: "Coverage", value: result.coverage_percentage },
    { axis: "Matched", value: (matched / total) * 100 },
    { axis: "Breadth", value: Math.min(100, matched * 12) },
    { axis: "Readiness", value: result.coverage_percentage * 0.9 },
    { axis: "Depth", value: Math.min(100, matched * 10) },
  ];

  return (
    <div className="grid gap-4 lg:grid-cols-2">
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm">
            Skill coverage · {result.target_path ?? "Target path"}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <SkillRadar data={radarData} />
          <div className="mt-2">
            <div className="mb-1 flex items-center justify-between text-xs">
              <span className="text-muted-foreground">Coverage</span>
              <span className="font-medium">{Math.round(result.coverage_percentage)}%</span>
            </div>
            <Progress value={result.coverage_percentage} />
          </div>
        </CardContent>
      </Card>

      <div className="space-y-4">
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm">Matched skills</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-wrap gap-2">
            {matched ? (
              result.matched_skills.map((s) => (
                <Badge key={s} variant="success">
                  {s}
                </Badge>
              ))
            ) : (
              <p className="text-sm text-muted-foreground">No matched skills detected yet.</p>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm">Skills to learn</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {missing ? (
              result.missing_skills.map((item) => (
                <div key={item.skill} className="rounded-lg border border-border p-3">
                  <div className="flex items-center justify-between">
                    <span className="font-medium capitalize">{item.skill}</span>
                    <Badge variant={item.importance === "high" ? "danger" : "warning"}>
                      {item.importance}
                    </Badge>
                  </div>
                  {item.resources?.length > 0 && (
                    <p className="mt-1 text-xs text-muted-foreground">
                      Resources: {item.resources.join(", ")}
                    </p>
                  )}
                </div>
              ))
            ) : (
              <p className="text-sm text-muted-foreground">You cover all key skills. 🎯</p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
