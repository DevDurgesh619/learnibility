import { defineConfig } from 'vitest/config';
import path from 'node:path';

export default defineConfig({
  resolve: { alias: { '@': path.resolve(__dirname, '.') } },
  test: {
    include: ['**/*.test.ts', '**/*.test.tsx'],
    exclude: ['node_modules/**', '.next/**'],
    coverage: { provider: 'v8', include: ['lib/**/*.ts'], exclude: ['lib/**/*.test.ts', 'lib/types/**'] },
  },
});
