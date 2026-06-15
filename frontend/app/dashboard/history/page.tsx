"use client";

import Link from "next/link";
import { History, Trash2 } from "lucide-react";

import { PageHeader } from "@/components/dashboard/page-header";
import { EmptyState } from "@/components/dashboard/empty-state";
import { StatusBadge } from "@/components/dashboard/status-badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { useAnalyses, useDeleteAnalysis } from "@/lib/hooks/use-analyses";
import { cn, formatDate, scoreColor } from "@/lib/utils";

export default function HistoryPage() {
  const { data, isLoading } = useAnalyses({ page_size: 50 });
  const remove = useDeleteAnalysis();
  const items = data?.items ?? [];

  return (
    <div>
      <PageHeader title="Analysis History" description="Every analysis you've run, with scores and status." />

      <div className="space-y-3">
        {isLoading ? (
          Array.from({ length: 4 }).map((_, i) => <Skeleton key={i} className="h-20 rounded-xl" />)
        ) : items.length === 0 ? (
          <EmptyState
            icon={History}
            title="No analyses yet"
            description="Run an analysis from your resumes to see it here."
            action={
              <Button asChild variant="gradient" size="sm">
                <Link href="/dashboard/resumes">Go to resumes</Link>
              </Button>
            }
          />
        ) : (
          items.map((a) => (
            <Card key={a.id}>
              <CardContent className="flex items-center gap-4 p-4">
                <Link href={`/dashboard/history/${a.id}`} className="min-w-0 flex-1">
                  <p className="truncate font-medium">{a.target_role ?? "General analysis"}</p>
                  <p className="mt-0.5 text-xs text-muted-foreground">{formatDate(a.created_at, true)}</p>
                </Link>
                {a.overall_score != null && (
                  <div className="text-right">
                    <p className={cn("text-lg font-semibold tabular-nums", scoreColor(a.overall_score))}>
                      {Math.round(a.overall_score)}
                    </p>
                    <p className="text-[10px] uppercase tracking-wide text-muted-foreground">Overall</p>
                  </div>
                )}
                {a.ats_score != null && (
                  <div className="text-right">
                    <p className={cn("text-lg font-semibold tabular-nums", scoreColor(a.ats_score))}>
                      {Math.round(a.ats_score)}
                    </p>
                    <p className="text-[10px] uppercase tracking-wide text-muted-foreground">ATS</p>
                  </div>
                )}
                <StatusBadge status={a.status} />
                <Button size="icon" variant="ghost" onClick={() => remove.mutate(a.id)}>
                  <Trash2 className="size-4" />
                </Button>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}
