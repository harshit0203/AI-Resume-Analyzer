"use client";

import { Check, Loader2, X } from "lucide-react";

import { cn } from "@/lib/utils";
import { AGENT_META, type AgentExecution, type AgentType } from "@/lib/types";

type LiveStatus = "pending" | "running" | "completed" | "failed";

const ORDER: AgentType[] = [
  "resume_parser",
  "ats_analyzer",
  "skill_gap",
  "job_match",
  "resume_improvement",
  "career_coach",
];

export function AgentTimeline({
  executions,
  liveStatus,
  connected,
}: {
  executions: AgentExecution[];
  liveStatus: Record<string, LiveStatus>;
  connected: boolean;
}) {
  const byType = new Map(executions.map((e) => [e.agent_type, e]));

  return (
    <div className="space-y-1">
      <div className="mb-3 flex items-center gap-2 text-xs text-muted-foreground">
        <span className={cn("size-2 rounded-full", connected ? "bg-emerald-400" : "bg-muted-foreground")} />
        {connected ? "Live · streaming agent updates" : "Live updates unavailable — polling"}
      </div>
      {ORDER.map((type, index) => {
        const execution = byType.get(type);
        const status: LiveStatus = (liveStatus[type] ?? execution?.status ?? "pending") as LiveStatus;
        const meta = AGENT_META[type];
        const last = index === ORDER.length - 1;
        return (
          <div key={type} className="relative flex gap-4 pb-4">
            {!last && (
              <span
                className={cn(
                  "absolute left-[15px] top-8 h-full w-px",
                  status === "completed" ? "bg-emerald-500/40" : "bg-border"
                )}
              />
            )}
            <div
              className={cn(
                "z-10 flex size-8 shrink-0 items-center justify-center rounded-full transition-colors",
                status === "completed"
                  ? "bg-emerald-500/20 text-emerald-400"
                  : status === "running"
                    ? "bg-primary/20 text-primary"
                    : status === "failed"
                      ? "bg-rose-500/20 text-rose-400"
                      : "bg-secondary text-muted-foreground"
              )}
            >
              {status === "completed" ? (
                <Check className="size-4" />
              ) : status === "running" ? (
                <Loader2 className="size-4 animate-spin" />
              ) : status === "failed" ? (
                <X className="size-4" />
              ) : (
                index + 1
              )}
            </div>
            <div className="flex-1 pt-1">
              <div className="flex items-center justify-between">
                <p className="text-sm font-medium">{meta.label}</p>
                <span
                  className={cn(
                    "text-xs capitalize",
                    status === "completed"
                      ? "text-emerald-400"
                      : status === "running"
                        ? "text-primary"
                        : status === "failed"
                          ? "text-rose-400"
                          : "text-muted-foreground"
                  )}
                >
                  {status}
                </span>
              </div>
              <p className="text-xs text-muted-foreground">{meta.description}</p>
              {execution?.duration_ms != null && status === "completed" && (
                <p className="mt-0.5 text-[11px] text-muted-foreground">
                  {(execution.duration_ms / 1000).toFixed(1)}s
                </p>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}
