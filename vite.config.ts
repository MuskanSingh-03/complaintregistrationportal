import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindPlugin from '@tailwindcss/vite'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), tailwindPlugin()],
  build: {
    outDir: 'dist',
    sourcemap: false,
  },
  server: {
    port: 3000,
  }
})
