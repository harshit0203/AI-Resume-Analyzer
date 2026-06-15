"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";

import { userApi } from "@/lib/api/services";
import { extractError } from "@/lib/api/client";
import { useAuthStore } from "@/lib/stores/auth-store";
import type { User, UserSettings } from "@/lib/types";

export function useSettings() {
  return useQuery({ queryKey: ["settings"], queryFn: userApi.getSettings });
}

export function useUpdateSettings() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: Partial<UserSettings>) => userApi.updateSettings(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["settings"] });
      toast.success("Settings updated.");
    },
    onError: (error) => toast.error(extractError(error).message),
  });
}

export function useUpdateProfile() {
  const setUser = useAuthStore((s) => s.setUser);
  return useMutation({
    mutationFn: (payload: Partial<Pick<User, "full_name" | "headline" | "avatar_url">>) =>
      userApi.updateProfile(payload),
    onSuccess: (user) => {
      setUser(user);
      toast.success("Profile updated.");
    },
    onError: (error) => toast.error(extractError(error).message),
  });
}

export function useChangePassword() {
  return useMutation({
    mutationFn: (payload: { current_password: string; new_password: string }) =>
      userApi.changePassword(payload),
    onSuccess: () => toast.success("Password changed."),
    onError: (error) => toast.error(extractError(error).message),
  });
}
