<script>
	import { onMount } from 'svelte';
	import { fly } from 'svelte/transition';
	import { goto } from '$app/navigation';
	import { auth, clearAuth } from '$lib/stores/auth.js';
	export let showLogin = true;
	export let variant = 'default';

	let scrolled = false;
	let user = null;

	$: user = $auth?.user;

	onMount(() => {
		const handleScroll = () => {
			scrolled = window.scrollY > 30;
		};

		window.addEventListener('scroll', handleScroll);
		return () => window.removeEventListener('scroll', handleScroll);
	});

	function logout() {
		clearAuth();
		goto('/');
	}
</script>

<nav
	in:fly={{ y: -60, duration: 600 }}
	class="navbar navbar-expand-lg {scrolled ? 'navbar-scrolled' : 'navbar-top'}"
	class:login-navbar={variant === 'login'}
>
	<div class="container">
		<a class="navbar-brand brand-logo" href="/"> PetHouse </a>

		<!-- svelte-ignore a11y_consider_explicit_label -->
		<button
			class="navbar-toggler"
			type="button"
			data-bs-toggle="collapse"
			data-bs-target="#navbarNav"
		>
			<span class="navbar-toggler-icon"></span>
		</button>

		<div class="collapse navbar-collapse justify-content-end" id="navbarNav">
			<ul class="navbar-nav align-items-center">
				<li class="nav-item">
					<a class="nav-link nav-custom" href="/">Inicio</a>
				</li>

				<li class="nav-item">
					<a class="nav-link nav-custom" href="/usuarios/mascotas">Mascotas</a>
				</li>

				<li class="nav-item">
					<a class="nav-link nav-custom" href="/usuarios/publicar">Publicar</a>
				</li>

				<li class="nav-item">
					<a class="nav-link nav-custom" href="/usuarios/rastreador">Rastreador</a>
				</li>

				<li class="nav-item ms-3">
					{#if user}
					<div class="d-flex align-items-center gap-2">
						<span class="text-white">Hola, {user.name}</span>
					{#if user.role_id === 1}
							<a class="btn btn-outline-primary btn-sm" href="/admin">Panel Admin</a>
						{/if}
						<button class="btn btn-outline-danger btn-sm" on:click={logout}>Cerrar Sesión</button>
						</div>
					{:else if showLogin}
						<a href="/login" class="nav-link nav-custom">Login</a>
					{/if}
				</li>
			</ul>
		</div>
	</div>
</nav>
