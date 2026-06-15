"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Briefcase,
  FileText,
  GraduationCap,
  History,
  LayoutDashboard,
  Settings,
  User,
} from "lucide-react";

import { Logo, LogoMark } from "@/components/logo";
import { cn } from "@/lib/utils";
import { useUiStore } from "@/lib/stores/ui-store";

const nav = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/dashboard/resumes", label: "Resume Uploads", icon: FileText },
  { href: "/dashboard/history", label: "Analysis History", icon: History },
  { href: "/dashboard/jobs", label: "Job Matching", icon: Briefcase },
  { href: "/dashboard/coach", label: "Career Coach", icon: GraduationCap },
];

const secondary = [
  { href: "/dashboard/profile", label: "Profile", icon: User },
  { href: "/dashboard/settings", label: "Settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();
  const collapsed = useUiStore((s) => s.sidebarCollapsed);

  const renderLink = (item: (typeof nav)[number]) => {
    const active = pathname === item.href || (item.href !== "/dashboard" && pathname.startsWith(item.href));
    return (
      <Link
        key={item.href}
        href={item.href}
        className={cn(
          "group flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
          active
            ? "bg-primary/15 text-primary"
            : "text-muted-foreground hover:bg-accent hover:text-foreground",
          collapsed && "justify-center px-2"
        )}
      >
        <item.icon className="size-[18px] shrink-0" />
        {!collapsed && <span>{item.label}</span>}
      </Link>
    );
  };

  return (
    <aside
      className={cn(
        "fixed inset-y-0 left-0 z-40 hidden flex-col border-r border-border bg-card/50 backdrop-blur-xl transition-all duration-300 md:flex",
        collapsed ? "w-16" : "w-64"
      )}
    >
      <div className="flex h-16 items-center gap-2 border-b border-border px-4">
        <Link href="/dashboard">
          {collapsed ? <LogoMark /> : <Logo />}
        </Link>
      </div>

      <nav className="flex flex-1 flex-col gap-1 overflow-y-auto p-3">
        {nav.map(renderLink)}
        <div className="my-3 h-px bg-border" />
        {secondary.map(renderLink)}
      </nav>

      {!collapsed && (
        <div className="m-3 rounded-xl border border-border bg-accent/40 p-4">
          <p className="text-xs font-medium">Need a hand?</p>
          <p className="mt-1 text-xs text-muted-foreground">
            Run a fresh analysis or explore the Career Coach for tailored guidance.
          </p>
          <Link
            href="/dashboard/coach"
            className="mt-3 inline-flex w-full items-center justify-center rounded-lg bg-[linear-gradient(120deg,var(--primary),oklch(0.66_0.2_320))] px-3 py-1.5 text-xs font-medium text-white"
          >
            Open Career Coach
          </Link>
        </div>
      )}
    </aside>
  );
}
