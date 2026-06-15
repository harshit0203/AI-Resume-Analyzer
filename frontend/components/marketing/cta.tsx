"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";

import { Button } from "@/components/ui/button";
import { fadeInUp } from "@/lib/motion";

export function Cta() {
  return (
    <section className="mx-auto max-w-6xl px-4 py-24">
      <motion.div
        variants={fadeInUp}
        initial="hidden"
        whileInView="show"
        viewport={{ once: true }}
        className="relative overflow-hidden rounded-3xl border border-primary/30 p-12 text-center"
      >
        <div className="mesh-bg animate-aurora absolute inset-0 -z-10" />
        <h2 className="text-balance text-3xl font-semibold tracking-tight sm:text-4xl">
          Ready to land your next role?
        </h2>
        <p className="mx-auto mt-4 max-w-xl text-balance text-muted-foreground">
          Join thousands of job seekers using AI to optimize their resumes and accelerate their careers.
        </p>
        <Button asChild size="lg" variant="gradient" className="group mt-8">
          <Link href="/register">
            Get started free
            <ArrowRight className="transition-transform group-hover:translate-x-0.5" />
          </Link>
        </Button>
      </motion.div>
    </section>
  );
}
