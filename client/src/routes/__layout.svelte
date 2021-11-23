<script lang="ts" context="module">
  import type { Load } from "@sveltejs/kit";

  export const load: Load = ({ page: { query } }) => {
    return {
      props: {
        addUser: query.get("add_user") || null
      }
    };
  };
</script>

<script lang="ts">
  import Header from "$lib/components/Header.svelte";
  import { fetchUser, user } from "$lib/stores/user";
  import { onMount } from "svelte";
  import axios from "axios";
  import "../app.css";
  import Auth from "$lib/components/Auth.svelte";
  import Sidebar from "$lib/components/Sidebar.svelte";
  import AddUserModal from "$lib/components/AddUserModal.svelte";
  import { chatRequests } from "$lib/stores/chat";

  axios.defaults.withCredentials = true;
  axios.defaults.baseURL = import.meta.env.VITE_SERVER_URL?.toString?.() || "/";

  let loading = true;
  let socket: WebSocket;
  let isAddModalVisible = false;
  export let addUser: string | null;

  onMount(async () => {
    await fetchUser();
    loading = false;

    if (!$user) return;
    const wsUrl = new URL(axios.defaults.baseURL, window.location.origin);
    wsUrl.protocol = wsUrl.protocol === "https" ? "wss" : "ws";
    wsUrl.pathname = "/ws/main";
    socket = new WebSocket(wsUrl.toString());
    socket.onopen = () => {
      console.log("Connected to websocket");
    };
    socket.onmessage = event => {
      const data = JSON.parse(event.data);
      switch (data.type) {
        case "error":
          alert("An error occcured: " + data.message);
          console.error(data.message);
          break;
        case "message":
          alert(data.message);
          break;
        case "new_chat_request":
          alert("Received a new chat request!");
          break;
        case "chat_request_accepted":
          alert("Someone accepted your chat request!");
          break;
        case "chat_request_declined":
          chatRequests.refetch();
          break;
      }
    };

    // TODO: remove in prod
    // to access in console
    window["socket"] = socket;

    if (addUser) {
      isAddModalVisible = true;
    }

    // fetch chat requests
    chatRequests.refetch();
  });
</script>

{#if !loading}
  {#if !$user}
    <Header />
    <Auth />
  {:else}
    <div class="m-4 min-h-[99vh] grid gap-4" style="grid-template-columns: 300px auto">
      <Sidebar on:modal-add={() => (isAddModalVisible = true)} />
      <slot />

      {#if isAddModalVisible}
        <AddUserModal
          on:close={() => (isAddModalVisible = false)}
          identifier={addUser}
        />
      {/if}
    </div>
  {/if}
{/if}
