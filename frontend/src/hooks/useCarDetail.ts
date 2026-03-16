"use client";

import { useQuery } from "@tanstack/react-query";
import { fetchCarById } from "@/lib/api";

export function useCarDetail(id: number) {
  const query = useQuery({
    queryKey: ["car", id],
    queryFn: () => fetchCarById(id),
    enabled: !Number.isNaN(id) && id > 0,
  });

  return {
    data: query.data,
    isLoading: query.isLoading,
    error: query.error,
    isError: query.isError,
  };
}
