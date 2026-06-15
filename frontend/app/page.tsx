import { Navbar } from "@/components/marketing/navbar";
import { Hero } from "@/components/marketing/hero";
import { BentoFeatures } from "@/components/marketing/bento-features";
import { AgentShowcase } from "@/components/marketing/agent-showcase";
import { HowItWorks, StatsBand } from "@/components/marketing/how-it-works";
import { Testimonials } from "@/components/marketing/testimonials";
import { Faq } from "@/components/marketing/faq";
import { Cta } from "@/components/marketing/cta";
import { Footer } from "@/components/marketing/footer";

export default function LandingPage() {
  return (
    <div className="relative">
      <Navbar />
      <main>
        <Hero />
        <StatsBand />
        <BentoFeatures />
        <AgentShowcase />
        <HowItWorks />
        <Testimonials />
        <Faq />
        <Cta />
      </main>
      <Footer />
    </div>
  );
}
