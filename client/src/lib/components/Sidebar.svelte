<script lang="ts">
  import { chatRequests } from "$lib/stores/chat";
  import { user } from "$lib/stores/user";
  import { createEventDispatcher } from "svelte";
  let showMenu = false;

  const d = createEventDispatcher();
</script>

<div class="bg-gray-200 rounded border border-gray-400">
  <header
    class="bg-gray-300 border-b border-black flex justify-between items-center px-4 py-2"
    style="border-top-left-radius: 0.25rem; border-top-right-radius: 0.25rem;"
  >
    <div class="flex items-center gap-2">
      <img src={$user.profile.avatar} alt="Your avatar" class="rounded-full w-8 h-8" />
      <p class="text-xl font-bold">{$user.profile.name}</p>
    </div>
    <div class="relative">
      <button
        class="cursor-pointer"
        aria-label="Menu"
        aria-haspopup={showMenu}
        on:click={() => (showMenu = !showMenu)}
        ><svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"
          />
        </svg></button
      >
      {#if showMenu}
        <ul
          class="absolute right-0 m-0 mt-1 w-48 bg-white rounded shadow z-20 list-none p-0"
        >
          <li>
            <button on:click={() => d("modal-add")} class="menu-list-item"
              >Add a person</button
            >
            <a href="/settings" class="menu-list-item">Settings</a>
          </li>
        </ul>
      {/if}
    </div>
  </header>
  <a
    class="border-b border-black px-4 py-2 hover:bg-gray-300 cursor-pointer block w-full"
    href="/requests"
    ><strong>Chat Requests:</strong> Sent {$chatRequests?.sent?.length || 0} | Received {$chatRequests
      ?.received?.length || 0}</a
  >
</div>

<style lang="postcss">
  .menu-list-item {
    @apply block text-sm text-gray-700 px-4 py-2 border-b border-gray-200 hover:bg-gray-100 cursor-pointer w-full text-left;
  }
</style>
