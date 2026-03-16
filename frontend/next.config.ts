import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactCompiler: true,
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "carsensor.net",
        pathname: "/**",
      },
      {
        protocol: "https",
        hostname: "*.carsensor.net",
        pathname: "/**",
      },
    ],
  },
};

export default nextConfig;
