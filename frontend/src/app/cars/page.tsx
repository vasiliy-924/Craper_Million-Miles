"use client";

import { useEffect, useState } from "react";
import { CarCard } from "@/components/CarCard";
import { CarCardSkeleton } from "@/components/CarCardSkeleton";
import { useCars } from "@/hooks/useCars";
import { useCarFilters } from "@/hooks/useCarFilters";

export default function CarsPage() {
  const { params, setFilter, clearFilters, SORT_OPTIONS } = useCarFilters();
  const { data, isLoading, error } = useCars(params);

  const [brandInput, setBrandInput] = useState(params.brand ?? "");
  const [modelInput, setModelInput] = useState(params.model ?? "");

  useEffect(() => {
    setBrandInput(params.brand ?? "");
    setModelInput(params.model ?? "");
  }, [params.brand, params.model]);

  return (
    <main className="min-h-screen bg-gray-50">
      <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
        <h1 className="mb-6 text-2xl font-bold text-gray-900">Cars</h1>

        <div className="mb-6 rounded-lg border border-gray-200 bg-white p-4">
          <div className="mb-2 flex flex-wrap items-center justify-between gap-2">
            <h2 className="text-sm font-medium text-gray-700">Filters</h2>
            <button
              type="button"
              onClick={clearFilters}
              className="text-sm text-gray-600 hover:text-gray-900"
            >
              Clear all
            </button>
          </div>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-6">
            <div>
              <label htmlFor="brand" className="mb-1 block text-xs font-medium text-gray-600">
                Brand
              </label>
              <input
                id="brand"
                type="text"
                value={brandInput}
                onChange={(e) => {
                  setBrandInput(e.target.value);
                  setFilter("brand", e.target.value);
                }}
                placeholder="e.g. Toyota"
                className="min-h-[44px] w-full rounded border border-gray-300 bg-white px-2 py-1.5 text-sm text-gray-900 placeholder:text-gray-500"
              />
            </div>
            <div>
              <label htmlFor="model" className="mb-1 block text-xs font-medium text-gray-600">
                Model
              </label>
              <input
                id="model"
                type="text"
                value={modelInput}
                onChange={(e) => {
                  setModelInput(e.target.value);
                  setFilter("model", e.target.value);
                }}
                placeholder="e.g. Camry"
                className="min-h-[44px] w-full rounded border border-gray-300 bg-white px-2 py-1.5 text-sm text-gray-900 placeholder:text-gray-500"
              />
            </div>
            <div>
              <label htmlFor="min_price" className="mb-1 block text-xs font-medium text-gray-600">
                Min price (JPY)
              </label>
              <input
                id="min_price"
                type="number"
                value={params.min_price ?? ""}
                onChange={(e) =>
                  setFilter("min_price", e.target.value ? parseInt(e.target.value, 10) : undefined)
                }
                placeholder="0"
                className="min-h-[44px] w-full rounded border border-gray-300 bg-white px-2 py-1.5 text-sm text-gray-900 placeholder:text-gray-500"
              />
            </div>
            <div>
              <label htmlFor="max_price" className="mb-1 block text-xs font-medium text-gray-600">
                Max price (JPY)
              </label>
              <input
                id="max_price"
                type="number"
                value={params.max_price ?? ""}
                onChange={(e) =>
                  setFilter("max_price", e.target.value ? parseInt(e.target.value, 10) : undefined)
                }
                placeholder="—"
                className="min-h-[44px] w-full rounded border border-gray-300 bg-white px-2 py-1.5 text-sm text-gray-900 placeholder:text-gray-500"
              />
            </div>
            <div>
              <label htmlFor="min_year" className="mb-1 block text-xs font-medium text-gray-600">
                Min year
              </label>
              <input
                id="min_year"
                type="number"
                value={params.min_year ?? ""}
                onChange={(e) =>
                  setFilter("min_year", e.target.value ? parseInt(e.target.value, 10) : undefined)
                }
                placeholder="—"
                className="min-h-[44px] w-full rounded border border-gray-300 bg-white px-2 py-1.5 text-sm text-gray-900 placeholder:text-gray-500"
              />
            </div>
            <div>
              <label htmlFor="max_year" className="mb-1 block text-xs font-medium text-gray-600">
                Max year
              </label>
              <input
                id="max_year"
                type="number"
                value={params.max_year ?? ""}
                onChange={(e) =>
                  setFilter("max_year", e.target.value ? parseInt(e.target.value, 10) : undefined)
                }
                placeholder="—"
                className="min-h-[44px] w-full rounded border border-gray-300 bg-white px-2 py-1.5 text-sm text-gray-900 placeholder:text-gray-500"
              />
            </div>
            <div>
              <label htmlFor="min_mileage" className="mb-1 block text-xs font-medium text-gray-600">
                Min mileage (km)
              </label>
              <input
                id="min_mileage"
                type="number"
                value={params.min_mileage ?? ""}
                onChange={(e) =>
                  setFilter("min_mileage", e.target.value ? parseInt(e.target.value, 10) : undefined)
                }
                placeholder="—"
                className="min-h-[44px] w-full rounded border border-gray-300 bg-white px-2 py-1.5 text-sm text-gray-900 placeholder:text-gray-500"
              />
            </div>
            <div>
              <label htmlFor="max_mileage" className="mb-1 block text-xs font-medium text-gray-600">
                Max mileage (km)
              </label>
              <input
                id="max_mileage"
                type="number"
                value={params.max_mileage ?? ""}
                onChange={(e) =>
                  setFilter("max_mileage", e.target.value ? parseInt(e.target.value, 10) : undefined)
                }
                placeholder="—"
                className="min-h-[44px] w-full rounded border border-gray-300 bg-white px-2 py-1.5 text-sm text-gray-900 placeholder:text-gray-500"
              />
            </div>
            <div>
              <label htmlFor="sort_by" className="mb-1 block text-xs font-medium text-gray-600">
                Sort by
              </label>
              <select
                id="sort_by"
                value={params.sort_by}
                onChange={(e) => setFilter("sort_by", e.target.value)}
                className="min-h-[44px] w-full rounded border border-gray-300 bg-white px-2 py-1.5 text-sm text-gray-900 placeholder:text-gray-500"
              >
                {SORT_OPTIONS.map((opt) => (
                  <option key={opt.value} value={opt.value}>
                    {opt.label}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label htmlFor="sort_order" className="mb-1 block text-xs font-medium text-gray-600">
                Order
              </label>
              <select
                id="sort_order"
                value={params.sort_order}
                onChange={(e) => setFilter("sort_order", e.target.value as "asc" | "desc")}
                className="min-h-[44px] w-full rounded border border-gray-300 bg-white px-2 py-1.5 text-sm text-gray-900 placeholder:text-gray-500"
              >
                <option value="asc">Ascending</option>
                <option value="desc">Descending</option>
              </select>
            </div>
          </div>
        </div>

        {error && (
          <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-red-700">
            {error instanceof Error ? error.message : "Failed to load cars"}
          </div>
        )}

        {isLoading && (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {Array.from({ length: 8 }).map((_, i) => (
              <CarCardSkeleton key={i} />
            ))}
          </div>
        )}

        {!isLoading && data && (
          <>
            <p className="mb-4 text-sm text-gray-600">
              {data.total} car{data.total !== 1 ? "s" : ""} found
            </p>
            {data.items.length === 0 ? (
              <p className="rounded-lg border border-gray-200 bg-white p-8 text-center text-gray-600">
                No cars found
              </p>
            ) : (
              <>
                <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                  {data.items.map((car) => (
                    <CarCard key={car.id} car={car} />
                  ))}
                </div>
                {data.pages > 1 && (
                  <div className="mt-6 flex items-center justify-center gap-2">
                    <button
                      type="button"
                      onClick={() => setFilter("page", (params.page ?? 1) - 1)}
                      disabled={(params.page ?? 1) <= 1}
                      className="min-h-[44px] min-w-[44px] rounded border border-gray-300 bg-white px-3 py-1 text-sm text-gray-900 disabled:opacity-50"
                    >
                      Previous
                    </button>
                    <span className="text-sm text-gray-600">
                      Page {data.page} of {data.pages}
                    </span>
                    <button
                      type="button"
                      onClick={() => setFilter("page", (params.page ?? 1) + 1)}
                      disabled={(params.page ?? 1) >= data.pages}
                      className="min-h-[44px] min-w-[44px] rounded border border-gray-300 bg-white px-3 py-1 text-sm text-gray-900 disabled:opacity-50"
                    >
                      Next
                    </button>
                  </div>
                )}
              </>
            )}
          </>
        )}
      </div>
    </main>
  );
}
