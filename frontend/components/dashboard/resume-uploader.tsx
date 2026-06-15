"use client";

import { useCallback, useRef, useState } from "react";
import { FileUp, Loader2 } from "lucide-react";

import { cn, formatBytes } from "@/lib/utils";
import { useUploadResume } from "@/lib/hooks/use-resumes";

const ACCEPTED = [".pdf", ".docx"];
const MAX_MB = 10;

export function ResumeUploader() {
  const upload = useUploadResume();
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFile = useCallback(
    (file: File) => {
      setError(null);
      const ext = `.${file.name.split(".").pop()?.toLowerCase()}`;
      if (!ACCEPTED.includes(ext)) {
        setError("Only PDF and DOCX files are supported.");
        return;
      }
      if (file.size > MAX_MB * 1024 * 1024) {
        setError(`File exceeds the ${MAX_MB} MB limit.`);
        return;
      }
      upload.mutate(file);
    },
    [upload]
  );

  return (
    <div>
      <div
        role="button"
        tabIndex={0}
        onClick={() => inputRef.current?.click()}
        onKeyDown={(e) => e.key === "Enter" && inputRef.current?.click()}
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragging(false);
          const file = e.dataTransfer.files?.[0];
          if (file) handleFile(file);
        }}
        className={cn(
          "flex cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed p-10 text-center transition-colors",
          dragging ? "border-primary bg-primary/5" : "border-border hover:border-primary/50 hover:bg-accent/30"
        )}
      >
        <div className="flex size-14 items-center justify-center rounded-2xl bg-primary/10 text-primary">
          {upload.isPending ? <Loader2 className="size-6 animate-spin" /> : <FileUp className="size-6" />}
        </div>
        <p className="mt-4 font-medium">
          {upload.isPending ? "Uploading & parsing…" : "Drop your resume here"}
        </p>
        <p className="mt-1 text-sm text-muted-foreground">
          or click to browse · PDF or DOCX · up to {formatBytes(MAX_MB * 1024 * 1024, 0)}
        </p>
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.docx"
          className="hidden"
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file) handleFile(file);
            e.target.value = "";
          }}
        />
      </div>
      {error && <p className="mt-2 text-sm text-rose-400">{error}</p>}
    </div>
  );
}
