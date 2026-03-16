"use client";

import { useQuery } from "@tanstack/react-query";
import { fetchCars, type CarListParams } from "@/lib/api";

export function useCars(params: CarListParams) {
  const query = useQuery({
    queryKey: ["cars", params],
    queryFn: () => fetchCars(params),
  });

  return {
    data: query.data,
    isLoading: query.isLoading,
    error: query.error,
  };
}
