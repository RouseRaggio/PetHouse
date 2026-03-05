<script>
	import { page } from '$app/stores';
	import Navbar from '$lib/components/Navbar.svelte';

	$: path = $page.url.pathname;

	$: isLogin = path === '/login';
	$: isAdmin = path.startsWith('/admin');
</script>

{#if !isAdmin}
	<Navbar showLogin={!isLogin} />
{/if}

<slot />
