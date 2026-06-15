"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { toast } from "sonner";

import { authApi } from "@/lib/api/services";
import { extractError } from "@/lib/api/client";
import { useAuthStore } from "@/lib/stores/auth-store";

export function useLogin() {
  const router = useRouter();
  const setUser = useAuthStore((s) => s.setUser);
  return useMutation({
    mutationFn: authApi.login,
    onSuccess: (data) => {
      setUser(data.user);
      toast.success(`Welcome back, ${data.user.full_name ?? "there"}!`);
      router.push("/dashboard");
    },
    onError: (error) => toast.error(extractError(error).message),
  });
}

export function useRegister() {
  const router = useRouter();
  const setUser = useAuthStore((s) => s.setUser);
  return useMutation({
    mutationFn: authApi.register,
    onSuccess: (data) => {
      setUser(data.user);
      toast.success("Account created. Welcome aboard!");
      router.push("/dashboard");
    },
    onError: (error) => toast.error(extractError(error).message),
  });
}

export function useLogout() {
  const router = useRouter();
  const clear = useAuthStore((s) => s.clear);
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: authApi.logout,
    onSuccess: () => {
      clear();
      queryClient.clear();
      toast.success("Signed out.");
      router.push("/login");
    },
  });
}
