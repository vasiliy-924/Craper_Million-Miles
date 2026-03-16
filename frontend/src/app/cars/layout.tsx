"use client";

import { AuthGuard } from "@/components/AuthGuard";

export default function CarsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <AuthGuard>{children}</AuthGuard>;
}
