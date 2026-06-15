"use client";

import { AlertTriangle, CheckCircle2, KeyRound, Lightbulb } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScoreGauge } from "@/components/charts/score-gauge";
import type { ATSResult } from "@/lib/types";

export function AtsPanel({ result }: { result: ATSResult }) {
  return (
    <div className="grid gap-4 lg:grid-cols-[280px_1fr]">
      <Card>
        <CardContent className="flex flex-col items-center justify-center p-6">
          <ScoreGauge score={result.ats_score} />
          <p className="mt-2 text-center text-sm text-muted-foreground">
            ATS compatibility score based on structure, keywords and content quality.
          </p>
        </CardContent>
      </Card>

      <div className="grid gap-4 sm:grid-cols-2">
        <ListCard icon={CheckCircle2} title="Strengths" items={result.strengths} tone="text-emerald-400" />
        <ListCard icon={AlertTriangle} title="Weaknesses" items={result.weaknesses} tone="text-amber-400" />
        <Card className="sm:col-span-2">
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center gap-2 text-sm">
              <KeyRound className="size-4 text-sky-400" /> Missing keywords
            </CardTitle>
          </CardHeader>
          <CardContent className="flex flex-wrap gap-2">
            {result.missing_keywords.length ? (
              result.missing_keywords.map((kw) => (
                <Badge key={kw} variant="secondary">
                  {kw}
                </Badge>
              ))
            ) : (
              <p className="text-sm text-muted-foreground">No critical keywords missing. 🎉</p>
            )}
          </CardContent>
        </Card>
        <ListCard
          icon={Lightbulb}
          title="Recommendations"
          items={result.recommendations}
          tone="text-primary"
          className="sm:col-span-2"
        />
      </div>
    </div>
  );
}

function ListCard({
  icon: Icon,
  title,
  items,
  tone,
  className,
}: {
  icon: typeof CheckCircle2;
  title: string;
  items: string[];
  tone: string;
  className?: string;
}) {
  return (
    <Card className={className}>
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center gap-2 text-sm">
          <Icon className={`size-4 ${tone}`} /> {title}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ul className="space-y-2">
          {items.map((item, i) => (
            <li key={i} className="flex gap-2 text-sm text-muted-foreground">
              <span className={`mt-1.5 size-1.5 shrink-0 rounded-full ${tone.replace("text", "bg")}`} />
              {item}
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
}
