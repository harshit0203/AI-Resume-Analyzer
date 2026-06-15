"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";

import { analysisApi } from "@/lib/api/services";
import { extractError } from "@/lib/api/client";

export const analysisKeys = {
  all: ["analyses"] as const,
  list: (params: Record<string, unknown>) => ["analyses", "list", params] as const,
  detail: (id: string) => ["analyses", "detail", id] as const,
  stats: ["analyses", "stats"] as const,
};

export function useAnalyses(params: { page?: number; page_size?: number; resume_id?: string } = {}) {
  return useQuery({
    queryKey: analysisKeys.list(params),
    queryFn: () => analysisApi.list(params),
  });
}

export function useAnalysis(id: string, options: { poll?: boolean } = {}) {
  return useQuery({
    queryKey: analysisKeys.detail(id),
    queryFn: () => analysisApi.get(id),
    enabled: Boolean(id),
    refetchInterval: (query) => {
      const status = query.state.data?.status;
      return options.poll && (status === "pending" || status === "running") ? 2500 : false;
    },
  });
}

export function useAnalysisStats() {
  return useQuery({ queryKey: analysisKeys.stats, queryFn: analysisApi.stats });
}

export function useCreateAnalysis() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: { resume_id: string; target_role?: string }) =>
      analysisApi.create(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: analysisKeys.all });
      toast.success("Analysis started.");
    },
    onError: (error) => toast.error(extractError(error).message),
  });
}

export function useDeleteAnalysis() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => analysisApi.remove(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: analysisKeys.all });
      toast.success("Analysis deleted.");
    },
    onError: (error) => toast.error(extractError(error).message),
  });
}
