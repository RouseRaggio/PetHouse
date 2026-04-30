<script>
	import { createUser, loginUser, registerUser } from '../../api/user_service.js';
	import { fade, fly } from 'svelte/transition';
	import Navbar from '$lib/components/Navbar.svelte';
	import { setAuth } from '$lib/stores/auth.js';
	import { getAndClearRedirectUrl } from '$lib/utils/auth.js';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import Swal from 'sweetalert2';
	// svelte-ignore export_let_unused
		export let data;

	let isRegister = false;

	let nombre = '';
	let apellido = '';
	let email = '';
	let password = '';
	let showPassword = false;
	let authMessage = '';
	let passwordError = '';

	// Reglas de validación reactivas
	$: pwdRules = {
		length: password.length >= 8,
		upper: /[A-Z]/.test(password),
		lower: /[a-z]/.test(password),
		number: /\d/.test(password),
		special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
	};

	$: isPasswordValid = Object.values(pwdRules).every(Boolean);

	// Get message from URL if present
	$: if ($page.url.searchParams.has('message')) {
		authMessage = $page.url.searchParams.get('message');
		// Show the message in a toast or alert
		if (authMessage) {
			Swal.fire({
				title: 'Acceso requerido',
				text: authMessage,
				icon: 'info',
				toast: true,
				position: 'top-end',
				showConfirmButton: false,
				timer: 3000
			});
		}
	}

	async function handleSubmit() {
		if (isRegister) {
			// =========================
			// REGISTRO
			// =========================
			const userData = {
				role_id: 2,  // Usuario normal por defecto
				name: nombre,
				last_name: apellido,
				email: email,
				password: password
			};

			try {
				const result = await registerUser(userData);

				Swal.fire({
					title: 'Éxito',
					text: 'Usuario registrado correctamente. Ahora puedes iniciar sesión.',
					icon: 'success'
				});

				// limpiar campos
				nombre = '';
				apellido = '';
				email = '';
				password = '';

				isRegister = false;

			} catch (error) {
				passwordError = error.message;
				// Si el error es de la contraseña, no mostramos modal, solo el texto abajo
				if (!error.message.includes('contraseña') && !error.message.includes('caracter')) {
					Swal.fire({
						title: 'Error',
						text: error.message || 'Error registrando usuario',
						icon: 'error'
					});
				}
			}

		} else {
		
			try {
				const result = await loginUser(email, password);
				
				console.log('Login result:', result);

				// guardar token y usuario
			setAuth(result.access_token, result.user);
           
				Swal.fire({
					title: 'Bienvenido',
					text: `Hola ${result.user.name}`,
					icon: 'success'
				});

				// Verificar si hay una URL de redirección guardada
				const redirectUrl = getAndClearRedirectUrl();

				if (redirectUrl) {
					// Redirigir a la URL guardada
					goto(redirectUrl);
				} else {
					// Redirección por rol si no hay URL guardada
					const roleId = result.user.role_id;
					if (roleId === 1) {
						goto('/admin');
					} else {
						// Usuario normal va a la página principal
						goto('/');
					}
				}

			} catch (error) {
				Swal.fire({
					title: 'Error',
					text: error.message || 'Credenciales incorrectas',
					icon: 'error'
				});
			}
		}
	}
</script>

