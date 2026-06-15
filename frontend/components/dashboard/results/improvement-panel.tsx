"use client";

import { ArrowRight, Wand2 } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { ImprovementResult } from "@/lib/types";

export function ImprovementPanel({ result }: { result: ImprovementResult }) {
  return (
    <div className="space-y-4">
      {result.improved_summary && (
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center gap-2 text-sm">
              <Wand2 className="size-4 text-primary" /> Suggested summary
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="rounded-lg bg-secondary/40 p-4 text-sm leading-relaxed">
              {result.improved_summary}
            </p>
          </CardContent>
        </Card>
      )}

      {result.stronger_bullets?.length > 0 && (
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm">Stronger bullet points</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {result.stronger_bullets.map((bullet, i) => (
              <div key={i} className="grid gap-2 rounded-lg border border-border p-3 sm:grid-cols-[1fr_auto_1fr] sm:items-center">
                <p className="text-sm text-muted-foreground line-through decoration-rose-400/50">
                  {bullet.before}
                </p>
                <ArrowRight className="hidden size-4 text-muted-foreground sm:block" />
                <p className="text-sm text-emerald-300">{bullet.after}</p>
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      <div className="grid gap-4 sm:grid-cols-2">
        {result.achievement_suggestions?.length > 0 && (
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm">Achievement ideas</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                {result.achievement_suggestions.map((s, i) => (
                  <li key={i}>• {s}</li>
                ))}
              </ul>
            </CardContent>
          </Card>
        )}
        {result.ats_keywords?.length > 0 && (
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm">ATS keywords to add</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-wrap gap-2">
              {result.ats_keywords.map((kw) => (
                <Badge key={kw} variant="default">
                  {kw}
                </Badge>
              ))}
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
