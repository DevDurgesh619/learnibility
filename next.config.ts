import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // The data layer reads data/ with fs at runtime (paths built from ids), so file tracing cannot see it.
  // Ship it with every server function. On Vercel the question banks are packed first (scripts/vercel).
  outputFileTracingIncludes: {
    '/**': ['./data/**/*'],
  },
  outputFileTracingExcludes: {
    '/**': ['./reference/**/*', './docs/**/*', './scripts/**/*', './prisma/**/*', './.data/**/*'],
  },
  serverExternalPackages: ['better-sqlite3'],
};

export default nextConfig;
