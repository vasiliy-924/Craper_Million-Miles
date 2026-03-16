"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useCallback } from "react";
import { useDebouncedCallback } from "use-debounce";

export type CarFilterParams = {
  page?: number;
  limit?: number;
  brand?: string;
  model?: string;
  min_price?: number;
  max_price?: number;
  min_year?: number;
  max_year?: number;
  min_mileage?: number;
  max_mileage?: number;
  sort_by?: string;
  sort_order?: "asc" | "desc";
};

const DEFAULT_LIMIT = 20;
const SORT_OPTIONS = [
  { value: "id", label: "ID" },
  { value: "year", label: "Year" },
  { value: "mileage_km", label: "Mileage" },
  { value: "price_jpy", label: "Price" },
  { value: "brand_normalized", label: "Brand" },
  { value: "model_normalized", label: "Model" },
] as const;

export function useCarFilters() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const parseParams = useCallback((): CarFilterParams => {
    const page = searchParams.get("page");
    const limit = searchParams.get("limit");
    const sortBy = searchParams.get("sort_by");
    const sortOrder = searchParams.get("sort_order");

    return {
      page: page ? parseInt(page, 10) : 1,
      limit: limit ? parseInt(limit, 10) : DEFAULT_LIMIT,
      brand: searchParams.get("brand") || undefined,
      model: searchParams.get("model") || undefined,
      min_price: searchParams.get("min_price")
        ? parseInt(searchParams.get("min_price")!, 10)
        : undefined,
      max_price: searchParams.get("max_price")
        ? parseInt(searchParams.get("max_price")!, 10)
        : undefined,
      min_year: searchParams.get("min_year")
        ? parseInt(searchParams.get("min_year")!, 10)
        : undefined,
      max_year: searchParams.get("max_year")
        ? parseInt(searchParams.get("max_year")!, 10)
        : undefined,
      min_mileage: searchParams.get("min_mileage")
        ? parseInt(searchParams.get("min_mileage")!, 10)
        : undefined,
      max_mileage: searchParams.get("max_mileage")
        ? parseInt(searchParams.get("max_mileage")!, 10)
        : undefined,
      sort_by: sortBy || "id",
      sort_order: (sortOrder as "asc" | "desc") || "asc",
    };
  }, [searchParams]);

  const setParams = useCallback(
    (updates: Partial<CarFilterParams>) => {
      const current = parseParams();
      const next = { ...current, ...updates };
      if (updates.page === undefined && updates.brand !== undefined) {
        next.page = 1;
      }
      if (updates.page === undefined && updates.model !== undefined) {
        next.page = 1;
      }

      const params = new URLSearchParams();
      Object.entries(next).forEach(([k, v]) => {
        if (v !== undefined && v !== null && v !== "") {
          params.set(k, String(v));
        }
      });
      router.push(`/cars?${params.toString()}`);
    },
    [parseParams, router]
  );

  const debouncedSetParams = useDebouncedCallback(setParams, 300);

  const setFilter = useCallback(
    (key: keyof CarFilterParams, value: string | number | undefined) => {
      if (key === "brand" || key === "model") {
        debouncedSetParams({ [key]: value || undefined });
      } else {
        setParams({ [key]: value });
      }
    },
    [debouncedSetParams, setParams]
  );

  const clearFilters = useCallback(() => {
    router.push("/cars");
  }, [router]);

  return {
    params: parseParams(),
    setFilter,
    clearFilters,
    SORT_OPTIONS,
  };
}
