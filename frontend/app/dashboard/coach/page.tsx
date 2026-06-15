"use client";

import { PageHeader } from "@/components/dashboard/page-header";
import { LatestAnalysisGate } from "@/components/dashboard/latest-analysis-gate";
import { CareerPanel } from "@/components/dashboard/results/career-panel";

export default function CoachPage() {
  return (
    <div>
      <PageHeader
        title="Career Coach"
        description="Salary insights, certifications and a personalized growth roadmap."
      />
      <LatestAnalysisGate
        emptyTitle="No career insights yet"
        emptyDescription="Run an analysis to unlock salary insights and a growth roadmap."
      >
        {(analysis) =>
          analysis.career_insight ? (
            <CareerPanel insight={analysis.career_insight} />
          ) : (
            <p className="text-muted-foreground">No career insight available for this analysis.</p>
          )
        }
      </LatestAnalysisGate>
    </div>
  );
}
