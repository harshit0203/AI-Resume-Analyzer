"use client";

import { Award, DollarSign, GraduationCap, Milestone, Rocket } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { CareerInsight } from "@/lib/types";

export function CareerPanel({ insight }: { insight: CareerInsight }) {
  const salary = (insight.salary_insights ?? {}) as Record<string, string>;

  return (
    <div className="space-y-4">
      {insight.narrative && (
        <Card className="border-primary/30">
          <CardContent className="p-5">
            <p className="text-sm leading-relaxed">{insight.narrative}</p>
            <div className="mt-3 flex flex-wrap gap-2">
              {insight.current_level && <Badge variant="default">Level: {insight.current_level}</Badge>}
              {insight.target_role && <Badge variant="secondary">Target: {insight.target_role}</Badge>}
            </div>
          </CardContent>
        </Card>
      )}

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center gap-2 text-sm">
              <DollarSign className="size-4 text-emerald-400" /> Salary insights
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2 text-sm">
            {Object.keys(salary).length ? (
              Object.entries(salary).map(([k, v]) => (
                <div key={k} className="flex justify-between border-b border-border/60 pb-1.5 last:border-0">
                  <span className="capitalize text-muted-foreground">{k.replace(/_/g, " ")}</span>
                  <span className="font-medium">{String(v)}</span>
                </div>
              ))
            ) : (
              <p className="text-muted-foreground">No salary data available.</p>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center gap-2 text-sm">
              <Rocket className="size-4 text-primary" /> Next steps
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2 text-sm text-muted-foreground">
              {insight.next_steps.map((s, i) => (
                <li key={i}>• {s}</li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </div>

      {insight.roadmap?.length > 0 && (
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center gap-2 text-sm">
              <Milestone className="size-4 text-sky-400" /> Growth roadmap
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {insight.roadmap.map((step, i) => {
                const s = step as Record<string, string>;
                return (
                  <div key={i} className="flex gap-3">
                    <div className="flex size-7 shrink-0 items-center justify-center rounded-full bg-primary/15 text-xs font-medium text-primary">
                      {i + 1}
                    </div>
                    <div>
                      <p className="text-sm font-medium">{s.horizon ?? s.phase ?? `Step ${i + 1}`}</p>
                      <p className="text-sm text-muted-foreground">{s.goal ?? s.focus ?? s.outcome}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      )}

      <div className="grid gap-4 md:grid-cols-2">
        {insight.recommended_certifications?.length > 0 && (
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center gap-2 text-sm">
                <Award className="size-4 text-amber-400" /> Certifications
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                {insight.recommended_certifications.map((c, i) => (
                  <li key={i}>• {c}</li>
                ))}
              </ul>
            </CardContent>
          </Card>
        )}
        {insight.growth_recommendations?.length > 0 && (
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center gap-2 text-sm">
                <GraduationCap className="size-4 text-primary" /> Growth tips
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                {insight.growth_recommendations.map((g, i) => (
                  <li key={i}>• {g}</li>
                ))}
              </ul>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
