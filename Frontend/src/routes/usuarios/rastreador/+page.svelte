<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { auth, setAuth } from '$lib/stores/auth.js';
	import Navbar from '$lib/components/Navbar.svelte';
	import Swal from 'sweetalert2';
	import { updateUser } from '../../../api/user_service.js';

	let currentUser = null;

	auth.subscribe((state) => {
		currentUser = state.user;
	});

	// Datos simulados (solo si tiene acceso)
	let trackers = [
		{ id: 1, name: 'Collar Fido', type: 'GPS', status: 'Activo', location: 'Barranquilla' },
		{ id: 2, name: 'Collar Mimi', type: 'GPS', status: 'Activo', location: 'Cartagena' }
	];

	onMount(async () => {
		if (!currentUser) {
			goto('/login');
		} else {
			// Hacer re-fetch del estado del usuario para ver si el admin ya le aprobó el GPS
			try {
				const res = await fetch(`http://localhost:8000/users/${currentUser.id}`, {
					headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
				});
				if (res.ok) {
					const freshUser = await res.json();
					if (freshUser.gps_status !== currentUser.gps_status) {
						currentUser.gps_status = freshUser.gps_status;
						setAuth(localStorage.getItem('token'), currentUser);
					}
				}
			} catch (err) {
				console.error("Error refreshing user state", err);
			}
		}
	});

	async function requestGPS() {
		try {
			// Solicitamos GPS actualizando el usuario
			await updateUser(currentUser.id, { gps_status: 'pending' });
			
			// Actualizamos store local para que la UI cambie inmediatamente
			currentUser.gps_status = 'pending';
			setAuth(localStorage.getItem('token'), currentUser);

			Swal.fire({
				title: 'Solicitud enviada',
				text: 'El administrador revisará tu solicitud de rastreador GPS pronto.',
				icon: 'success'
			});
		} catch (error) {
			console.error("Error pidiendo GPS:", error);
			Swal.fire('Error', 'Hubo un problema al enviar la solicitud', 'error');
		}
	}
</script>

<Navbar />

<section class="container my-5">
	{#if currentUser}
		{#if currentUser.gps_status === 'approved'}
			<!-- VISTA DEL RASTREADOR -->
			<h2 class="mb-4 text-center">Mis Rastreadores</h2>

			<div class="row g-3">
				{#each trackers as t (t.id)}
					<div class="col-12 col-md-6 col-lg-4">
						<div class="card p-3 shadow-sm">
							<h5>{t.name}</h5>
							<p><strong>Tipo:</strong> {t.type}</p>
							<p><strong>Estado:</strong> {t.status}</p>
							<p><strong>Ubicación:</strong> {t.location}</p>
						</div>
					</div>
				{/each}
			</div>

			<div class="card mt-5 p-3 shadow-sm">
				<h5>Ubicación en Mapa</h5>
				<div class="map-placeholder d-flex align-items-center justify-content-center bg-light rounded" style="height: 350px;">
					<span class="text-muted">Aquí se mostrará un mapa con la ubicación de los rastreadores</span>
				</div>
			</div>

		{:else if currentUser.gps_status === 'pending'}
			<!-- VISTA PENDIENTE -->
			<div class="row justify-content-center">
				<div class="col-md-8 text-center">
					<div class="card p-5 shadow-sm border-0">
						<div class="mb-4">
							<i class="bi bi-hourglass-split" style="font-size: 4rem; color: #ffcb1b;"></i>
						</div>
						<h3 class="mb-3">Solicitud en proceso</h3>
						<p class="text-muted lead">
							Tu solicitud de GPS ha sido enviada correctamente. Estamos esperando que el administrador la apruebe. Una vez aprobada, tendrás acceso a esta sección.
						</p>
					</div>
				</div>
			</div>

		{:else}
			<!-- VISTA NO TIENE GPS -->
			<div class="row justify-content-center">
				<div class="col-md-8 text-center">
					<div class="card p-5 shadow-sm border-0 bg-light">
						<div class="mb-4">
							<i class="bi bi-geo-alt-fill text-danger" style="font-size: 4rem;"></i>
						</div>
						<h3 class="mb-3">Adquiere un Rastreador GPS</h3>
						<p class="lead mb-4">
							Para utilizar los servicios de rastreo, primero necesitas un dispositivo GPS asignado a tu cuenta. 
							Solicítalo ahora y mantén a tu mascota siempre segura.
						</p>
						<button class="btn btn-warning btn-lg px-5 py-3 fw-bold shadow" on:click={requestGPS}>
							Solicitar GPS
						</button>
					</div>
				</div>
			</div>
		{/if}
	{:else}
		<div class="text-center py-5">
			<div class="spinner-border text-warning" role="status">
				<span class="visually-hidden">Cargando...</span>
			</div>
		</div>
	{/if}
</section>

<style>
	.btn-warning {
		background-color: #ffcb1b;
		border: none;
		transition: all 0.3s;
	}
	.btn-warning:hover {
		background-color: #e6b800;
		transform: translateY(-2px);
	}
</style>
