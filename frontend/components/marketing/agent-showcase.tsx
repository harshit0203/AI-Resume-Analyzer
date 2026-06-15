"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Check, Loader2 } from "lucide-react";

import { SectionHeading } from "./bento-features";
import { cn } from "@/lib/utils";

const AGENTS = [
  { name: "Resume Parser", task: "Extracting contact, skills, education & experience" },
  { name: "ATS Analyzer", task: "Scoring ATS compatibility & missing keywords" },
  { name: "Skill Gap", task: "Comparing skills against your target career path" },
  { name: "Job Match", task: "Ranking best-fit roles with match percentages" },
  { name: "Resume Improvement", task: "Rewriting bullets & crafting a stronger summary" },
  { name: "Career Coach", task: "Building salary insights & a growth roadmap" },
];

export function AgentShowcase() {
  const [active, setActive] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setActive((prev) => (prev + 1) % (AGENTS.length + 1));
    }, 1400);
    return () => clearInterval(interval);
  }, []);

  return (
    <section id="agents" className="relative overflow-hidden py-24">
      <div className="mesh-bg absolute inset-0 -z-10 opacity-50" />
      <div className="mx-auto max-w-6xl px-4">
        <SectionHeading
          eyebrow="Multi-agent workflow"
          title="Six specialized agents, one orchestrated pipeline"
          subtitle="Built on LangGraph + LangChain. Each agent is an expert at one job, passing structured context to the next — just like a senior career team."
        />

        <div className="mt-14 grid gap-3">
          {AGENTS.map((agent, index) => {
            const done = index < active;
            const running = index === active;
            return (
              <motion.div
                key={agent.name}
                initial={{ opacity: 0, x: -16 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.06 }}
                className={cn(
                  "flex items-center gap-4 rounded-xl border p-4 transition-all duration-300",
                  running
                    ? "border-primary/50 bg-primary/5 glow"
                    : done
                      ? "border-emerald-500/30 bg-emerald-500/5"
                      : "border-border bg-card"
                )}
              >
                <div
                  className={cn(
                    "flex size-9 shrink-0 items-center justify-center rounded-full text-sm font-medium",
                    done
                      ? "bg-emerald-500/20 text-emerald-400"
                      : running
                        ? "bg-primary/20 text-primary"
                        : "bg-secondary text-muted-foreground"
                  )}
                >
                  {done ? <Check className="size-4" /> : running ? <Loader2 className="size-4 animate-spin" /> : index + 1}
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex items-center justify-between">
                    <span className="font-medium">{agent.name}</span>
                    <span
                      className={cn(
                        "text-xs",
                        done ? "text-emerald-400" : running ? "text-primary" : "text-muted-foreground"
                      )}
                    >
                      {done ? "Completed" : running ? "Processing…" : "Queued"}
                    </span>
                  </div>
                  <p className="truncate text-sm text-muted-foreground">{agent.task}</p>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
