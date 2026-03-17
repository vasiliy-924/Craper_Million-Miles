import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen, waitFor } from "@testing-library/react";
import { vi } from "vitest";
import CarsPage from "./page";

const mockFetchCars = vi.fn();

vi.mock("@/lib/api", () => ({
  fetchCars: (...args: unknown[]) => mockFetchCars(...args),
}));

vi.mock("next/navigation", () => ({
  useRouter: vi.fn(() => ({ push: vi.fn() })),
  useSearchParams: vi.fn(() => ({
    get: (key: string) => {
      const params: Record<string, string> = {
        page: "1",
        limit: "20",
        sort_by: "id",
        sort_order: "asc",
      };
      return params[key] ?? null;
    },
  })),
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

describe("CarsPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders cars list", async () => {
    mockFetchCars.mockResolvedValue({
      items: [
        {
          id: 1,
          external_id: "AU001",
          brand_normalized: "Toyota",
          model_normalized: "Camry",
          year: 2020,
          mileage_km: 35000,
          price_jpy: 1500000,
          location_normalized: "Aichi",
          main_image_url: null,
        },
      ],
      total: 1,
      page: 1,
      limit: 20,
      pages: 1,
    });

    renderWithProviders(<CarsPage />);

    await waitFor(() => {
      expect(screen.getByText(/Toyota Camry/)).toBeInTheDocument();
    });
    expect(screen.getByText(/1 car found/)).toBeInTheDocument();
  });

  it("shows loading state", () => {
    mockFetchCars.mockImplementation(() => new Promise(() => {}));

    renderWithProviders(<CarsPage />);

    expect(screen.getByRole("heading", { name: /cars/i })).toBeInTheDocument();
    expect(screen.getByText(/filters/i)).toBeInTheDocument();
  });

  it("shows empty state", async () => {
    mockFetchCars.mockResolvedValue({
      items: [],
      total: 0,
      page: 1,
      limit: 20,
      pages: 0,
    });

    renderWithProviders(<CarsPage />);

    await waitFor(() => {
      expect(screen.getByText(/no cars found/i)).toBeInTheDocument();
    });
  });

  it("renders filters", () => {
    mockFetchCars.mockResolvedValue({
      items: [],
      total: 0,
      page: 1,
      limit: 20,
      pages: 0,
    });

    renderWithProviders(<CarsPage />);

    expect(screen.getByLabelText(/brand/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/model/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/min price/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/max price/i)).toBeInTheDocument();
  });
});
