import { sveltekit } from '@sveltejs/kit/vite';
import type { UserConfig } from 'vite';

const config: UserConfig = {
	optimizeDeps: {
        exclude: ["codemirror", 
				  "@codemirror/autocomplete",
				  "@codemirror/commands",
				  "@codemirror/lang-css",
				  "@codemirror/lang-html",
				  "@codemirror/lang-javascript",
				  "@codemirror/language",
				  "@codemirror/state",
				  "@codemirror/view",
			      "@codemirror/lang-python" /* ... */],
    },
	plugins: [sveltekit()],
};

export default config;
