<!--
  Totally not copy-pasted from my website by the way :) (https://arnu515.gq)
-->
<script lang="ts">
  interface Item {
    tooltip: string;
    href: string;
    className?: string;
    icon: string;
    onClick?: () => void;
  }

  export let items: Item[] = [];
</script>

<nav
  class="fixed top-0 left-0 h-screen w-16 m-0 p-0 flex flex-col bg-gray-200 shadow-lg"
>
  {#each items as item}
    <a
      class={"relative flex items-center justify-center h-12 w-12 m-2 bg-gray-300 dark:bg-[#212121] dark:text-white hover:bg-blue-600 hover:text-white rounded-3xl hover:rounded-xl cursor-pointer !transition-all !duration-500 group " +
        (item.className || "")}
      href={item.href}
      role={item.href ? "link" : "button"}
      on:click={e => {
        if (item.onClick) {
          e.preventDefault();
          item.onClick();
        }
      }}
    >
      {@html item.icon}
      <span
        class="absolute w-auto p-2 m-2 min-w-max left-14 rounded-md shadow-md bg-blue-600 text-white text-xs font-bold transition-all duration-100 scale-0 origin-left group-hover:scale-100"
      >
        {item.tooltip}
      </span>
    </a>
  {/each}
</nav>
