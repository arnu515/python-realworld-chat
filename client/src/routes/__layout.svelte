<script lang="ts">
  import Header from "$lib/components/Header.svelte";
  import { user } from "$lib/stores/user";
  import { onMount } from "svelte";
  import axios from "axios";
  import type { AxiosError } from "axios";
  import "../app.css";

  axios.defaults.withCredentials = true;
  axios.defaults.baseURL = import.meta.env.VITE_SERVER_URL?.toString?.() || "/";

  let loading = true;

  onMount(() => {
    axios
      .get("/api/auth/me")
      .then(({ data }) => {
        $user = data.user;
        loading = false;
      })
      .catch((e: AxiosError) => {
        if (e.response.status === 401) {
          $user = null;
          loading = false;
        } else {
          throw e;
        }
      });
  });
</script>

{#if !loading}
  <Header />
  <slot />
{/if}
