"use client";

import { useMutation } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { login } from "@/lib/api";
import { useAuthStore } from "@/stores/auth";

export function useLogin() {
  const router = useRouter();

  const mutation = useMutation({
    mutationFn: login,
    onSuccess: (data) => {
      useAuthStore.getState().setToken(data.access_token);
      router.push("/cars");
    },
  });

  return {
    mutate: mutation.mutate,
    isPending: mutation.isPending,
    error: mutation.error,
  };
}
