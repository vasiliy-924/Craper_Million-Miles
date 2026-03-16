export function CarDetailSkeleton() {
  return (
    <div className="mx-auto max-w-4xl animate-pulse">
      <div className="aspect-video w-full rounded-lg bg-gray-200" />
      <div className="mt-6 space-y-4">
        <div className="h-8 w-2/3 rounded bg-gray-200" />
        <div className="flex gap-4">
          <div className="h-4 w-24 rounded bg-gray-200" />
          <div className="h-4 w-32 rounded bg-gray-200" />
          <div className="h-4 w-20 rounded bg-gray-200" />
        </div>
        <div className="h-6 w-1/4 rounded bg-gray-200" />
        <div className="grid gap-2 sm:grid-cols-2">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="h-4 rounded bg-gray-200" />
          ))}
        </div>
      </div>
    </div>
  );
}
