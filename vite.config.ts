import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
  root: resolve(__dirname, 'frontend'), // Set the root to the frontend folder
  plugins: [react()],
  build: {
    outDir: resolve(__dirname, 'dist'),
  },
});