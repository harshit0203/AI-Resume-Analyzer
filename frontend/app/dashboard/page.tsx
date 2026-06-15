"use client";

import Link from "next/link";
import { Activity, Award, FileText, Gauge, ScanText, TrendingUp } from "lucide-react";

import { PageHeader } from "@/components/dashboard/page-header";
import { StatCard } from "@/components/dashboard/stat-card";
import { EmptyState } from "@/components/dashboard/empty-state";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { ScoreTrend } from "@/components/charts/score-trend";
import { useAnalyses, useAnalysisStats } from "@/lib/hooks/use-analyses";
import { useResumes } from "@/lib/hooks/use-resumes";
import { cn, formatDate, scoreColor } from "@/lib/utils";

export default function DashboardOverview() {
  const stats = useAnalysisStats();
  const analyses = useAnalyses({ page_size: 6 });
  const resumes = useResumes({ page_size: 1 });

  const items = analyses.data?.items ?? [];
  const trend = [...items]
    .reverse()
    .filter((a) => a.ats_score != null)
    .map((a, i) => ({ label: `#${i + 1}`, score: Math.round(a.ats_score ?? 0) }));

  return (
    <div>
      <PageHeader
        title="Dashboard"
        description="Your resume intelligence at a glance."
        action={
          <Button asChild variant="gradient">
            <Link href="/dashboard/resumes">
              <ScanText className="size-4" /> New analysis
            </Link>
          </Button>
        }
      />

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {stats.isLoading ? (
          Array.from({ length: 4 }).map((_, i) => <Skeleton key={i} className="h-32 rounded-xl" />)
        ) : (
          <>
            <StatCard label="Total analyses" value={stats.data?.total_analyses ?? 0} icon={Activity} />
            <StatCard
              label="Average ATS"
              value={stats.data?.average_ats_score ?? 0}
              icon={Gauge}
              hint="Across all analyses"
            />
            <StatCard
              label="Best score"
              value={stats.data?.best_ats_score ?? 0}
              icon={Award}
              accent="text-emerald-400"
            />
            <StatCard
              label="Resumes"
              value={resumes.data?.meta.total ?? 0}
              icon={FileText}
              accent="text-sky-400"
            />
          </>
        )}
      </div>

      <div className="mt-6 grid gap-6 lg:grid-cols-[1.6fr_1fr]">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-base">
              <TrendingUp className="size-4 text-primary" /> ATS score trend
            </CardTitle>
            <CardDescription>Your ATS scores across recent analyses.</CardDescription>
          </CardHeader>
          <CardContent>
            {trend.length > 1 ? (
              <ScoreTrend data={trend} />
            ) : (
              <div className="flex h-[260px] items-center justify-center text-sm text-muted-foreground">
                Run a few analyses to see your trend.
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-base">Recent analyses</CardTitle>
            <CardDescription>Your latest resume runs.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-2">
            {analyses.isLoading ? (
              Array.from({ length: 4 }).map((_, i) => <Skeleton key={i} className="h-14 rounded-lg" />)
            ) : items.length === 0 ? (
              <EmptyState
                icon={FileText}
                title="No analyses yet"
                description="Upload a resume to get your first AI analysis."
                action={
                  <Button asChild variant="gradient" size="sm">
                    <Link href="/dashboard/resumes">Upload resume</Link>
                  </Button>
                }
              />
            ) : (
              items.map((a) => (
                <Link
                  key={a.id}
                  href={`/dashboard/history/${a.id}`}
                  className="flex items-center justify-between rounded-lg border border-border p-3 transition-colors hover:border-primary/40 hover:bg-accent/50"
                >
                  <div className="min-w-0">
                    <p className="truncate text-sm font-medium">{a.target_role ?? "General analysis"}</p>
                    <p className="text-xs text-muted-foreground">{formatDate(a.created_at, true)}</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <StatusBadge status={a.status} />
                    {a.ats_score != null && (
                      <span className={cn("text-sm font-semibold tabular-nums", scoreColor(a.ats_score))}>
                        {Math.round(a.ats_score)}
                      </span>
                    )}
                  </div>
                </Link>
              ))
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const map: Record<string, { variant: "default" | "success" | "warning" | "danger"; label: string }> = {
    completed: { variant: "success", label: "Completed" },
    running: { variant: "warning", label: "Running" },
    pending: { variant: "warning", label: "Pending" },
    failed: { variant: "danger", label: "Failed" },
  };
  const meta = map[status] ?? { variant: "default" as const, label: status };
  return <Badge variant={meta.variant}>{meta.label}</Badge>;
}
