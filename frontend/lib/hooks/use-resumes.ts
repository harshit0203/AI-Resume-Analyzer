"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";

import { resumeApi } from "@/lib/api/services";
import { extractError } from "@/lib/api/client";

export const resumeKeys = {
  all: ["resumes"] as const,
  list: (params: Record<string, unknown>) => ["resumes", "list", params] as const,
  detail: (id: string) => ["resumes", "detail", id] as const,
};

export function useResumes(params: { page?: number; page_size?: number; search?: string } = {}) {
  return useQuery({
    queryKey: resumeKeys.list(params),
    queryFn: () => resumeApi.list(params),
  });
}

export function useResume(id: string) {
  return useQuery({
    queryKey: resumeKeys.detail(id),
    queryFn: () => resumeApi.get(id),
    enabled: Boolean(id),
  });
}

export function useUploadResume() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (file: File) => resumeApi.upload(file),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: resumeKeys.all });
      toast.success("Resume uploaded and parsed.");
    },
    onError: (error) => toast.error(extractError(error).message),
  });
}

export function useDeleteResume() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => resumeApi.remove(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: resumeKeys.all });
      toast.success("Resume deleted.");
    },
    onError: (error) => toast.error(extractError(error).message),
  });
}

export function useSetPrimaryResume() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => resumeApi.setPrimary(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: resumeKeys.all });
      toast.success("Primary resume updated.");
    },
    onError: (error) => toast.error(extractError(error).message),
  });
}
