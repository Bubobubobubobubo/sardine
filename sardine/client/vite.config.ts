// vite.config.js
import { defineConfig } from 'vite';
import tailwindcss from 'tailwindcss';

export default defineConfig({
    plugins: [],
    resolve: {
        /*something*/
    },
    css: {
        postcss: {
            plugins: [tailwindcss],
        },
    },
    build: {
        chunkSizeWarningLimit: 1600
    }
});
