import { type LucideIcon } from "lucide-react";

import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";

export function StatCard({
  label,
  value,
  icon: Icon,
  hint,
  accent = "text-primary",
}: {
  label: string;
  value: string | number;
  icon: LucideIcon;
  hint?: string;
  accent?: string;
}) {
  return (
    <Card className="relative overflow-hidden">
      <div className="absolute -right-6 -top-6 size-24 rounded-full bg-primary/5 blur-2xl" />
      <CardContent className="p-5">
        <div className="flex items-center justify-between">
          <span className="text-sm text-muted-foreground">{label}</span>
          <Icon className={cn("size-4", accent)} />
        </div>
        <div className="mt-3 text-3xl font-semibold tabular-nums">{value}</div>
        {hint && <p className="mt-1 text-xs text-muted-foreground">{hint}</p>}
      </CardContent>
    </Card>
  );
}
