<script>
	import { on } from 'svelte/events';
	import { fade, fly } from 'svelte/transition';
	// svelte-ignore export_let_unused
	export let data;

	let isRegister = false;

	let nombre = '';
	let apellido = '';
	let email = '';
	let password = '';
	let showPassword = false;

	function handleSubmit() {
		if (isRegister) {
			console.log('Intentando registro:', { nombre, apellido, email, password });
		} else {
			console.log('Intentando login:', { email, password });
		}
	}
</script>

<section class="login-wrapper" in:fade>
	<div class="login-card px-4" in:fly={{ y: 30, duration: 400, opacity: 0 }}>
		<h2>{isRegister ? 'Crear cuenta' : 'Bienvenido'}</h2>
		<p class="subtitle">
			{isRegister ? 'Regístrate para comenzar' : 'Inicia sesión para continuar'}
		</p>

		<form on:submit|preventDefault={handleSubmit}>
			{#if isRegister}
				<div class="input-group" in:fly={{ y: -15, duration: 500 }}>
					<label for="nombre">Nombre</label>
					<input id="nombre" type="text" bind:value={nombre} required />
				</div>

				<div class="input-group" in:fly={{ y: -15, duration: 500 }}>
					<label for="apellido">Apellido</label>
					<input id="apellido" type="text" bind:value={apellido} required />
				</div>
			{/if}

			<div class="input-group">
				<!-- svelte-ignore a11y_label_has_associated_control -->
				<label>Correo electrónico</label>
				<input type="email" bind:value={email} placeholder="ejemplo@email.com" required />
			</div>

			<div class="input-group">
				<!-- svelte-ignore a11y_label_has_associated_control -->
				<label>Contraseña</label>

				<div class="password-wrapper">
					<input
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
			</div>

			<button class="btn-login">
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
		min-height: 85vh;
		display: flex;
		justify-content: center;
		align-items: center;
		background: linear-gradient(135deg, #ecd75f, #b89a14);
		padding: 1rem;
	}

	.login-card {
		background: white;
		padding-top: 2rem;
		padding-bottom: 1rem;
		border-radius: 20px;
		width: 100%;
		max-width: 500px;
		box-shadow: 0 30px 60px rgba(0, 0, 0, 0.25);
		text-align: center;
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
		margin-bottom: 2.5rem;
		margin-bottom: 1.2rem;
		text-align: left;
	}

	.input-group label {
		font-size: 1rem;
		font-weight: 600;
		display: block;
		margin-bottom: 0rem;
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
</style>
