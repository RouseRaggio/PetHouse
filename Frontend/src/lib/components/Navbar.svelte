<script>
	import { onMount } from 'svelte';
	import 'bootstrap/dist/css/bootstrap.min.css';
	import { fly } from 'svelte/transition';
	import '../../app.css';
	export let showLogin = true;
	export let variant = "default"; 

	let scrolled = false;

	onMount(() => {
		const handleScroll = () => {
			scrolled = window.scrollY > 30;
		};

		window.addEventListener('scroll', handleScroll);
		return () => window.removeEventListener('scroll', handleScroll);
	});
</script>

<nav
	in:fly={{ y: -60, duration: 600 }}
	class="navbar navbar-expand-lg fixed-top {scrolled ? 'navbar-scrolled' : 'navbar-top'}"
	class:login-navbar={variant === "login"}
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
					<a class="nav-link nav-custom" href="/adoptar">Adoptar</a>
				</li>

				<li class="nav-item">
					<a class="nav-link nav-custom" href="/usuarios/rastreador">Rastreador</a>
				</li>

				<li class="nav-item ms-3">
					{#if showLogin}
							<a href="/login" class="nav-link nav-custom">Login</a>
					{/if}
				</li>
			</ul>
		</div>
	</div>
</nav>
