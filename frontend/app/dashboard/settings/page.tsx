"use client";

import { PageHeader } from "@/components/dashboard/page-header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Skeleton } from "@/components/ui/skeleton";
import { CAREER_PATHS } from "@/lib/types";
import { useSettings, useUpdateSettings } from "@/lib/hooks/use-user";
import { cn } from "@/lib/utils";

export default function SettingsPage() {
  const { data: settings, isLoading } = useSettings();
  const update = useUpdateSettings();

  if (isLoading || !settings) {
    return (
      <div>
        <PageHeader title="Settings" description="Manage your preferences." />
        <Skeleton className="h-64 rounded-xl" />
      </div>
    );
  }

  const toggles = [
    { key: "email_notifications", label: "Email notifications", desc: "Receive important account emails." },
    { key: "analysis_complete_alerts", label: "Analysis alerts", desc: "Get notified when an analysis finishes." },
    { key: "product_updates", label: "Product updates", desc: "Occasional product news and tips." },
  ] as const;

  return (
    <div>
      <PageHeader title="Settings" description="Manage your preferences and notifications." />

      <div className="grid gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Default target role</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="mb-3 text-sm text-muted-foreground">
              Pre-selected when you run a new analysis.
            </p>
            <div className="flex flex-wrap gap-2">
              {CAREER_PATHS.map((path) => (
                <button
                  key={path}
                  onClick={() =>
                    update.mutate({
                      default_target_role: settings.default_target_role === path ? undefined : path,
                    })
                  }
                  className={cn(
                    "rounded-lg border px-3 py-2 text-sm transition-colors",
                    settings.default_target_role === path
                      ? "border-primary bg-primary/10 text-primary"
                      : "border-border hover:border-primary/40"
                  )}
                >
                  {path}
                </button>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-base">Notifications</CardTitle>
          </CardHeader>
          <CardContent className="space-y-5">
            {toggles.map((toggle) => (
              <div key={toggle.key} className="flex items-center justify-between">
                <div>
                  <Label>{toggle.label}</Label>
                  <p className="text-sm text-muted-foreground">{toggle.desc}</p>
                </div>
                <Switch
                  checked={settings[toggle.key]}
                  onCheckedChange={(checked) => update.mutate({ [toggle.key]: checked })}
                />
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
