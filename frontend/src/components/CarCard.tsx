"use client";

import Image from "next/image";
import Link from "next/link";
import type { CarListItem } from "@/lib/api";

function formatPrice(price: number | null): string {
  if (price == null) return "Price on request";
  return `¥${price.toLocaleString()}`;
}

function formatMileage(km: number | null): string {
  if (km == null) return "—";
  return `${km.toLocaleString()} km`;
}

export function CarCard({ car }: { car: CarListItem }) {
  const brandModel = [car.brand_normalized, car.model_normalized]
    .filter(Boolean)
    .join(" ") || "—";

  return (
    <Link
      href={`/cars/${car.id}`}
      className="group block overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm transition-shadow hover:shadow-md"
    >
      <div className="relative aspect-[4/3] w-full bg-gray-100">
        {car.main_image_url ? (
          <Image
            src={car.main_image_url}
            alt={brandModel}
            fill
            className="object-cover transition-transform group-hover:scale-105"
            sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 25vw"
          />
        ) : (
          <div className="flex h-full items-center justify-center text-gray-400">
            <svg
              className="h-16 w-16"
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
      <div className="p-4">
        <h3 className="font-semibold text-gray-900">{brandModel}</h3>
        <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-sm text-gray-600">
          {car.year != null && <span>{car.year}</span>}
          <span>{formatMileage(car.mileage_km)}</span>
        </div>
        <p className="mt-2 font-medium text-gray-900">{formatPrice(car.price_jpy)}</p>
      </div>
    </Link>
  );
}
