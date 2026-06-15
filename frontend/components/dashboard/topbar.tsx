"use client";

import Link from "next/link";
import { LogOut, PanelLeft, ScanText, Settings, User } from "lucide-react";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { ThemeToggle } from "@/components/theme-toggle";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { useAuthStore } from "@/lib/stores/auth-store";
import { useUiStore } from "@/lib/stores/ui-store";
import { useLogout } from "@/lib/hooks/use-auth";
import { initials } from "@/lib/utils";

export function Topbar() {
  const user = useAuthStore((s) => s.user);
  const toggleSidebar = useUiStore((s) => s.toggleSidebar);
  const logout = useLogout();

  return (
    <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-border bg-background/70 px-4 backdrop-blur-xl sm:px-6">
      <div className="flex items-center gap-3">
        <Button variant="ghost" size="icon" onClick={toggleSidebar} className="hidden md:inline-flex">
          <PanelLeft className="size-4" />
        </Button>
        <div>
          <p className="text-sm font-medium">
            Welcome back{user?.full_name ? `, ${user.full_name.split(" ")[0]}` : ""} 👋
          </p>
          <p className="text-xs text-muted-foreground">Let&apos;s optimize your career today.</p>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <ThemeToggle />
        <Button asChild variant="gradient" size="sm" className="hidden sm:inline-flex">
          <Link href="/dashboard/resumes">
            <ScanText className="size-4" />
            New analysis
          </Link>
        </Button>

        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <button className="rounded-full outline-none ring-ring focus-visible:ring-2">
              <Avatar>
                {user?.avatar_url && <AvatarImage src={user.avatar_url} alt={user.full_name ?? "User"} />}
                <AvatarFallback>{initials(user?.full_name)}</AvatarFallback>
              </Avatar>
            </button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-56">
            <DropdownMenuLabel>
              <div className="font-medium text-foreground">{user?.full_name ?? "Account"}</div>
              <div className="truncate text-xs">{user?.email}</div>
            </DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem asChild>
              <Link href="/dashboard/profile">
                <User className="size-4" /> Profile
              </Link>
            </DropdownMenuItem>
            <DropdownMenuItem asChild>
              <Link href="/dashboard/settings">
                <Settings className="size-4" /> Settings
              </Link>
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem
              onClick={() => logout.mutate()}
              className="text-rose-400 focus:text-rose-400"
            >
              <LogOut className="size-4" /> Sign out
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </header>
  );
}
