import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Export static HTML during build for simple static hosting
  output: "export",
  async rewrites() {
    if (process.env.NODE_ENV === "development") {
      return [
        {
          source: "/api/:path*",
          destination: "http://localhost:8001/api/:path*",
        },
      ];
    }
    return [];
  },
};

export default nextConfig;
