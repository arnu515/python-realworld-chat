import type { ChatRequests } from "$lib/types/db";
import { writable } from "svelte/store";
import axios from "axios";
import { parseFastAPIError } from "$lib/util";

export const chatRequests = (() => {
  const { subscribe, set, update } = writable<{
    sent: ChatRequests[];
    received: ChatRequests[];
  } | null>(null);

  return {
    subscribe,
    set,
    update,
    refetch: async () => {
      try {
        const { data } = await axios.get("/api/chat/requests");
        set(data);
      } catch (e) {
        if (e.response) {
          alert(parseFastAPIError(e.response.data));
        } else {
          alert("Unknown error");
          console.error(e);
        }
      }
    }
  };
})();
