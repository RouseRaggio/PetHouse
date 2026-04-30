<script>
	import AdminNavbar from '$lib/components/AdminNavbar.svelte';
	import { onMount } from 'svelte';
	import { getUsers, updateUser } from '../../../api/user_service.js';
	import Swal from 'sweetalert2';

	let pendingRequests = [];
	let loading = true;

	// Datos del rastreador (pueden venir luego de su base de datos)
	let trackers = [
		{
			id: 1,
			name: 'Collar Fido',
			type: 'GPS',
			status: 'Activo',
			location: 'Barranquilla'
		}
	];

	// URL del panel del GPS ya logueado
	let gpsUrl = 'https://www.365gps.net/platform/#/';

	onMount(async () => {
		await loadRequests();
	});

	async function loadRequests() {
		try {
			const res = await getUsers();
			const users = res.data ?? res;
			pendingRequests = users.filter(u => u.gps_status === 'pending');
		} catch (error) {
			console.error('Error loading users:', error);
		} finally {
			loading = false;
		}
	}

	async function approveRequest(userId, userName) {
		const result = await Swal.fire({
			title: '¿Aprobar solicitud?',
			text: `Vas a asignar acceso GPS a ${userName}.`,
			icon: 'question',
			showCancelButton: true,
			confirmButtonText: 'Sí, aprobar',
			cancelButtonText: 'Cancelar'
		});

		if (result.isConfirmed) {
			try {
				await updateUser(userId, { gps_status: 'approved' });
				Swal.fire('¡Aprobado!', 'El usuario ahora tiene acceso al rastreador GPS.', 'success');
				await loadRequests();
			} catch (error) {
				console.error("Error approving request:", error);
				Swal.fire('Error', 'No se pudo aprobar la solicitud.', 'error');
			}
		}
	}

	async function rejectRequest(userId, userName) {
		const result = await Swal.fire({
			title: '¿Rechazar solicitud?',
			text: `Vas a rechazar la solicitud de GPS de ${userName}.`,
			icon: 'warning',
			showCancelButton: true,
			confirmButtonText: 'Sí, rechazar',
			cancelButtonText: 'Cancelar'
		});

		if (result.isConfirmed) {
			try {
				await updateUser(userId, { gps_status: 'none' });
				Swal.fire('Rechazado', 'La solicitud fue rechazada.', 'success');
				await loadRequests();
			} catch (error) {
				console.error("Error rejecting request:", error);
				Swal.fire('Error', 'No se pudo rechazar la solicitud.', 'error');
			}
		}
	}
</script>

<AdminNavbar />

<section class="container my-4">
	<h2 class="mb-4 text-center">Gestión de Rastreadores</h2>

	<div class="card mb-5 p-3 shadow-sm border-0">
		<h4 class="mb-3 text-warning">Solicitudes de GPS Pendientes</h4>
		
		{#if loading}
			<div class="text-center py-3">
				<div class="spinner-border text-warning" role="status"></div>
			</div>
		{:else if pendingRequests.length === 0}
			<div class="alert alert-light text-center mb-0">
				No hay solicitudes pendientes en este momento.
			</div>
		{:else}
			<div class="table-responsive">
				<table class="table table-hover align-middle">
					<thead class="table-light">
						<tr>
							<th>Nombre</th>
							<th>Email</th>
							<th>Fecha de Solicitud</th>
							<th class="text-end">Acciones</th>
						</tr>
					</thead>
					<tbody>
						{#each pendingRequests as req}
							<tr>
								<td>{req.name} {req.last_name}</td>
								<td>{req.email}</td>
								<td>Pendiente</td>
								<td class="text-end">
									<button class="btn btn-sm btn-success me-2" on:click={() => approveRequest(req.id, req.name)}>
										Aprobar
									</button>
									<button class="btn btn-sm btn-outline-danger" on:click={() => rejectRequest(req.id, req.name)}>
										Rechazar
									</button>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		{/if}
	</div>

	<h4 class="mb-4 text-center">Rastreadores Globales Activos</h4>

	<div class="row g-3">
		{#each trackers as t (t.id)}
			<div class="col-12 col-md-6 col-lg-4">
				<div class="card p-3 shadow-sm border-0 border-start border-4 border-warning">
					<h5>{t.name}</h5>
					<p class="mb-1"><strong>Tipo:</strong> {t.type}</p>
					<p class="mb-1"><strong>Estado:</strong> <span class="badge bg-success">{t.status}</span></p>
					<p class="mb-0"><strong>Ubicación:</strong> {t.location}</p>
				</div>
			</div>
		{/each}
	</div>

	<div class="card mt-5 p-3 shadow-sm border-0">
		<h5 class="mb-3">Plataforma GPS Principal</h5>
		<div class="map-container">
			<iframe
				src={gpsUrl}
				title="Mapa GPS"
				width="100%"
				height="500"
				style="border:0;"
				loading="lazy"
			>
			</iframe>
		</div>
	</div>
</section>

<style>
	.map-container {
		width: 100%;
		height: 500px;
		overflow: hidden;
		border-radius: 10px;
	}

	iframe {
		width: 100%;
		height: 100%;
	}
</style>
