"use client";

import { FileText, MoreVertical, ScanText, Star, Trash2 } from "lucide-react";

import { PageHeader } from "@/components/dashboard/page-header";
import { EmptyState } from "@/components/dashboard/empty-state";
import { ResumeUploader } from "@/components/dashboard/resume-uploader";
import { RunAnalysisDialog } from "@/components/dashboard/run-analysis-dialog";
import { StatusBadge } from "@/components/dashboard/status-badge";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  useDeleteResume,
  useResumes,
  useSetPrimaryResume,
} from "@/lib/hooks/use-resumes";
import { formatBytes, formatDate } from "@/lib/utils";

export default function ResumesPage() {
  const { data, isLoading } = useResumes({ page_size: 50 });
  const remove = useDeleteResume();
  const setPrimary = useSetPrimaryResume();
  const resumes = data?.items ?? [];

  return (
    <div>
      <PageHeader title="Resume Uploads" description="Upload, version and manage your resumes." />

      <ResumeUploader />

      <div className="mt-8 space-y-3">
        {isLoading ? (
          Array.from({ length: 3 }).map((_, i) => <Skeleton key={i} className="h-20 rounded-xl" />)
        ) : resumes.length === 0 ? (
          <EmptyState
            icon={FileText}
            title="No resumes yet"
            description="Upload your first resume above to get started with AI analysis."
          />
        ) : (
          resumes.map((resume) => (
            <Card key={resume.id}>
              <CardContent className="flex items-center gap-4 p-4">
                <div className="flex size-11 shrink-0 items-center justify-center rounded-xl bg-primary/10 text-primary">
                  <FileText className="size-5" />
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2">
                    <p className="truncate font-medium">{resume.file_name}</p>
                    {resume.is_primary && (
                      <Badge variant="default" className="gap-1">
                        <Star className="size-3" /> Primary
                      </Badge>
                    )}
                    <Badge variant="secondary">v{resume.version}</Badge>
                  </div>
                  <p className="mt-0.5 text-xs text-muted-foreground">
                    {formatBytes(resume.file_size)} · {formatDate(resume.created_at, true)}
                  </p>
                </div>
                <StatusBadge status={resume.status} />
                {resume.status === "parsed" && (
                  <RunAnalysisDialog
                    resumeId={resume.id}
                    trigger={
                      <Button size="sm" variant="gradient">
                        <ScanText className="size-4" /> Analyze
                      </Button>
                    }
                  />
                )}
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button size="icon" variant="ghost">
                      <MoreVertical className="size-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem onClick={() => setPrimary.mutate(resume.id)}>
                      <Star className="size-4" /> Set as primary
                    </DropdownMenuItem>
                    <DropdownMenuItem
                      className="text-rose-400 focus:text-rose-400"
                      onClick={() => remove.mutate(resume.id)}
                    >
                      <Trash2 className="size-4" /> Delete
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}
