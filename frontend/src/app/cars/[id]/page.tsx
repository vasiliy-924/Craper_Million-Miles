"use client";

import Image from "next/image";
import Link from "next/link";
import { use, useEffect } from "react";
import { CarDetailSkeleton } from "@/components/CarDetailSkeleton";
import { useCarDetail } from "@/hooks/useCarDetail";

function formatPrice(price: number | null): string {
  if (price == null) return "Price on request";
  return `¥${price.toLocaleString()}`;
}

function formatMileage(km: number | null): string {
  if (km == null) return "—";
  return `${km.toLocaleString()} km`;
}

function orNormalized(normalized: string | null, raw: string | null): string {
  return normalized || raw || "—";
}

export default function CarDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id: idStr } = use(params);
  const id = parseInt(idStr, 10);
  const { data: car, isLoading, error, isError } = useCarDetail(id);

  useEffect(() => {
    if (car) {
      const title = `${orNormalized(car.brand_normalized, car.brand_raw)} ${orNormalized(car.model_normalized, car.model_raw)} | 25 Million Miles`;
      document.title = title;
    }
  }, [car]);

  if (isLoading) {
    return (
      <main className="min-h-screen bg-gray-50 px-4 py-6">
        <div className="mx-auto max-w-4xl">
          <CarDetailSkeleton />
        </div>
      </main>
    );
  }

  if (isError || !car) {
    return (
      <main className="min-h-screen bg-gray-50 px-4 py-6">
        <div className="mx-auto max-w-4xl">
          <p className="rounded-lg border border-gray-200 bg-white p-8 text-center text-gray-600">
            Car not found
          </p>
          <Link
            href="/cars"
            className="mt-4 inline-block text-sm text-gray-600 hover:text-gray-900"
          >
            Back to cars
          </Link>
        </div>
      </main>
    );
  }

  const brandModel = `${orNormalized(car.brand_normalized, car.brand_raw)} ${orNormalized(car.model_normalized, car.model_raw)}`;
  const images = car.image_urls?.length ? car.image_urls : car.main_image_url ? [car.main_image_url] : [];
  const mainImage = car.main_image_url || images[0];

  return (
    <main className="min-h-screen bg-gray-50 px-4 py-6">
      <div className="mx-auto max-w-4xl">
        <Link
          href="/cars"
          className="mb-4 inline-block text-sm text-gray-600 hover:text-gray-900"
        >
          ← Back to cars
        </Link>

        <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
          <h1 className="text-2xl font-bold text-gray-900">{brandModel}</h1>

          <div className="mt-6">
            <div className="relative aspect-video w-full overflow-hidden rounded-lg bg-gray-100">
              {mainImage ? (
                <Image
                  src={mainImage}
                  alt={brandModel}
                  fill
                  className="object-contain"
                  sizes="(max-width: 768px) 100vw, 896px"
                  priority
                />
              ) : (
                <div className="flex h-full items-center justify-center text-gray-400">
                  <svg
                    className="h-24 w-24"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={1.5}
                      d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                    />
                  </svg>
                </div>
              )}
            </div>
            {images.length > 1 && (
              <div className="mt-2 flex gap-2 overflow-x-auto pb-2">
                {images.slice(0, 8).map((url, i) => (
                  <div
                    key={i}
                    className="relative h-16 w-24 flex-shrink-0 overflow-hidden rounded"
                  >
                    <Image
                      src={url}
                      alt={`${brandModel} ${i + 1}`}
                      fill
                      className="object-cover"
                      sizes="96px"
                    />
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="mt-6 grid gap-4 sm:grid-cols-2">
            <div>
              <h2 className="text-sm font-medium text-gray-500">Year</h2>
              <p className="text-gray-900">{car.year ?? "—"}</p>
            </div>
            <div>
              <h2 className="text-sm font-medium text-gray-500">Mileage</h2>
              <p className="text-gray-900">{formatMileage(car.mileage_km)}</p>
            </div>
            <div>
              <h2 className="text-sm font-medium text-gray-500">Price</h2>
              <p className="font-semibold text-gray-900">
                {formatPrice(car.price_jpy)}
              </p>
            </div>
            <div>
              <h2 className="text-sm font-medium text-gray-500">Location</h2>
              <p className="text-gray-900">
                {orNormalized(car.location_normalized, car.location_raw)}
              </p>
            </div>
            <div>
              <h2 className="text-sm font-medium text-gray-500">Fuel</h2>
              <p className="text-gray-900">
                {orNormalized(car.fuel_normalized, car.fuel_raw)}
              </p>
            </div>
            <div>
              <h2 className="text-sm font-medium text-gray-500">Transmission</h2>
              <p className="text-gray-900">
                {orNormalized(car.transmission_normalized, car.transmission_raw)}
              </p>
            </div>
            <div>
              <h2 className="text-sm font-medium text-gray-500">Body type</h2>
              <p className="text-gray-900">
                {orNormalized(car.body_type_normalized, car.body_type_raw)}
              </p>
            </div>
            <div>
              <h2 className="text-sm font-medium text-gray-500">Dealer</h2>
              <p className="text-gray-900">{car.dealer_name || "—"}</p>
            </div>
          </div>

          {car.specs && Object.keys(car.specs).length > 0 && (
            <div className="mt-8">
              <h2 className="mb-4 text-lg font-semibold text-gray-900">Specifications</h2>
              <div className="overflow-hidden rounded border border-gray-200">
                <table className="w-full text-sm">
                  <tbody>
                    {Object.entries(car.specs).map(([key, value]) => (
                      <tr
                        key={key}
                        className="border-b border-gray-100 last:border-0 odd:bg-gray-50"
                      >
                        <td className="px-4 py-2 font-medium text-gray-600">
                          {key}
                        </td>
                        <td className="px-4 py-2 text-gray-900">
                          {String(value ?? "—")}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {car.source_url && (
            <div className="mt-6">
              <a
                href={car.source_url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 text-sm font-medium text-gray-600 hover:text-gray-900"
              >
                View on Carsensor
                <svg
                  className="h-4 w-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                  />
                </svg>
              </a>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
