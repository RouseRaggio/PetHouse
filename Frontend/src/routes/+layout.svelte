<script>
	import { page } from "$app/stores";
	import Navbar from "$lib/components/Navbar.svelte";

	$: isLogin = $page.url.pathname === "/login";
</script>

{#if isLogin}
	<Navbar showLogin={false} fixed={false} />
{:else}
	<Navbar showLogin={true} fixed={true} />
{/if}

<slot />