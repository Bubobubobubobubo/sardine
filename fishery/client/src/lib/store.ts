import { writable } from "svelte/store";

// Choosing an editor mode between Emacs (default) and Vim
export const editorMode = writable("emacs");
export const selectedTab = writable(null);
export const selectedPanel = writable(null);