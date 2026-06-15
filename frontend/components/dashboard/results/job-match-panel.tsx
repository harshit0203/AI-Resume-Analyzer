"use client";

import { Briefcase, TrendingUp } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import type { JobMatch } from "@/lib/types";
import { cn, scoreColor } from "@/lib/utils";

export function JobMatchPanel({ matches }: { matches: JobMatch[] }) {
  if (!matches.length) {
    return <p className="text-sm text-muted-foreground">No job matches generated.</p>;
  }
  return (
    <div className="grid gap-4 md:grid-cols-2">
      {matches.map((job) => (
        <Card key={job.id} className="transition-colors hover:border-primary/40">
          <CardContent className="p-5">
            <div className="flex items-start justify-between gap-3">
              <div className="flex items-center gap-3">
                <div className="flex size-10 items-center justify-center rounded-xl bg-primary/10 text-primary">
                  <Briefcase className="size-5" />
                </div>
                <div>
                  <h3 className="font-medium leading-tight">{job.title}</h3>
                  <p className="text-xs text-muted-foreground">
                    {job.seniority ? `${job.seniority} · ` : ""}
                    {job.company_type ?? ""}
                  </p>
                </div>
              </div>
              <span className={cn("text-xl font-semibold tabular-nums", scoreColor(job.match_percentage))}>
                {Math.round(job.match_percentage)}%
              </span>
            </div>

            <Progress value={job.match_percentage} className="mt-4" />

            {job.salary_range && (
              <p className="mt-3 flex items-center gap-1.5 text-sm text-muted-foreground">
                <TrendingUp className="size-3.5 text-emerald-400" /> {job.salary_range}
              </p>
            )}

            {job.reasons?.length > 0 && (
              <ul className="mt-3 space-y-1">
                {job.reasons.slice(0, 2).map((r, i) => (
                  <li key={i} className="text-xs text-muted-foreground">
                    • {r}
                  </li>
                ))}
              </ul>
            )}

            {job.missing_skills?.length > 0 && (
              <div className="mt-3 flex flex-wrap gap-1.5">
                {job.missing_skills.slice(0, 5).map((s) => (
                  <Badge key={s} variant="secondary" className="text-[10px]">
                    {s}
                  </Badge>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
