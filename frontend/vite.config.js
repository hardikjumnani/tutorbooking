import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// During local development, Vite serves the UI on port 5173 and forwards any
// request starting with /api to the FastAPI backend (port 8000 by default).
// Set VITE_API_TARGET to use a different backend port, e.g. if 8000 is busy.
const apiTarget = process.env.VITE_API_TARGET || 'http://localhost:8000'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': apiTarget,
    },
  },
})
