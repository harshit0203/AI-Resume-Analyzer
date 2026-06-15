import Link from "next/link";
import { Logo } from "@/components/logo";

const groups = [
  {
    title: "Product",
    links: [
      { label: "Features", href: "#features" },
      { label: "AI Agents", href: "#agents" },
      { label: "How it works", href: "#faq" },
    ],
  },
  {
    title: "Company",
    links: [
      { label: "About", href: "#" },
      { label: "Blog", href: "#" },
      { label: "Careers", href: "#" },
    ],
  },
  {
    title: "Legal",
    links: [
      { label: "Privacy", href: "#" },
      { label: "Terms", href: "#" },
      { label: "Security", href: "#" },
    ],
  },
];

export function Footer() {
  return (
    <footer className="border-t border-border">
      <div className="mx-auto max-w-6xl px-4 py-14">
        <div className="grid gap-10 md:grid-cols-[1.5fr_repeat(3,1fr)]">
          <div>
            <Link href="/">
              <Logo />
            </Link>
            <p className="mt-4 max-w-xs text-sm text-muted-foreground">
              Multi-agent AI resume analysis and career coaching for the modern job seeker.
            </p>
          </div>
          {groups.map((group) => (
            <div key={group.title}>
              <h4 className="text-sm font-medium">{group.title}</h4>
              <ul className="mt-4 space-y-2.5">
                {group.links.map((link) => (
                  <li key={link.label}>
                    <a href={link.href} className="text-sm text-muted-foreground transition-colors hover:text-foreground">
                      {link.label}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        <div className="mt-12 flex flex-col items-center justify-between gap-4 border-t border-border pt-6 text-sm text-muted-foreground sm:flex-row">
          <p>© {new Date().getFullYear()} AIResumeAnalyzer. All rights reserved.</p>
          <p>Built with Next.js, FastAPI & LangGraph.</p>
        </div>
      </div>
    </footer>
  );
}
