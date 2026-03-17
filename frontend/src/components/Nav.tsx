"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { getToken } from "@/lib/auth";
import { useAuthStore } from "@/stores/auth";

export function Nav() {
  const router = useRouter();
  const token = useAuthStore((s) => s.token);
  const clearToken = useAuthStore((s) => s.clearToken);
  const [mounted, setMounted] = useState(false);

  // Defer auth-dependent rendering until after hydration to avoid server/client mismatch
  useEffect(() => setMounted(true), []);

  const isAuthenticated = mounted && (!!token || !!getToken());

  const handleLogout = () => {
    clearToken();
    router.replace("/login");
  };

  return (
    <nav className="border-b border-gray-200 bg-white">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">
        <Link
          href="/"
          className="text-lg font-semibold text-gray-900 hover:text-gray-700"
        >
          Thunderbasil × Million Miles
        </Link>
        <div className="flex items-center gap-4">
          {isAuthenticated ? (
            <>
              <Link
                href="/cars"
                className="text-sm font-medium text-gray-600 hover:text-gray-900"
              >
                Cars
              </Link>
              <button
                type="button"
                onClick={handleLogout}
                className="text-sm font-medium text-gray-600 hover:text-gray-900"
              >
                Logout
              </button>
            </>
          ) : (
            <Link
              href="/login"
              className="text-sm font-medium text-gray-600 hover:text-gray-900"
            >
              Sign in
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
}
