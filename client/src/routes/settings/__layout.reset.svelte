<script lang="ts">
  import Auth from "$lib/components/Auth.svelte";
  import Header from "$lib/components/Header.svelte";
  import IconSidebar from "$lib/components/IconSidebar.svelte";
  import { fetchUser, user } from "$lib/stores/user";
  import axios from "axios";
  import { onMount } from "svelte";
  import "$lib/styles/settings-form.css";

  let loading = true;

  axios.defaults.withCredentials = true;
  axios.defaults.baseURL = import.meta.env.VITE_SERVER_URL?.toString?.() || "/";

  onMount(() => fetchUser().then(() => (loading = false)));
</script>

{#if !loading}
  {#if $user}
    <IconSidebar
      items={[
        {
          icon: `<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
</svg>`,
          tooltip: "Home",
          href: "/"
        },
        {
          icon: `<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0m-5 8a2 2 0 100-4 2 2 0 000 4zm0 0c1.306 0 2.417.835 2.83 2M9 14a3.001 3.001 0 00-2.83 2M15 11h3m-3 4h2" />
</svg>`,
          tooltip: "Profile",
          href: "/settings/profile"
        },
        {
          icon: `<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
</svg>`,
          tooltip: "Account",
          href: "/settings/account"
        }
      ]}
    />
    <div class="ml-16">
      <slot />
    </div>
  {:else}
    <Header />
    <Auth />
  {/if}
{/if}
