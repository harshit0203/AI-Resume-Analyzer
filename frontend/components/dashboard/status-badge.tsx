import { Badge } from "@/components/ui/badge";
import type { AnalysisStatus, ResumeStatus } from "@/lib/types";

const MAP: Record<string, { variant: "default" | "success" | "warning" | "danger"; label: string }> = {
  completed: { variant: "success", label: "Completed" },
  parsed: { variant: "success", label: "Parsed" },
  running: { variant: "warning", label: "Running" },
  parsing: { variant: "warning", label: "Parsing" },
  pending: { variant: "warning", label: "Pending" },
  uploaded: { variant: "default", label: "Uploaded" },
  failed: { variant: "danger", label: "Failed" },
};

export function StatusBadge({ status }: { status: AnalysisStatus | ResumeStatus | string }) {
  const meta = MAP[status] ?? { variant: "default" as const, label: status };
  return <Badge variant={meta.variant}>{meta.label}</Badge>;
}
