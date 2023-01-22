import { writable } from "svelte/store";

// set editor mode var vim / emacs
export const editorMode = writable("emacs");
