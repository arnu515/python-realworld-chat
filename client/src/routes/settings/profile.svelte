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
      .patch("/api/settings/profile", values)
      .then(({ data }) => {
        const u = { ...$user };
        u.profile = data.profile;
        user.set(u);
        saving = false;
      })
      .catch(err => {
        console.error(err);
        alert(parseFastAPIError(err));
        saving = false;
      });
  }
</script>

<div class="my-6 mx-4 flex items-center justify-between">
  <h1 class="text-5xl font-bold">Profile</h1>
  <button class="save-button" disabled={saving} on:click={save}
    >{saving ? "..." : "Save"}</button
  >
</div>

<form class="settings-form" on:submit|preventDefault={save} bind:this={form}>
  <div class="fg">
    <label for="name">Full name</label>
    <input
      type="text"
      id="name"
      name="name"
      placeholder="Enter your name"
      value={$user.profile.name}
    />
  </div>
  <div class="fg">
    <label for="avatar">Avatar URL</label>
    <input
      type="text"
      id="avatar"
      name="avatar"
      placeholder="Imgur or Gravatar only!"
      value={$user.profile.avatar}
    />
  </div>
  <div class="fg">
    <label for="website">Website (Optional)</label>
    <input
      type="text"
      id="website"
      name="website"
      placeholder="Enter your website's URL"
      value={$user.profile.website}
    />
  </div>
  <div class="fg">
    <label for="bio">About you (Optional)</label>
    <textarea
      rows={5}
      id="bio"
      name="bio"
      placeholder="Enter something about you"
      value={$user.profile.bio}
    />
  </div>
  <div class="fg">
    <button disabled={saving} class="save-button w-full"
      >{saving ? "..." : "Save"}</button
    >
  </div>
</form>
