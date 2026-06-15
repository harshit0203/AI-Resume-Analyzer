"use client";

import { motion } from "framer-motion";

import { SectionHeading } from "./bento-features";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { fadeInUp, staggerContainer } from "@/lib/motion";

const testimonials = [
  {
    quote:
      "The ATS score jumped from 61 to 89 after applying the agent's bullet rewrites. I had three interviews the next week.",
    name: "Priya S.",
    role: "Full Stack Engineer",
  },
  {
    quote:
      "Watching the agents work in real time felt like having a senior recruiter, a career coach and an ATS expert in one screen.",
    name: "Marcus T.",
    role: "AI Engineer",
  },
  {
    quote:
      "The skill gap roadmap told me exactly what to learn for a DevOps role. No fluff, just a clear 12 week plan.",
    name: "Daniel K.",
    role: "DevOps Engineer",
  },
  {
    quote:
      "Clean, fast, and genuinely useful. The job match percentages were spot on for my background.",
    name: "Aisha R.",
    role: "Python Developer",
  },
];

export function Testimonials() {
  return (
    <section className="mx-auto max-w-6xl px-4 py-24">
      <SectionHeading eyebrow="Loved by job seekers" title="Results people can feel" />
      <motion.div
        variants={staggerContainer}
        initial="hidden"
        whileInView="show"
        viewport={{ once: true, margin: "-60px" }}
        className="mt-14 grid gap-4 sm:grid-cols-2"
      >
        {testimonials.map((t) => (
          <motion.figure
            key={t.name}
            variants={fadeInUp}
            className="rounded-2xl border border-border bg-card p-6"
          >
            <blockquote className="text-balance leading-relaxed">&ldquo;{t.quote}&rdquo;</blockquote>
            <figcaption className="mt-5 flex items-center gap-3">
              <Avatar>
                <AvatarFallback>{t.name.split(" ").map((p) => p[0]).join("")}</AvatarFallback>
              </Avatar>
              <div>
                <div className="text-sm font-medium">{t.name}</div>
                <div className="text-xs text-muted-foreground">{t.role}</div>
              </div>
            </figcaption>
          </motion.figure>
        ))}
      </motion.div>
    </section>
  );
}
