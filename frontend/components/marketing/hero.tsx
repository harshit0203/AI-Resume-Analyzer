"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowRight, Workflow, Zap } from "lucide-react";

import { Button } from "@/components/ui/button";
import { fadeInUp, staggerContainer } from "@/lib/motion";

export function Hero() {
  return (
    <section className="relative overflow-hidden pt-36 pb-24">
      <div className="mesh-bg animate-aurora absolute inset-0 -z-10" />
      <div className="grid-pattern absolute inset-0 -z-10 opacity-40" />

      <motion.div
        variants={staggerContainer}
        initial="hidden"
        animate="show"
        className="mx-auto max-w-4xl px-4 text-center"
      >
        <motion.div variants={fadeInUp} className="flex justify-center">
          <span className="glass inline-flex items-center gap-2 rounded-full px-4 py-1.5 text-xs font-medium text-muted-foreground">
            <Workflow className="size-3.5 text-primary" />
            Powered by a 6-agent AI workflow
          </span>
        </motion.div>

        <motion.h1
          variants={fadeInUp}
          className="mt-6 text-balance text-5xl font-semibold tracking-tight sm:text-6xl md:text-7xl"
        >
          Your resume, <span className="text-gradient">analyzed by AI</span> in seconds
        </motion.h1>

        <motion.p
          variants={fadeInUp}
          className="mx-auto mt-6 max-w-2xl text-balance text-lg text-muted-foreground"
        >
          Upload your resume and watch six specialized AI agents score ATS compatibility,
          uncover skill gaps, match jobs, rewrite weak bullets, and map your career path —
          all in real time.
        </motion.p>

        <motion.div variants={fadeInUp} className="mt-9 flex flex-col items-center justify-center gap-3 sm:flex-row">
          <Button asChild size="lg" variant="gradient" className="group">
            <Link href="/register">
              Analyze my resume free
              <ArrowRight className="transition-transform group-hover:translate-x-0.5" />
            </Link>
          </Button>
          <Button asChild size="lg" variant="outline">
            <Link href="#agents">
              <Zap className="text-primary" />
              See the agents
            </Link>
          </Button>
        </motion.div>

        <motion.p variants={fadeInUp} className="mt-4 text-xs text-muted-foreground">
          No credit card required · PDF & DOCX supported · Free forever tier
        </motion.p>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4, duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
        className="mx-auto mt-16 max-w-5xl px-4"
      >
        <div className="glass overflow-hidden rounded-2xl p-2 shadow-2xl">
          <div className="rounded-xl border border-border bg-card/60 p-6">
            <HeroPreview />
          </div>
        </div>
      </motion.div>
    </section>
  );
}

function HeroPreview() {
  const agents = [
    { name: "Resume Parser", value: 100 },
    { name: "ATS Analyzer", value: 86 },
    { name: "Skill Gap", value: 72 },
    { name: "Job Match", value: 91 },
    { name: "Improvement", value: 100 },
    { name: "Career Coach", value: 100 },
  ];
  return (
    <div className="grid gap-4 sm:grid-cols-3">
      <div className="sm:col-span-1 flex flex-col items-center justify-center rounded-xl bg-secondary/40 p-6">
        <div className="text-xs text-muted-foreground">Overall ATS Score</div>
        <div className="mt-2 text-6xl font-semibold text-gradient">86</div>
        <div className="mt-1 text-xs text-emerald-400">Strong match</div>
      </div>
      <div className="sm:col-span-2 space-y-2.5">
        {agents.map((a, i) => (
          <div key={a.name} className="flex items-center gap-3">
            <span className="w-28 shrink-0 text-xs text-muted-foreground">{a.name}</span>
            <div className="h-2 flex-1 overflow-hidden rounded-full bg-secondary">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${a.value}%` }}
                transition={{ delay: 0.6 + i * 0.12, duration: 0.8 }}
                className="h-full rounded-full bg-[linear-gradient(90deg,var(--primary),oklch(0.66_0.2_320))]"
              />
            </div>
            <span className="w-9 text-right text-xs tabular-nums text-muted-foreground">{a.value}%</span>
          </div>
        ))}
      </div>
    </div>
  );
}
