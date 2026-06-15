"use client";

import { motion } from "framer-motion";
import { FileUp, ScanText, Trophy } from "lucide-react";

import { SectionHeading } from "./bento-features";
import { fadeInUp, staggerContainer } from "@/lib/motion";

const steps = [
  {
    icon: FileUp,
    title: "Upload your resume",
    description: "Drop a PDF or DOCX. We parse it into clean, structured data in seconds.",
  },
  {
    icon: ScanText,
    title: "Agents analyze it live",
    description: "Six specialized agents score ATS, find gaps, match jobs and rewrite content.",
  },
  {
    icon: Trophy,
    title: "Act on the insights",
    description: "Apply recommendations, track versions and watch your scores climb.",
  },
];

export function HowItWorks() {
  return (
    <section className="mx-auto max-w-6xl px-4 py-24">
      <SectionHeading
        eyebrow="How it works"
        title="From upload to offer-ready in three steps"
        subtitle="No setup, no friction — just upload and let the agents do the heavy lifting."
      />

      <motion.div
        variants={staggerContainer}
        initial="hidden"
        whileInView="show"
        viewport={{ once: true, margin: "-60px" }}
        className="relative mt-14 grid gap-6 md:grid-cols-3"
      >
        <div className="absolute left-0 right-0 top-12 hidden h-px bg-gradient-to-r from-transparent via-border to-transparent md:block" />
        {steps.map((step, i) => (
          <motion.div key={step.title} variants={fadeInUp} className="relative text-center">
            <div className="mx-auto flex size-14 items-center justify-center rounded-2xl border border-border bg-card text-primary">
              <step.icon className="size-6" />
            </div>
            <div className="mx-auto mt-4 flex size-6 items-center justify-center rounded-full bg-primary/15 text-xs font-semibold text-primary">
              {i + 1}
            </div>
            <h3 className="mt-4 text-lg font-semibold">{step.title}</h3>
            <p className="mx-auto mt-2 max-w-xs text-sm text-muted-foreground">{step.description}</p>
          </motion.div>
        ))}
      </motion.div>
    </section>
  );
}

const stats = [
  { value: "6", label: "Specialized AI agents" },
  { value: "<10s", label: "Average analysis time" },
  { value: "6", label: "Career paths supported" },
  { value: "100%", label: "Free to get started" },
];

export function StatsBand() {
  return (
    <section className="mx-auto max-w-6xl px-4 pb-8">
      <motion.div
        variants={staggerContainer}
        initial="hidden"
        whileInView="show"
        viewport={{ once: true }}
        className="grid grid-cols-2 gap-4 rounded-2xl border border-border bg-card/50 p-8 md:grid-cols-4"
      >
        {stats.map((stat) => (
          <motion.div key={stat.label} variants={fadeInUp} className="text-center">
            <div className="text-3xl font-semibold text-gradient sm:text-4xl">{stat.value}</div>
            <div className="mt-1 text-xs text-muted-foreground sm:text-sm">{stat.label}</div>
          </motion.div>
        ))}
      </motion.div>
    </section>
  );
}
