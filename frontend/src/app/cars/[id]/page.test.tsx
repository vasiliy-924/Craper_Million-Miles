import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { act, render, screen, waitFor } from "@testing-library/react";
import { Suspense } from "react";
import { vi } from "vitest";
import CarDetailPage from "./page";

const mockFetchCarById = vi.fn();

vi.mock("@/lib/api", () => ({
  fetchCarById: (...args: unknown[]) => mockFetchCarById(...args),
}));

vi.mock("next/image", () => ({
  default: ({ src, alt }: { src: string; alt: string }) => (
    <img src={src} alt={alt} />
  ),
}));

function renderWithProviders(ui: React.ReactElement) {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });
  return render(
    <QueryClientProvider client={queryClient}>
      {ui}
    </QueryClientProvider>
  );
}

describe("CarDetailPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders car details", async () => {
    mockFetchCarById.mockResolvedValueOnce({
      id: 1,
      external_id: "AU001",
      source_url: "https://carsensor.net/usedcar/detail/AU001/",
      brand_raw: "トヨタ",
      brand_normalized: "Toyota",
      model_raw: "カムリ",
      model_normalized: "Camry",
      year: 2020,
      mileage_km: 35000,
      price_jpy: 1500000,
      total_price_jpy: null,
      location_raw: "愛知県",
      location_normalized: "Aichi",
      fuel_raw: "ガソリン",
      fuel_normalized: "petrol",
      transmission_raw: "CVT",
      transmission_normalized: "CVT",
      body_type_raw: null,
      body_type_normalized: null,
      color_raw: null,
      dealer_name: "Test Dealer",
      main_image_url: null,
      image_urls: null,
      specs: { Year: "2020", Mileage: "35,000 km" },
      scraped_at: "2024-01-01T00:00:00Z",
      updated_at: "2024-01-01T00:00:00Z",
    });

    await act(async () => {
      renderWithProviders(
        <Suspense fallback={<div>Loading...</div>}>
          <CarDetailPage params={Promise.resolve({ id: "1" })} />
        </Suspense>
      );
    });

    expect(
      await screen.findByText(/Toyota Camry/, {}, { timeout: 5000 })
    ).toBeInTheDocument();
    expect(screen.getByText(/Test Dealer/)).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /view on carsensor/i })).toBeInTheDocument();
  });

  it("shows loading state initially", async () => {
    mockFetchCarById.mockImplementation(() => new Promise(() => {}));

    await act(async () => {
      renderWithProviders(
        <Suspense fallback={<div>Loading...</div>}>
          <CarDetailPage params={Promise.resolve({ id: "1" })} />
        </Suspense>
      );
    });

    await waitFor(() => {
      expect(screen.getByRole("main")).toBeInTheDocument();
    });
  });

  it("shows error for not found", async () => {
    mockFetchCarById.mockRejectedValue(new Error("Not found"));

    await act(async () => {
      renderWithProviders(
        <Suspense fallback={<div>Loading...</div>}>
          <CarDetailPage params={Promise.resolve({ id: "99999" })} />
        </Suspense>
      );
    });

    expect(
      await screen.findByText(/car not found/i, {}, { timeout: 5000 })
    ).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /back to cars/i })).toBeInTheDocument();
  });
});
