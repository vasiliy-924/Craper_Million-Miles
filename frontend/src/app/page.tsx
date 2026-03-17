"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { getToken } from "@/lib/auth";

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    if (typeof window !== "undefined" && getToken()) {
      router.replace("/cars");
    }
  }, [router]);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gray-50 px-4">
      <h1 className="text-2xl font-bold text-gray-900">
        Thunderbasil × Million Miles – Car Listings
      </h1>
      <p className="mt-2 text-center text-gray-600">
        Browse used cars from Carsensor. Sign in to view the catalog.
      </p>
      <Link
        href="/login"
        className="mt-6 rounded-md bg-gray-900 px-6 py-2 text-sm font-medium text-white hover:bg-gray-800"
      >
        Sign in
      </Link>
    </main>
  );
}
