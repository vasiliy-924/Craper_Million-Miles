"use client";

import { ErrorBoundary as ReactErrorBoundary } from "react-error-boundary";

function ErrorFallback({
  error,
  resetErrorBoundary,
}: {
  error: unknown;
  resetErrorBoundary: () => void;
}) {
  const message = error instanceof Error ? error.message : String(error);
  return (
    <div className="flex min-h-[200px] flex-col items-center justify-center gap-4 p-8 text-center">
      <h2 className="text-xl font-semibold text-gray-900">Something went wrong</h2>
      <p className="text-sm text-gray-600">{message}</p>
      <button
        type="button"
        onClick={resetErrorBoundary}
        className="rounded-md bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800"
      >
        Try again
      </button>
    </div>
  );
}

export function ErrorBoundary({ children }: { children: React.ReactNode }) {
  return (
    <ReactErrorBoundary FallbackComponent={ErrorFallback}>
      {children}
    </ReactErrorBoundary>
  );
}
