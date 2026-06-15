"use client";

import { useEffect } from "react";
import { usePathname, useRouter } from "next/navigation";

import { Sidebar } from "@/components/dashboard/sidebar";
import { Topbar } from "@/components/dashboard/topbar";
import { useAuthStore } from "@/lib/stores/auth-store";
import { useUiStore } from "@/lib/stores/ui-store";
import { cn } from "@/lib/utils";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const { user, isLoading } = useAuthStore();
  const collapsed = useUiStore((s) => s.sidebarCollapsed);
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (!isLoading && !user) {
      router.replace(`/login?next=${encodeURIComponent(pathname)}`);
    }
  }, [isLoading, user, router, pathname]);

  if (isLoading || !user) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="size-8 animate-spin rounded-full border-2 border-primary border-t-transparent" />
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      <Sidebar />
      <div className={cn("transition-all duration-300", collapsed ? "md:pl-16" : "md:pl-64")}>
        <Topbar />
        <main className="mx-auto max-w-7xl p-4 sm:p-6">{children}</main>
      </div>
    </div>
  );
}
