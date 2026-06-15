"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Loader2, ScanText } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { cn } from "@/lib/utils";
import { CAREER_PATHS } from "@/lib/types";
import { useCreateAnalysis } from "@/lib/hooks/use-analyses";

export function RunAnalysisDialog({
  resumeId,
  trigger,
}: {
  resumeId: string;
  trigger: React.ReactNode;
}) {
  const [open, setOpen] = useState(false);
  const [role, setRole] = useState<string>("");
  const create = useCreateAnalysis();
  const router = useRouter();

  const onRun = async () => {
    const analysis = await create.mutateAsync({
      resume_id: resumeId,
      target_role: role || undefined,
    });
    setOpen(false);
    router.push(`/dashboard/history/${analysis.id}`);
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>{trigger}</DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <ScanText className="size-5 text-primary" /> Run AI analysis
          </DialogTitle>
          <DialogDescription>
            Choose a target career path to tailor the skill gap, job match and coaching agents.
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-3">
          <Label>Target career path (optional)</Label>
          <div className="grid grid-cols-2 gap-2">
            {CAREER_PATHS.map((path) => (
              <button
                key={path}
                onClick={() => setRole((prev) => (prev === path ? "" : path))}
                className={cn(
                  "rounded-lg border px-3 py-2 text-sm transition-colors",
                  role === path
                    ? "border-primary bg-primary/10 text-primary"
                    : "border-border hover:border-primary/40"
                )}
              >
                {path}
              </button>
            ))}
          </div>
        </div>

        <Button onClick={onRun} variant="gradient" disabled={create.isPending} className="w-full">
          {create.isPending && <Loader2 className="animate-spin" />}
          Start analysis
        </Button>
      </DialogContent>
    </Dialog>
  );
}
