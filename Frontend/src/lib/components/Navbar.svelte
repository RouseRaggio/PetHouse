<script>
	import { onMount } from 'svelte';
	import { fly } from 'svelte/transition';
	import { goto } from '$app/navigation';
	import { auth, clearAuth } from '$lib/stores/auth.js';
	import Swal from 'sweetalert2';
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

	async function logout() {
		const result = await Swal.fire({
			title: '¿Cerrar sesión?',
			text: '¿Estás seguro de que deseas salir de tu cuenta?',
			icon: 'question',
			showCancelButton: true,
			confirmButtonColor: '#ffcb1b',
			cancelButtonColor: '#dc3545',
			confirmButtonText: 'Sí, cerrar sesión',
			cancelButtonText: 'Cancelar',
			background: '#ffffff',
			customClass: {
				confirmButton: 'btn btn-warning rounded-pill px-4',
				cancelButton: 'btn btn-outline-danger rounded-pill px-4'
			},
			buttonsStyling: false
		});

		if (result.isConfirmed) {
			// Efecto de despedida suave
			await Swal.fire({
				title: '¡Hasta pronto!',
				text: 'Cerrando tu sesión de forma segura...',
				timer: 1200,
				timerProgressBar: true,
				showConfirmButton: false,
				didOpen: () => {
					Swal.showLoading();
				}
			});

			clearAuth();
			goto('/');
		}
	}
</script>

<nav
	in:fly={{ y: -60, duration: 600 }}
	class="navbar navbar-expand-lg {scrolled ? 'navbar-scrolled' : 'navbar-top'}"
	class:login-navbar={variant === 'login'}
>
	<div class="container-fluid px-lg-6">
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

		<div class="collapse navbar-collapse" id="navbarNav">
			<ul class="navbar-nav ms-auto align-items-center me-0">
				<li class="nav-item">
					<a class="nav-link nav-custom px-3" href="/">Inicio</a>
				</li>

				<li class="nav-item">
					<a class="nav-link nav-custom px-3" href="/usuarios/mascotas">Mascotas</a>
				</li>

				<li class="nav-item">
					<a class="nav-link nav-custom px-3" href="/usuarios/publicar">Publicar</a>
				</li>

				<li class="nav-item">
					<a class="nav-link nav-custom px-3" href="/usuarios/rastreador">Rastreador</a>
				</li>

				<li class="nav-item user-menu-item ms-lg-3 mt-3 mt-lg-0 pe-0">
					{#if user}
						<div class="dropdown">
							<button 
								class="btn profile-trigger d-flex align-items-center gap-2" 
								type="button" 
								data-bs-toggle="dropdown" 
								aria-expanded="false"
							>
								<div class="avatar-circle">
									{user.name.charAt(0).toUpperCase()}
								</div>
								<span class="user-name-label d-none d-xl-inline text-white">{user.name}</span>
								<i class="bi bi-chevron-down small text-white opacity-50"></i>
							</button>

							<ul class="dropdown-menu dropdown-menu-end shadow-lg border-0 rounded-4 p-2 mt-2">
								<li class="px-3 py-2 border-bottom mb-2">
									<div class="fw-bold text-dark">{user.name} {user.last_name || ''}</div>
									<div class="text-muted small">{user.email}</div>
								</li>
								
								{#if user.role_id === 1}
									<li>
										<a class="dropdown-item rounded-3 py-2" href="/admin">
											<i class="bi bi-speedometer2 me-2"></i> Panel Admin
										</a>
									</li>
								{/if}
								
								<li>
									<button class="dropdown-item rounded-3 py-2 text-danger" on:click={logout}>
										<i class="bi bi-box-arrow-right me-2"></i> Cerrar Sesión
									</button>
								</li>
							</ul>
						</div>
					{:else if showLogin}
						<a href="/login" class="btn btn-login-pill px-4">
							<i class="bi me-1"></i> Iniciar Sesión
						</a>
					{/if}
				</li>
			</ul>
		</div>
	</div>
</nav>
<style>
	/* ... existing styles if any ... */
	.avatar-circle {
		width: 38px;
		height: 38px;
		background: linear-gradient(135deg, #ffcb1b 0%, #ff9800 100%);
		color: #000;
		font-weight: bold;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 0.95rem;
		border: 2px solid rgba(255,255,255,0.3);
		transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
		box-shadow: 0 0 0 0 rgba(255, 203, 27, 0);
	}

	.profile-trigger {
		background: rgba(255,255,255,0.08);
		border: 1px solid rgba(255,255,255,0.15);
		padding: 4px 14px 4px 4px;
		border-radius: 50px;
		transition: all 0.3s ease;
		position: relative;
		overflow: hidden;
	}
	.profile-trigger:hover {
		background: rgba(255,255,255,0.2);
		border-color: rgba(255,255,255,0.4);
		transform: translateY(-1px);
	}
	.profile-trigger:hover .avatar-circle {
		transform: rotate(10deg) scale(1.1);
		box-shadow: 0 0 15px rgba(255, 203, 27, 0.4);
	}

	.dropdown-menu {
		animation: fadeInUp 0.3s ease-out forwards;
		transform-origin: top right;
	}

	@keyframes fadeInUp {
		from {
			opacity: 0;
			transform: translateY(10px) scale(0.95);
		}
		to {
			opacity: 1;
			transform: translateY(0) scale(1);
		}
	}

	.dropdown-item {
		transition: all 0.2s ease;
		font-size: 0.95rem;
		padding: 0.6rem 1rem;
	}
	.dropdown-item:hover {
		background-color: #f0f4f8;
		transform: translateX(8px);
		color: #0d6efd;
	}
	.dropdown-item.text-danger:hover {
		background-color: #fff5f5;
		color: #dc3545 !important;
	}

	.btn-login-pill {
		background-color: #ffcb1b;
		color: #000;
		font-weight: bold;
		border-radius: 50px;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		border: none;
		position: relative;
		z-index: 1;
	}
	.btn-login-pill::before {
		content: '';
		position: absolute;
		top: 0; left: 0; right: 0; bottom: 0;
		background: rgba(255,255,255,0.2);
		border-radius: 50px;
		transform: scaleX(0);
		transform-origin: right;
		transition: transform 0.3s ease;
		z-index: -1;
	}
	.btn-login-pill:hover {
		transform: translateY(-3px) scale(1.05);
		box-shadow: 0 10px 20px rgba(255, 203, 27, 0.3);
	}
	.btn-login-pill:hover::before {
		transform: scaleX(1);
		transform-origin: left;
	}

	@media (max-width: 991.98px) {
		.user-menu-item {
			border-top: 1px solid rgba(255,255,255,0.1);
			padding-top: 1.5rem;
			margin-top: 1rem;
		}
		.profile-trigger {
			width: 100%;
			justify-content: center;
			padding: 8px;
		}
	}
</style>
