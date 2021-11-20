<script lang="ts">
  import axios from "axios";
  import joi from "joi";

  let authForm: HTMLFormElement;
  async function auth(action: "login" | "register") {
    if (!authForm) return;

    let formData = new FormData(authForm);
    // convert formData to object
    let values = {};
    formData.forEach((value, key) => {
      values[key] = value;
    });

    const { error } = joi
      .object()
      .keys({
        email: joi.string().email({ tlds: false }).required(),
        password: joi.string().required()
      })
      .validate(values);

    if (error) return alert(error.message);

    try {
      if (action === "login") {
        await axios.post("/api/auth/login", values);
      } else {
        await axios.post("/api/auth/register", values);
      }
      window.location.href = "/";
    } catch (e) {
      if (e.isAxiosError) {
        alert(e.response.data.message);
      } else {
        alert(e.message);
      }
    }
  }
</script>

<main class="min-h-screen grid place-items-center bg-gray-200">
  <section class="border border-gray-500 rounded px-6 py-4 bg-white">
    <h1 class="text-center text-5xl font-bold">Authenticate</h1>
    <h3 class="text-center text-xl mt-4">Use Password</h3>
    <form bind:this={authForm} class="auth-form">
      <label for="email">Email</label>
      <input type="email" name="email" id="email" />
      <label for="password">Password</label>
      <input type="password" name="password" id="password" />
      <p class="btns">
        <button type="button" on:click={() => auth("register")}>Register</button>
        <button type="button" on:click={() => auth("login")}>Login</button>
      </p>
    </form>
    <hr class="border-t border-gray-300 my-4" />
    <h3 class="text-center text-xl">Use OAuth</h3>
    <div class="my-4 flex flex-col items-center">
      <a
        href="{axios.defaults.baseURL}/api/auth/github"
        class="auth-button bg-[#181717] text-white">Login with Github</a
      >
    </div>
  </section>
</main>

<style lang="postcss">
  .auth-button {
    @apply text-center border border-transparent w-full font-bold py-2 px-4 rounded hover:brightness-110 transition-all duration-500;
  }
  .auth-form {
    @apply my-4;
  }
  .auth-form label {
    @apply font-bold block mt-2;
  }
  .auth-form input {
    @apply border border-gray-500 px-2 py-1 rounded w-full outline-none;
  }
  .auth-form .btns {
    @apply flex gap-2 mt-2;
  }
  .auth-form .btns button {
    @apply bg-blue-500 text-white hover:bg-blue-600 transition-colors duration-500 cursor-pointer border border-transparent px-2 py-1 rounded w-full;
  }
</style>