<Navbar />
<section class="login-wrapper" in:fade>
	<div class="login-card px-4" in:fly={{ y: 30, duration: 400, opacity: 0 }}>
		<h2>{isRegister ? 'Crear cuenta' : 'Bienvenido'}</h2>
		<p class="subtitle">
			{isRegister ? 'Regístrate para comenzar' : 'Inicia sesión para continuar'}
		</p>

		<form on:submit|preventDefault={handleSubmit}>
			{#if isRegister}
				<div class="row g-2 mb-2" in:fly={{ y: -15, duration: 500 }}>
					<div class="col-md-6 text-start">
						<label for="nombre" class="small fw-bold">Nombre</label>
						<input id="nombre" class="form-control form-control-sm" type="text" bind:value={nombre} required />
					</div>
					<div class="col-md-6 text-start">
						<label for="apellido" class="small fw-bold">Apellido</label>
						<input id="apellido" class="form-control form-control-sm" type="text" bind:value={apellido} required />
					</div>
				</div>
			{/if}

			<div class="input-group mb-2">
				<label class="small fw-bold">Correo electrónico</label>
				<input class="form-control form-control-sm" type="email" bind:value={email} placeholder="ejemplo@email.com" required />
			</div>

			<div class="input-group mb-2">
				<label class="small fw-bold">Contraseña</label>
				<div class="password-wrapper">
					<input
						class="form-control form-control-sm"
						type={showPassword ? 'text' : 'password'}
						bind:value={password}
						placeholder="••••••••"
						required
					/>
					<!-- svelte-ignore a11y_click_events_have_key_events -->
					<!-- svelte-ignore a11y_no_static_element_interactions -->
					<span class="toggle-password" on:click={() => (showPassword = !showPassword)}>
						{showPassword ? '👁' : '👁‍🗨'}
					</span>
				</div>

				{#if isRegister}
					<div class="password-guidelines mt-2 p-2 rounded-3 bg-light border-0">
						<div class="row g-1">
							<div class="col-6 {pwdRules.length ? 'text-success' : 'text-muted'} x-small">
								<i class="bi {pwdRules.length ? 'bi-check-circle-fill' : 'bi-circle'}"></i> 8+ chars
							</div>
							<div class="col-6 {pwdRules.upper && pwdRules.lower ? 'text-success' : 'text-muted'} x-small">
								<i class="bi {pwdRules.upper && pwdRules.lower ? 'bi-check-circle-fill' : 'bi-circle'}"></i> Aa
							</div>
							<div class="col-6 {pwdRules.number ? 'text-success' : 'text-muted'} x-small">
								<i class="bi {pwdRules.number ? 'bi-check-circle-fill' : 'bi-circle'}"></i> Número
							</div>
							<div class="col-6 {pwdRules.special ? 'text-success' : 'text-muted'} x-small">
								<i class="bi {pwdRules.special ? 'bi-check-circle-fill' : 'bi-circle'}"></i> Especial
							</div>
						</div>
					</div>
					
					{#if passwordError}
						<div class="error-text text-danger x-small mt-1 fw-bold">
							{passwordError}
						</div>
					{/if}
				{/if}
			</div>

			<button class="btn-login py-2 mt-3" disabled={isRegister && !isPasswordValid}>
				{isRegister ? 'Registrarse' : 'Iniciar Sesión'}
			</button>
			
		</form>

		<p class="footer-text">
			{#if !isRegister}
				¿No tienes cuenta?

				<a href="..." on:click|preventDefault={() => (isRegister = true)}> Regístrate </a>
			{:else}
				¿Ya tienes cuenta?
				<a href="..." on:click|preventDefault={() => (isRegister = false)}> Inicia sesión </a>
			{/if}
		</p>
	</div>
</section>

<style>
	.login-wrapper {
		min-height: 100vh;
		display: flex;
		justify-content: center;
		align-items: center;
		background: linear-gradient(135deg, #ecd75f, #b89a14);
	}

	.login-card {
		background: white;
		padding: 2rem 1.5rem;
		border-radius: 24px;
		width: 100%;
		max-width: 420px;
		box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
		text-align: center;
		margin: 1rem;
	}

	.login-card h2 {
		font-weight: 700;
		margin-bottom: 0.5rem;
	}

	.subtitle {
		color: #6c757d;
		margin-bottom: 1.5rem;
	}

	.input-group {
		display: flex;
		flex-direction: column;
		margin-bottom: 1.2rem;
		text-align: left;
	}

	.input-group label {
		font-size: 1rem;
		font-weight: 600;
		display: block;
		margin-bottom: 0.2rem;
	}

	.input-group input {
		width: 100%;
		padding: 0.3rem;
		border-radius: 12px;
		border: 1px solid #dfe1e2;
		transition: all 0.2s ease;
	}

	.input-group input:focus {
		border-color: #0d6efd;
		box-shadow: 0 0 0 3px rgba(13, 110, 253, 0.2);
		outline: none;
	}

	.password-wrapper {
		position: relative;
	}

	.password-wrapper input {
		padding-right: 87px; /* espacio para el icono */
	}

	.toggle-password {
		position: absolute;
		right: 6px;
		top: 50%;
		transform: translateY(-50%);
		cursor: pointer;
		font-size: 1rem;
		user-select: none;
		color: #6c757d;
		transition: 0.2s ease;
	}

	.toggle-password:hover {
		color: #b7b921;
	}

	.btn-login {
		width: 100%;
		padding: 0.8rem;
		border-radius: 12px;
		border: none;
		background: linear-gradient(135deg, #ced121, #828a1b);
		color: rgb(253, 253, 247);
		font-weight: 600;
		cursor: pointer;
		transition: all 0.25s ease;
		box-shadow: 0 8px 20px rgba(13, 110, 253, 0.3);
		margin-top: 0.5rem;
	}

	.btn-login:hover {
		transform: translateY(-3px);
		box-shadow: 0 12px 30px rgba(13, 110, 253, 0.4);
	}

	.footer-text {
		margin-top: 1.5rem;
		font-size: 0.9rem;
		color: #6c757d;
	}

	.footer-text a {
		color: #0d6efd;
		text-decoration: none;
		font-weight: 600;
	}

	.footer-text a:hover {
		text-decoration: underline;
	}

	@media (max-width: 480px) {
		.login-card {
			padding: 2rem;
		}
	}
	#admin-login {
		background: linear-gradient(135deg, #b89a14, #ecd75f);
		color: #333;
		box-shadow: 0 8px 20px rgba(184, 154, 20, 0.3);
	}

	.password-guidelines {
		text-align: left;
		background-color: #f8f9fa !important;
	}

	.x-small {
		font-size: 0.75rem;
	}

	.password-guidelines .row > div {
		display: flex;
		align-items: center;
		gap: 5px;
		transition: all 0.3s ease;
	}

	.error-text {
		text-align: left;
	}

	.btn-login:disabled {
		background: #e9ecef;
		color: #adb5bd;
		cursor: not-allowed;
		box-shadow: none;
		transform: none;
	}
</style>