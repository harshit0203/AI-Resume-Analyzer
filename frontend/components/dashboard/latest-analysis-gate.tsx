"use client";

import Link from "next/link";
import { Briefcase } from "lucide-react";

import { EmptyState } from "@/components/dashboard/empty-state";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useAnalyses, useAnalysis } from "@/lib/hooks/use-analyses";
import type { Analysis } from "@/lib/types";

/**
 * Resolves the most recent *completed* analysis and renders its detail through
 * the provided render-prop. Used by the Jobs & Career Coach pages.
 */
export function LatestAnalysisGate({
  emptyTitle,
  emptyDescription,
  children,
}: {
  emptyTitle: string;
  emptyDescription: string;
  children: (analysis: Analysis) => React.ReactNode;
}) {
  const list = useAnalyses({ page_size: 20 });
  const latest = list.data?.items.find((a) => a.status === "completed");
  const detail = useAnalysis(latest?.id ?? "");

  if (list.isLoading || (latest && detail.isLoading)) {
    return (
      <div className="grid gap-4 md:grid-cols-2">
        {Array.from({ length: 4 }).map((_, i) => (
          <Skeleton key={i} className="h-40 rounded-xl" />
        ))}
      </div>
    );
  }

  if (!latest || !detail.data) {
    return (
      <EmptyState
        icon={Briefcase}
        title={emptyTitle}
        description={emptyDescription}
        action={
          <Button asChild variant="gradient" size="sm">
            <Link href="/dashboard/resumes">Run an analysis</Link>
          </Button>
        }
      />
    );
  }

  return <>{children(detail.data)}</>;
}
