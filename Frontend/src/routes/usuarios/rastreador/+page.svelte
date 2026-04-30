<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { auth } from '$lib/stores/auth.js';
	import { saveRedirectUrl } from '$lib/utils/auth.js';
	import { getPets, updatePet } from '../../../api/pet_service.js';
	import Navbar from '$lib/components/Navbar.svelte';
	import Swal from 'sweetalert2';

	$: currentUser = $auth?.user;
	
	let myPets = [];
	let otherPets = [];
	let selectedPet = null;
	let loading = true;

	// Cargar datos cuando el usuario esté disponible
	$: if (currentUser && loading) {
		loadData();
	}

	onMount(async () => {
		if (!currentUser) {
			// Si no hay usuario después de un tiempo, dejar de cargar
			setTimeout(() => {
				if (!currentUser) loading = false;
			}, 1000);
		}
	});

	async function loadData() {
		try {
			const allPets = await getPets();
			
			// Todas las mascotas del usuario
			const adoptedByMe = allPets.filter(p => p.adopter_id === currentUser.id);

			// Con GPS (aprobado o pendiente)
			myPets = adoptedByMe.filter(p => p.gps_status !== 'none');
			
			// Sin GPS
			otherPets = adoptedByMe.filter(p => p.gps_status === 'none');
			
			if (myPets.length > 0) {
				// Por defecto seleccionamos la primera con GPS aprobado, o la primera de la lista
				if (!selectedPet) {
					selectedPet = myPets.find(p => p.gps_status === 'approved') || myPets[0];
				} else {
					// Actualizar la mascota seleccionada con los nuevos datos
					selectedPet = myPets.find(p => p.id === selectedPet.id) || myPets[0];
				}
			}
		} catch (err) {
			console.error("Error loading trackers:", err);
		} finally {
			loading = false;
		}
	}

	function selectPet(pet) {
		console.log("Selecting pet:", pet.name);
		selectedPet = pet;
	}

	async function requestGPS(pet) {
		const result = await Swal.fire({
			title: '¿Solicitar rastreador GPS?',
			text: `Iniciaremos el proceso de preparación del dispositivo para ${pet.name}.`,
			icon: 'question',
			showCancelButton: true,
			confirmButtonText: 'Sí, solicitar',
			cancelButtonText: 'Cancelar'
		});

		if (result.isConfirmed) {
			try {
				loading = true;
				await updatePet(pet.id, { gps_status: 'pending' });
				await Swal.fire('Solicitud enviada', 'El administrador revisará tu solicitud.', 'success');
				await loadData();
			} catch (error) {
				console.error("Error requesting GPS:", error);
				Swal.fire('Error', 'No se pudo enviar la solicitud.', 'error');
			} finally {
				loading = false;
			}
		}
	}

	async function handleHeroAction() {
		if (loading) return;
		
		if (currentUser && myPets.length === 0 && otherPets.length === 0) {
			loading = true;
			await loadData();
		}

		if (otherPets.length === 1) {
			requestGPS(otherPets[0]);
		} else if (otherPets.length > 1) {
			const section = document.getElementById('otras-mascotas');
			if (section) {
				section.scrollIntoView({ behavior: 'smooth' });
			} else {
				Swal.fire({
					title: 'Selecciona una mascota',
					text: 'Tienes varias mascotas adoptadas. Elige para cuál quieres el GPS en la sección inferior.',
					icon: 'info'
				});
			}
		} else {
			if (myPets.length > 0) {
				Swal.fire('Ya tienes rastreadores', 'Puedes ver la ubicación de tus mascotas arriba.', 'info');
			} else {
				Swal.fire({
					title: 'Información',
					text: 'Para obtener un rastreador GPS, primero debes adoptar una mascota en nuestra plataforma.',
					icon: 'info',
					showCancelButton: true,
					confirmButtonText: 'Ver mascotas disponibles',
					cancelButtonText: 'Cerrar'
				}).then((result) => {
					if (result.isConfirmed) {
						goto('/usuarios/mascotas');
					}
				});
			}
		}
	}

	function redirectToLogin() {
		saveRedirectUrl('/usuarios/rastreador');
		goto('/login?message=Para ver tus rastreadores debes iniciar sesión');
	}
</script>

<Navbar />

