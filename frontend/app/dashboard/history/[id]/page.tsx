"use client";

import { use } from "react";
import Link from "next/link";
import { ArrowLeft, Briefcase, Compass, GraduationCap, Target, Wand2, Workflow } from "lucide-react";

import { PageHeader } from "@/components/dashboard/page-header";
import { AgentTimeline } from "@/components/dashboard/agent-timeline";
import { StatusBadge } from "@/components/dashboard/status-badge";
import { AtsPanel } from "@/components/dashboard/results/ats-panel";
import { SkillGapPanel } from "@/components/dashboard/results/skill-gap-panel";
import { JobMatchPanel } from "@/components/dashboard/results/job-match-panel";
import { ImprovementPanel } from "@/components/dashboard/results/improvement-panel";
import { CareerPanel } from "@/components/dashboard/results/career-panel";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useAnalysis } from "@/lib/hooks/use-analyses";
import { useAnalysisSocket } from "@/lib/hooks/use-analysis-socket";
import { cn, formatDate, scoreColor } from "@/lib/utils";

export default function AnalysisDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const { data: analysis, isLoading } = useAnalysis(id, { poll: true });
  const { connected, agentStatus } = useAnalysisSocket(id);

  const running = analysis?.status === "running" || analysis?.status === "pending";

  return (
    <div>
      <Button asChild variant="ghost" size="sm" className="mb-4 -ml-2">
        <Link href="/dashboard/history">
          <ArrowLeft className="size-4" /> Back to history
        </Link>
      </Button>

      <PageHeader
        title={analysis?.target_role ?? "Resume analysis"}
        description={analysis ? formatDate(analysis.created_at, true) : "Loading analysis…"}
        action={analysis && <StatusBadge status={analysis.status} />}
      />

      {isLoading ? (
        <div className="grid gap-6 lg:grid-cols-[320px_1fr]">
          <Skeleton className="h-96 rounded-xl" />
          <Skeleton className="h-96 rounded-xl" />
        </div>
      ) : !analysis ? (
        <p className="text-muted-foreground">Analysis not found.</p>
      ) : (
        <div className="grid gap-6 lg:grid-cols-[320px_1fr]">
          {/* Sidebar: scores + agent timeline */}
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <ScoreTile label="ATS" value={analysis.ats_score} />
              <ScoreTile label="Overall" value={analysis.overall_score} />
            </div>
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="flex items-center gap-2 text-sm">
                  <Workflow className="size-4 text-primary" /> Agent execution
                </CardTitle>
              </CardHeader>
              <CardContent>
                <AgentTimeline
                  executions={analysis.agent_executions}
                  liveStatus={agentStatus}
                  connected={connected}
                />
              </CardContent>
            </Card>
          </div>

          {/* Main: results */}
          <div>
            {running ? (
              <Card>
                <CardContent className="flex flex-col items-center justify-center py-20 text-center">
                  <div className="size-10 animate-spin rounded-full border-2 border-primary border-t-transparent" />
                  <p className="mt-4 font-medium">Agents are analyzing your resume…</p>
                  <p className="mt-1 text-sm text-muted-foreground">
                    Watch the timeline on the left update in real time.
                  </p>
                </CardContent>
              </Card>
            ) : analysis.status === "failed" ? (
              <Card>
                <CardContent className="py-16 text-center">
                  <p className="font-medium text-rose-400">Analysis failed</p>
                  <p className="mt-1 text-sm text-muted-foreground">{analysis.error}</p>
                </CardContent>
              </Card>
            ) : (
              <Tabs defaultValue="ats">
                <TabsList className="flex w-full flex-wrap justify-start">
                  <TabsTrigger value="ats"><Target className="size-4" /> ATS</TabsTrigger>
                  <TabsTrigger value="skills"><GraduationCap className="size-4" /> Skill Gap</TabsTrigger>
                  <TabsTrigger value="jobs"><Briefcase className="size-4" /> Jobs</TabsTrigger>
                  <TabsTrigger value="improve"><Wand2 className="size-4" /> Improve</TabsTrigger>
                  <TabsTrigger value="career"><Compass className="size-4" /> Career</TabsTrigger>
                </TabsList>

                <TabsContent value="ats">
                  {analysis.ats_result && <AtsPanel result={analysis.ats_result} />}
                </TabsContent>
                <TabsContent value="skills">
                  {analysis.skill_gap_result && <SkillGapPanel result={analysis.skill_gap_result} />}
                </TabsContent>
                <TabsContent value="jobs">
                  <JobMatchPanel matches={analysis.job_matches} />
                </TabsContent>
                <TabsContent value="improve">
                  {analysis.improvement_result && <ImprovementPanel result={analysis.improvement_result} />}
                </TabsContent>
                <TabsContent value="career">
                  {analysis.career_insight && <CareerPanel insight={analysis.career_insight} />}
                </TabsContent>
              </Tabs>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

function ScoreTile({ label, value }: { label: string; value?: number | null }) {
  return (
    <Card>
      <CardContent className="p-4 text-center">
        <p className={cn("text-3xl font-semibold tabular-nums", value != null ? scoreColor(value) : "text-muted-foreground")}>
          {value != null ? Math.round(value) : "—"}
        </p>
        <p className="text-xs uppercase tracking-wide text-muted-foreground">{label}</p>
      </CardContent>
    </Card>
  );
}
