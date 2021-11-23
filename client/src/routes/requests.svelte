<script lang="ts">
  import axios from "axios";
  import { chatRequests } from "$lib/stores/chat";
  import AddUserModal from "$lib/components/AddUserModal.svelte";

  let isAddModalVisible = false;
  let loading = false;

  function chatRequest(action: "accept" | "decline", id: string) {
    loading = true;

    // confirm action
    if (window.confirm(`Are you sure you want to ${action} this chat request?`)) {
      // send to server
      axios
        .patch(`/api/chat/requests`, { id, action })
        .then(() => {
          // refetch
          chatRequests.refetch();
        })
        .catch(e => {
          loading = false;
          if (e.response) {
            alert(e.response.data);
          } else {
            alert("An unknown error occured.");
            console.error(e);
          }
        });
    } else {
      loading = false;
    }
  }
</script>

<div class="m-4">
  <h1 class="text-5xl font-bold my-4">Chat requests</h1>

  <h3 class="text-3xl font-bold my-4">Requests you've received</h3>
  {#if $chatRequests?.received?.length}
    <ul class="flex flex-col list-none m-4">
      {#each $chatRequests.received as request}
        <li
          class="border-b border-gray-400 px-4 py-2 flex justify-between items-center"
        >
          <div class="flex gap-4 items-center">
            <img
              src={request.from_user.profile.avatar}
              alt="{request.from_user.profile.name}'s avatar"
              class="rounded-full w-8 h-8"
            />
            <p class="text-xl font-bold">{request.from_user.profile.name}</p>
            <a href="mailto:{request.from_user.email}"
              ><small class="text-sm font-gray-500 text-light"
                >&lt;{request.from_user.email}&gt;</small
              ></a
            >
          </div>
          <div class="flex gap-4 items-center">
            <button
              on:click={() => chatRequest("accept", request.id)}
              aria-label="Accept"
              title="Accept"
              class="rounded-full p-2 text-green-500 bg-gray-200 hover:bg-green-100 transition-colors duration-500"
              disabled={loading}
            >
              {#if loading}
                <svg
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
                    d="M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z"
                  />
                </svg>
              {:else}
                <svg
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
                    d="M5 13l4 4L19 7"
                  />
                </svg>{/if}</button
            >
            <button
              on:click={() => chatRequest("decline", request.id)}
              aria-label="Decline"
              title="Decline"
              class="rounded-full p-2 text-red-500 bg-gray-200 hover:bg-red-100 transition-colors duration-500"
              disabled={loading}
            >
              {#if loading}
                <svg
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
                    d="M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z"
                  />
                </svg>
              {:else}
                <svg
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
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>{/if}</button
            >
          </div>
        </li>
      {/each}
    </ul>
  {:else}
    <p class="text-lg my-2">
      You haven't received any requests yet. Be sure to give your friends your email
      address so they can find you!
    </p>
  {/if}

  <h3 class="text-3xl font-bold my-4">Requests you've sent</h3>
  {#if $chatRequests?.sent?.length}
    <ul class="flex flex-col list-none m-4">
      {#each $chatRequests.sent as request}
        <li
          class="border-b border-gray-400 px-4 py-2 flex justify-between items-center"
        >
          <div class="flex gap-4 items-center">
            <img
              src={request.from_user.profile.avatar}
              alt="{request.from_user.profile.name}'s avatar"
              class="rounded-full w-8 h-8"
            />
            <p class="text-xl font-bold">{request.from_user.profile.name}</p>
            <a href="mailto:{request.from_user.email}"
              ><small class="text-sm font-gray-500 text-light"
                >&lt;{request.from_user.email}&gt;</small
              ></a
            >
          </div>
        </li>
      {/each}
    </ul>
  {:else}
    <p class="text-lg my-2">
      You haven't sent any requests yet! Send a request by <button
        class="text-blue-500 cursor-pointer hover:underline"
        on:click={() => (isAddModalVisible = true)}>clicking here</button
      >
    </p>
  {/if}
</div>

{#if isAddModalVisible}
  <AddUserModal on:close={() => (isAddModalVisible = false)} />
{/if}
