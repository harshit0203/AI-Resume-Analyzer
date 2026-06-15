"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Menu, X } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Logo } from "@/components/logo";
import { ThemeToggle } from "@/components/theme-toggle";
import { cn } from "@/lib/utils";
import { useAuthStore } from "@/lib/stores/auth-store";

const links = [
  { href: "#features", label: "Features" },
  { href: "#agents", label: "AI Agents" },
  { href: "#faq", label: "FAQ" },
];

export function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);
  const user = useAuthStore((s) => s.user);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 16);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header
      className={cn(
        "fixed inset-x-0 top-0 z-50 transition-all duration-300",
        scrolled ? "py-2" : "py-4"
      )}
    >
      <div className="mx-auto max-w-6xl px-4">
        <nav
          className={cn(
            "flex items-center justify-between rounded-2xl px-4 py-2.5 transition-all",
            scrolled ? "glass shadow-lg" : ""
          )}
        >
          <Link href="/">
            <Logo />
          </Link>

          <div className="hidden items-center gap-1 md:flex">
            {links.map((link) => (
              <a
                key={link.href}
                href={link.href}
                className="rounded-lg px-3 py-2 text-sm text-muted-foreground transition-colors hover:text-foreground"
              >
                {link.label}
              </a>
            ))}
          </div>

          <div className="hidden items-center gap-2 md:flex">
            <ThemeToggle />
            {user ? (
              <Button asChild size="sm" variant="gradient">
                <Link href="/dashboard">Open dashboard</Link>
              </Button>
            ) : (
              <>
                <Button asChild size="sm" variant="ghost">
                  <Link href="/login">Sign in</Link>
                </Button>
                <Button asChild size="sm" variant="gradient">
                  <Link href="/register">Get started</Link>
                </Button>
              </>
            )}
          </div>

          <button
            className="md:hidden"
            onClick={() => setOpen((v) => !v)}
            aria-label="Toggle menu"
          >
            {open ? <X className="size-5" /> : <Menu className="size-5" />}
          </button>
        </nav>

        {open && (
          <div className="glass mt-2 flex flex-col gap-1 rounded-2xl p-3 md:hidden">
            {links.map((link) => (
              <a
                key={link.href}
                href={link.href}
                onClick={() => setOpen(false)}
                className="rounded-lg px-3 py-2 text-sm text-muted-foreground hover:bg-accent hover:text-foreground"
              >
                {link.label}
              </a>
            ))}
            <div className="mt-2 flex flex-col gap-2">
              <Button asChild variant="outline" size="sm">
                <Link href="/login">Sign in</Link>
              </Button>
              <Button asChild variant="gradient" size="sm">
                <Link href="/register">Get started</Link>
              </Button>
            </div>
          </div>
        )}
      </div>
    </header>
  );
}
