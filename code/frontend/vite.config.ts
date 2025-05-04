import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    build: {
        outDir: "../dist/static",
        emptyOutDir: true,
        sourcemap: true
    },
    server: {
        host: true,
        proxy: {
            "/api": {
                target: "http://azure_function:80",
                changeOrigin: true,
                secure: false
            }
        }
    }
});
