"use client";

import { motion } from "framer-motion";
import {
  BarChart3,
  FileSearch,
  Gauge,
  Radar,
  Target,
  Workflow,
} from "lucide-react";

import { cn } from "@/lib/utils";
import { fadeInUp, staggerContainer } from "@/lib/motion";

const features = [
  {
    icon: Gauge,
    title: "ATS Score Engine",
    description:
      "Get an instant 0–100 ATS compatibility score with strengths, weaknesses and the exact keywords you're missing.",
    className: "md:col-span-2",
  },
  {
    icon: Radar,
    title: "Skill Radar",
    description: "Visualize how your skills map to your target career path.",
    className: "",
  },
  {
    icon: Target,
    title: "Job Matching",
    description: "Top roles ranked by match %, with reasons and gaps.",
    className: "",
  },
  {
    icon: Workflow,
    title: "Live Agent Timeline",
    description:
      "Watch each AI agent process your resume step-by-step over a real-time WebSocket stream.",
    className: "md:col-span-2",
  },
  {
    icon: FileSearch,
    title: "Deep Parsing",
    description: "PDF & DOCX parsed into clean structured JSON.",
    className: "",
  },
  {
    icon: BarChart3,
    title: "Career Insights",
    description: "Salary bands, certifications and a 12-month growth roadmap.",
    className: "",
  },
];

export function BentoFeatures() {
  return (
    <section id="features" className="relative mx-auto max-w-6xl px-4 py-24">
      <SectionHeading
        eyebrow="Everything you need"
        title="A complete resume intelligence suite"
        subtitle="From ATS scoring to career coaching, every insight you need to land your next role — in one beautiful dashboard."
      />

      <motion.div
        variants={staggerContainer}
        initial="hidden"
        whileInView="show"
        viewport={{ once: true, margin: "-80px" }}
        className="mt-14 grid gap-4 md:grid-cols-3"
      >
        {features.map((feature) => (
          <motion.div
            key={feature.title}
            variants={fadeInUp}
            className={cn(
              "group relative overflow-hidden rounded-2xl border border-border bg-card p-6 transition-colors hover:border-primary/40",
              feature.className
            )}
          >
            <div className="absolute -right-10 -top-10 size-32 rounded-full bg-primary/10 blur-2xl transition-opacity group-hover:opacity-100 opacity-0" />
            <div className="flex size-11 items-center justify-center rounded-xl bg-primary/15 text-primary">
              <feature.icon className="size-5" />
            </div>
            <h3 className="mt-4 text-lg font-semibold">{feature.title}</h3>
            <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{feature.description}</p>
          </motion.div>
        ))}
      </motion.div>
    </section>
  );
}

export function SectionHeading({
  eyebrow,
  title,
  subtitle,
}: {
  eyebrow: string;
  title: string;
  subtitle?: string;
}) {
  return (
    <motion.div
      variants={staggerContainer}
      initial="hidden"
      whileInView="show"
      viewport={{ once: true }}
      className="mx-auto max-w-2xl text-center"
    >
      <motion.span
        variants={fadeInUp}
        className="inline-flex items-center gap-1.5 rounded-full bg-primary/10 px-3 py-1 text-xs font-medium text-primary"
      >
        <span className="size-1.5 rounded-full bg-primary" />
        {eyebrow}
      </motion.span>
      <motion.h2 variants={fadeInUp} className="mt-4 text-3xl font-semibold tracking-tight sm:text-4xl">
        {title}
      </motion.h2>
      {subtitle && (
        <motion.p variants={fadeInUp} className="mt-4 text-balance text-muted-foreground">
          {subtitle}
        </motion.p>
      )}
    </motion.div>
  );
}
