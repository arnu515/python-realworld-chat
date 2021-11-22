<script lang="ts">
  import { user } from "$lib/stores/user";
  import { parseFastAPIError } from "$lib/util";
  import axios from "axios";

  let form: HTMLFormElement;
  let saving = false;

  async function save() {
    // get formdata of the form
    let formData = new FormData(form);

    // convert formdata to object
    let values = {};
    formData.forEach((value, key) => {
      values[key] = value;
    });

    // send to server
    saving = true;
    axios
      .patch("/api/settings/account", values)
      .then(() => {
        window.location.reload();
      })
      .catch(err => {
        console.error(err);
        alert(parseFastAPIError(err));
        saving = false;
      });
  }
</script>

<div class="my-6 mx-4 flex items-center justify-between">
  <h1 class="text-5xl font-bold">Account</h1>
  <button class="save-button" disabled={saving} on:click={save}
    >{saving ? "..." : "Save"}</button
  >
</div>

<form class="settings-form" on:submit|preventDefault={save} bind:this={form}>
  <div class="fg">
    <label for="email">Email</label>
    <input
      type="email"
      id="email"
      name="email"
      placeholder="Enter your email"
      value={$user.email}
    />
  </div>
  {#if $user.provider === "password"}
    <div class="fg">
      <label for="password">Password</label>
      <input
        type="password"
        id="password"
        name="password"
        placeholder="Enter a strong password"
      />
    </div>
    <div class="fg">
      <label for="cpassword">Confirm Password</label>
      <input
        type="password"
        id="cpassword"
        name="cpassword"
        placeholder="Re-Enter that password"
      />
    </div>
  {:else}
    <p class="fg">You've signed in with "{$user.provider}".</p>
  {/if}
  <div class="fg">
    <button disabled={saving} class="save-button w-full"
      >{saving ? "..." : "Save"}</button
    >
    <p class="mt-4 text-sm text-gray-500 text-center uppercase">
      You'll be logged out!
    </p>
  </div>
</form>
