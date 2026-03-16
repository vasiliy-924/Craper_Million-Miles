export function CarCardSkeleton() {
  return (
    <div className="overflow-hidden rounded-lg border border-gray-200 bg-white">
      <div className="aspect-[4/3] w-full animate-pulse bg-gray-200" />
      <div className="p-4">
        <div className="h-5 w-3/4 animate-pulse rounded bg-gray-200" />
        <div className="mt-2 flex gap-4">
          <div className="h-4 w-12 animate-pulse rounded bg-gray-200" />
          <div className="h-4 w-16 animate-pulse rounded bg-gray-200" />
        </div>
        <div className="mt-2 h-5 w-24 animate-pulse rounded bg-gray-200" />
      </div>
    </div>
  );
}
