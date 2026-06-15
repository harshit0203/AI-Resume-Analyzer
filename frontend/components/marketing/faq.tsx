"use client";

import { SectionHeading } from "./bento-features";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

const faqs = [
  {
    q: "How does the AI analysis work?",
    a: "When you upload a resume, six specialized agents run in sequence on a LangGraph workflow: parsing, ATS scoring, skill gap analysis, job matching, content improvement and career coaching. You can watch them work in real time.",
  },
  {
    q: "Which file formats are supported?",
    a: "PDF and DOCX resumes up to 10 MB. The text is extracted and structured into clean JSON, then analyzed by the agents.",
  },
  {
    q: "Is my data secure?",
    a: "Yes. Authentication uses JWT access and refresh tokens stored in secure, HTTP-only cookies. Your files are stored privately and scoped to your account, and every request is validated and rate limited.",
  },
  {
    q: "Do I need an OpenAI API key?",
    a: "No. The platform ships with a deterministic analysis engine so it works out of the box. Adding an OpenAI key unlocks richer, LLM-powered insights.",
  },
  {
    q: "Can I track multiple resume versions?",
    a: "Absolutely. Every upload is versioned, and your full analysis history is available in the dashboard so you can measure improvement over time.",
  },
];

export function Faq() {
  return (
    <section id="faq" className="mx-auto max-w-3xl px-4 py-24">
      <SectionHeading eyebrow="FAQ" title="Frequently asked questions" />
      <div className="mt-10">
        <Accordion type="single" collapsible>
          {faqs.map((faq, i) => (
            <AccordionItem key={faq.q} value={`item-${i}`}>
              <AccordionTrigger>{faq.q}</AccordionTrigger>
              <AccordionContent>{faq.a}</AccordionContent>
            </AccordionItem>
          ))}
        </Accordion>
      </div>
    </section>
  );
}