<main class="tracker-page">
	{#if loading}
		<div class="text-center py-5">
			<div class="spinner-border text-primary" role="status"></div>
		</div>
	{:else if myPets.length > 0 && selectedPet}
		<!-- VISTA DEL RASTREADOR -->
		<section class="container py-5">
			<div class="row mb-5">
				<div class="col-lg-8">
					<h1 class="fw-bold mb-2">Mis Rastreadores GPS</h1>
					<p class="text-muted lead">Sigue la ubicación de tus mascotas en tiempo real.</p>
				</div>
				<div class="col-lg-4 text-center text-lg-end d-flex flex-wrap gap-2 justify-content-center justify-content-lg-end align-items-center mt-3 mt-lg-0">
					<button class="btn btn-outline-primary rounded-pill px-3 py-2 btn-sm" on:click={() => {
						if (otherPets.length > 0) {
							const section = document.getElementById('otras-mascotas');
							if (section) section.scrollIntoView({ behavior: 'smooth' });
						} else {
							Swal.fire({
								title: 'Información',
								text: 'Para adquirir otro rastreador GPS debes tener otra mascota adoptada sin servicio activo.',
								icon: 'info',
								showCancelButton: true,
								confirmButtonText: 'Ver catálogo de mascotas',
								cancelButtonText: 'Cerrar'
							}).then((result) => {
								if (result.isConfirmed) {
									goto('/usuarios/mascotas');
								}
							});
						}
					}}>
						<i class="bi bi-plus-circle me-1"></i> Solicitar otro
					</button>
					<div class="dropdown">
						<button class="btn btn-white shadow-sm dropdown-toggle rounded-pill px-4 py-2 border" type="button" data-bs-toggle="dropdown">
							<i class="bi bi-suit-heart-fill text-danger me-2"></i>
							{selectedPet.name}
						</button>
						<ul class="dropdown-menu shadow border-0 rounded-3">
							{#each myPets as pet}
								<li>
									<!-- svelte-ignore a11y_invalid_attribute -->
									<a class="dropdown-item {selectedPet.id === pet.id ? 'active' : ''}" 
									   href="javascript:void(0)" 
									   on:click|preventDefault={() => selectPet(pet)}>
										{pet.name} ({pet.gps_status === 'approved' ? 'Activo' : 'Pendiente'})
									</a>
								</li>
							{/each}
						</ul>
					</div>
				</div>
			</div>

			{#key selectedPet.id}
				{#if selectedPet.gps_status === 'approved'}
					<div class="row mb-4">
						<div class="col-12 text-center text-lg-end mb-3">
							<div class="p-3 bg-white shadow-sm rounded-4 border-start border-4 border-success d-inline-block text-start w-100 w-lg-auto">
								<small class="text-muted d-block text-uppercase fw-bold">IMEI de {selectedPet.name}:</small>
								<span class="fs-5 fw-bold text-dark">{selectedPet.gps_imei || 'Cargando...'}</span>
							</div>
						</div>
					</div>

					<div class="card border-0 shadow-lg overflow-hidden rounded-4 mb-5">
						<div class="card-header bg-dark text-white p-4 d-flex justify-content-between align-items-center">
							<div class="d-flex align-items-center">
								<i class="bi bi-map-fill text-warning me-3 fs-3"></i>
								<div>
									<h5 class="mb-0 fw-bold">Plataforma: {selectedPet.name}</h5>
									<small class="opacity-75">Ingresa el IMEI en el panel para ver la ubicación</small>
								</div>
							</div>
							<a href="https://www.365gps.net/" target="_blank" class="btn btn-outline-light btn-sm rounded-pill px-3">
								<i class="bi bi-box-arrow-up-right me-1"></i> Abrir en nueva pestaña
							</a>
						</div>
						<div class="map-container position-relative">
							<iframe
								src="https://www.365gps.net/platform/#/"
								title="Mapa GPS"
								width="100%"
								height="100%"
								style="border:0;"
								loading="lazy"
							>
							</iframe>
						</div>
					</div>
				{:else}
					<div class="card p-5 shadow-lg border-0 bg-white rounded-4 text-center">
						<div class="mb-4">
							<div class="status-icon-pending">
								<i class="bi bi-hourglass-split"></i>
							</div>
						</div>
						<h2 class="fw-bold mb-3">Solicitud de {selectedPet.name} en Proceso</h2>
						<p class="text-muted lead mb-4">
							Estamos preparando el dispositivo GPS para {selectedPet.name}. 
							Recibirás un correo cuando esté listo para retirar.
						</p>
						<div class="alert alert-warning border-0 bg-warning-subtle d-inline-block px-4">
							<i class="bi bi-info-circle-fill me-2"></i> Estado: Pendiente de aprobación
						</div>
					</div>
				{/if}

				<div class="row g-4 mt-2 mb-5">
					<div class="col-md-4">
						<div class="card p-4 border-0 shadow-sm h-100 rounded-4">
							<div class="icon-box bg-primary-subtle text-primary mb-3">
								<i class="bi bi-info-circle fs-4"></i>
							</div>
							<h5 class="fw-bold">¿Cómo usar?</h5>
							<p class="text-muted small">Copia el IMEI de {selectedPet.name} e ingrésalo en la plataforma para iniciar el rastreo.</p>
						</div>
					</div>
					<div class="col-md-4">
						<div class="card p-4 border-0 shadow-sm h-100 rounded-4">
							<div class="icon-box bg-success-subtle text-success mb-3">
								<i class="bi bi-shield-check fs-4"></i>
							</div>
							<h5 class="fw-bold">Zonas Seguras</h5>
							<p class="text-muted small">Configura geo-cercas para {selectedPet.name} directamente en la plataforma.</p>
						</div>
					</div>
					<div class="col-md-4">
						<div class="card p-4 border-0 shadow-sm h-100 rounded-4">
							<div class="icon-box bg-warning-subtle text-warning mb-3">
								<i class="bi bi-headset fs-4"></i>
							</div>
							<h5 class="fw-bold">Soporte</h5>
							<p class="text-muted small">Contáctanos a soporte@pethouse.com indicando el nombre de tu mascota.</p>
						</div>
					</div>
				</div>
			{/key}

			{#if otherPets.length > 0}
				<div id="otras-mascotas" class="mt-5 pt-4 border-top">
					<h3 class="fw-bold mb-4">Solicitar GPS para tus otras mascotas</h3>
					<div class="row g-4">
						{#each otherPets as pet}
							<div class="col-md-6 col-lg-4">
								<div class="card p-4 border-0 shadow-sm rounded-4 d-flex flex-row align-items-center">
									<div class="flex-grow-1">
										<h5 class="fw-bold mb-1">{pet.name}</h5>
										<p class="text-muted small mb-0">Sin rastreador activo</p>
									</div>
									<button class="btn btn-outline-primary btn-sm rounded-pill" on:click={() => requestGPS(pet)}>
										Solicitar GPS
									</button>
								</div>
							</div>
						{/each}
					</div>
				</div>
			{/if}
		</section>
	{:else}
		<!-- VISTA LANDING -->
		<div class="hero-section">
			<div class="container py-5">
				<div class="row align-items-center">
					<div class="col-lg-6">
						<span class="badge bg-warning text-dark mb-3 px-3 py-2 rounded-pill fw-bold">
							NUEVO SERVICIO
						</span>
						<h1 class="display-4 fw-bold mb-4">La seguridad de tu mascota <span class="text-primary">en tus manos</span></h1>
						<p class="lead text-muted mb-5">
							Con nuestro sistema de rastreo GPS premium, nunca perderás de vista a tu mejor amigo. 
							Localización en tiempo real, zonas seguras y alertas instantáneas.
						</p>
						
						{#if currentUser}
							<div class="d-flex flex-column gap-3">
								<div class="d-flex gap-3">
									<button on:click={handleHeroAction} class="btn btn-warning btn-lg px-5 py-3 fw-bold shadow-lg">
										Solicitar GPS
									</button>
								</div>
								
								{#if otherPets.length > 1}
									<p class="text-muted small mt-2">
										<i class="bi bi-info-circle me-1"></i> Tienes {otherPets.length} mascotas listas para recibir su rastreador.
									</p>
								{/if}
							</div>
						{:else}
							<div class="d-flex gap-3">
								<button on:click={redirectToLogin} class="btn btn-primary btn-lg px-5 py-3 fw-bold shadow-lg">
									Iniciar Sesión para Empezar
								</button>
							</div>
						{/if}
					</div>
					<div class="col-lg-6 d-none d-lg-block">
						<div class="position-relative">
							<div class="blob-bg"></div>
							<img src="https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80" 
								 alt="Perro con collar GPS" class="img-fluid rounded-4 shadow-2xl position-relative z-1">
							<div class="floating-card p-3 bg-white shadow rounded-3 position-absolute bottom-0 start-0 m-4 z-2">
								<div class="d-flex align-items-center">
									<div class="bg-success rounded-circle p-1 me-2"></div>
									<span class="small fw-bold">Ubicación Actual: Barranquilla, COL</span>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>

		<section id="beneficios" class="container py-5 mt-5">
			<div class="text-center mb-5">
				<h2 class="fw-bold">¿Por qué elegir nuestro GPS?</h2>
				<p class="text-muted mx-auto" style="max-width: 600px;">
					Diseñado especialmente para mascotas activas y dueños que valoran la tranquilidad.
				</p>
			</div>

			<div class="row g-4">
				<div class="col-md-4">
					<div class="benefit-card p-4 h-100 text-center">
						<div class="icon-circle mb-4 bg-primary-subtle text-primary mx-auto">
							<i class="bi bi-geo-alt-fill"></i>
						</div>
						<h4 class="fw-bold">Rastreo Preciso</h4>
						<p class="text-muted">Utilizamos tecnología satelital de última generación para darte la ubicación exacta en todo momento.</p>
					</div>
				</div>
				<div class="col-md-4">
					<div class="benefit-card p-4 h-100 text-center">
						<div class="icon-circle mb-4 bg-danger-subtle text-danger mx-auto">
							<i class="bi bi-shield-check"></i>
						</div>
						<h4 class="fw-bold">Geo-Vallas</h4>
						<p class="text-muted">Configura zonas seguras y recibe notificaciones inmediatas en tu celular si tu mascota sale de ellas.</p>
					</div>
				</div>
				<div class="col-md-4">
					<div class="benefit-card p-4 h-100 text-center">
						<div class="icon-circle mb-4 bg-success-subtle text-success mx-auto">
							<i class="bi bi-battery-charging"></i>
						</div>
						<h4 class="fw-bold">Batería de Larga Duración</h4>
						<p class="text-muted">Nuestros dispositivos están optimizados para durar hasta 7 días con una sola carga.</p>
					</div>
				</div>
			</div>
		</section>

		<section class="bg-dark text-white py-5 mt-5">
			<div class="container">
				<div class="row align-items-center">
					<div class="col-lg-8">
						<h2 class="fw-bold mb-3">¿Listo para proteger a tu mascota?</h2>
						<p class="lead mb-0 opacity-75">Únete a cientos de dueños que ya confían en PetHouse para la seguridad de sus peludos.</p>
					</div>
					<div class="col-lg-4 text-lg-end mt-4 mt-lg-0">
						<a href="/usuarios/mascotas" class="btn btn-warning btn-lg px-5 py-3 fw-bold">
							Solicitar GPS
						</a>
					</div>
				</div>
			</div>
		</section>
	{/if}
</main>

<style>
	:global(body) {
		background-color: #f8f9fa;
	}

	.tracker-page {
		min-height: 80vh;
	}

	.map-container {
		height: 600px;
	}

	@media (max-width: 768px) {
		.map-container {
			height: 400px;
		}
		
		h1.display-4 {
			font-size: 2.5rem;
		}

		.hero-section {
			padding: 40px 0;
			text-align: center;
		}

		.hero-section .d-flex {
			justify-content: center;
		}
	}

	.icon-box {
		width: 50px;
		height: 50px;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 12px;
	}

	.status-icon-pending {
		width: 100px;
		height: 100px;
		background: #fff8e1;
		color: #ffcb1b;
		font-size: 3rem;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 50%;
		margin: 0 auto;
		animation: pulse 2s infinite;
	}

	@keyframes pulse {
		0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 203, 27, 0.4); }
		70% { transform: scale(1.05); box-shadow: 0 0 0 20px rgba(255, 203, 27, 0); }
		100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 203, 27, 0); }
	}

	.hero-section {
		background: linear-gradient(135deg, #fff 0%, #f0f4f8 100%);
		padding: 60px 0;
		overflow: hidden;
	}

	.blob-bg {
		position: absolute;
		width: 500px;
		height: 500px;
		background: #ffcb1b;
		filter: blur(80px);
		opacity: 0.15;
		border-radius: 50%;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		z-index: 0;
	}

	.benefit-card {
		background: white;
		border-radius: 20px;
		border: 1px solid rgba(0,0,0,0.05);
		transition: all 0.3s ease;
	}
	.benefit-card:hover {
		box-shadow: 0 15px 30px rgba(0,0,0,0.08);
	}

	.icon-circle {
		width: 70px;
		height: 70px;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 50%;
		font-size: 1.8rem;
	}

	.shadow-2xl {
		box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
	}

	.btn-warning {
		background-color: #ffcb1b;
		border-color: #ffcb1b;
		color: #000;
	}
	.btn-warning:hover {
		background-color: #e6b800;
		border-color: #e6b800;
	}

	.text-primary {
		color: #4361ee !important;
	}
	.bg-primary-subtle {
		background-color: #eef1ff;
	}
</style>
