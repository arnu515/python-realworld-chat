<script lang="ts">
  import Header from "$lib/components/Header.svelte";
  import { fetchUser, user } from "$lib/stores/user";
  import { onMount } from "svelte";
  import axios from "axios";
  import "../app.css";
  import Auth from "$lib/components/Auth.svelte";
  import Sidebar from "$lib/components/Sidebar.svelte";

  axios.defaults.withCredentials = true;
  axios.defaults.baseURL = import.meta.env.VITE_SERVER_URL?.toString?.() || "/";

  let loading = true;

  onMount(() => {
    fetchUser().then(() => (loading = false));
  });
</script>

{#if !loading}
  {#if !$user}
    <Header />
    <Auth />
  {:else}
    <div class="m-4 min-h-[99vh] grid gap-4" style="grid-template-columns: 300px auto">
      <Sidebar />
      <slot />
    </div>
  {/if}
{/if}
