<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { fade, slide } from "svelte/transition";
  import axios from "axios";
  import { parseFastAPIError } from "$lib/util";
  import { chatRequests } from "$lib/stores/chat";
  import { goto } from "$app/navigation";

  const d = createEventDispatcher();
  export let identifier: string = "";
  let isDone = false;
  let isLoading = false;

  function addUser() {
    isDone = false;
    isLoading = true;

    if ($chatRequests?.sent) {
      if (
        $chatRequests.received.find(
          x => x.from_user.id === identifier || x.from_user.email === identifier
        )
      ) {
        // TODO: auto-accept the request instead of redirecting
        alert(
          "Looks like you have received a request from this user. You will now be redirected to the requests page to view the requests"
        );
        isDone = true;
        isLoading = false;
        goto("/requests");
        return;
      }
    }

    axios
      .post("/api/chat/requests", { identifier })
      .then(() => {
        isDone = true;
        isLoading = false;
      })
      .catch(e => {
        isLoading = false;
        if (e.response) {
          alert(parseFastAPIError(e.response.data));
        } else {
          alert("Something went wrong");
          console.error(e);
        }
      });
  }
</script>

<div
  class="fixed w-full h-full top-0 left-0 z-20 grid place-items-center"
  style="background-color: rgba(0, 0, 0, 0.6)"
  transition:fade
  on:click|self={() => {
    d("close");
  }}
>
  <div class="bg-white px-4 py-2 rounded border border-black" transition:slide>
    <h2 class="text-4xl font-bold my-4">Add user to chat</h2>
    <form on:submit|preventDefault={addUser}>
      <label for="identifier" class="block font-bold my-1">User ID or email</label>
      <input
        bind:value={identifier}
        type="text"
        class="bg-white border border-gray-500 px-3 py-2 rounded w-full"
        name="identifier"
        id="identifier"
      />
    </form>
    <p class="flex gap-2 items-center mt-4">
      <button
        type="button"
        disabled={isLoading}
        on:click={() => d("close")}
        class="bg-gray-300 rounded px-4 w-full py-2 border border-transparent"
        >{isLoading ? "..." : "Close"}</button
      >
      <button
        type="submit"
        disabled={isLoading}
        class="bg-blue-500 text-white w-full rounded px-4 py-2 border border-transparent"
        >{isLoading ? "..." : "Add user"}</button
      >
    </p>
    {#if isDone}
      <p class="mt-4 text-green-500 text-center text-lg">
        We've sent a request! Feel free to add another user or close this window.
      </p>
    {/if}
  </div>
</div>
