import { writable } from "svelte/store";

export const playerNameStore = writable("");
export const roomNameStore = writable("");
export const gameLoopDataStore = writable(null); 
