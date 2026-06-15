"use client";

import { PageHeader } from "@/components/dashboard/page-header";
import { LatestAnalysisGate } from "@/components/dashboard/latest-analysis-gate";
import { JobMatchPanel } from "@/components/dashboard/results/job-match-panel";

export default function JobsPage() {
  return (
    <div>
      <PageHeader
        title="Job Matching"
        description="Roles ranked by match percentage from your most recent analysis."
      />
      <LatestAnalysisGate
        emptyTitle="No job matches yet"
        emptyDescription="Run an analysis on a resume to discover your best-fit roles."
      >
        {(analysis) => <JobMatchPanel matches={analysis.job_matches} />}
      </LatestAnalysisGate>
    </div>
  );
}
