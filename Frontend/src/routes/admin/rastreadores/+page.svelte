<script>
	import AdminNavbar from '$lib/components/AdminNavbar.svelte';
	import { onMount } from 'svelte';
	import { getPets, updatePet } from '../../../api/pet_service.js';
	import Swal from 'sweetalert2';

	let pendingRequests = [];
	let approvedPets = [];
	let loading = true;

	// URL del panel del GPS ya logueado
	let gpsUrl = 'https://www.365gps.net/platform/#/';

	onMount(async () => {
		await loadRequests();
	});

	async function loadRequests() {
		try {
			const pets = await getPets();
			pendingRequests = pets.filter(p => p.gps_status === 'pending');
			approvedPets = pets.filter(p => p.gps_status === 'approved');
		} catch (error) {
			console.error('Error loading pets:', error);
		} finally {
			loading = false;
		}
	}

	async function approveRequest(petId, petName, adopterName) {
		const { value: imei } = await Swal.fire({
			title: 'Aprobar solicitud de GPS',
			text: `Ingresa el IMEI para la mascota ${petName} (Dueño: ${adopterName || 'N/A'}):`,
			input: 'text',
			inputPlaceholder: 'Número de IMEI (ej: 8634...)',
			showCancelButton: true,
			confirmButtonText: 'Aprobar y Asignar',
			cancelButtonText: 'Cancelar',
			inputValidator: (value) => {
				if (!value) {
					return '¡Debes ingresar un IMEI!'
				}
			}
		});

		if (imei) {
			try {
				await updatePet(petId, { 
					gps_status: 'approved',
					gps_imei: imei
				});
				Swal.fire('¡Aprobado!', `La mascota ${petName} ahora tiene GPS con IMEI: ${imei}`, 'success');
				await loadRequests();
			} catch (error) {
				console.error("Error approving request:", error);
				Swal.fire('Error', 'No se pudo aprobar la solicitud.', 'error');
			}
		}
	}

	async function rejectRequest(petId, petName) {
		const result = await Swal.fire({
			title: '¿Rechazar solicitud?',
			text: `Vas a rechazar la solicitud de GPS de la mascota ${petName}.`,
			icon: 'warning',
			showCancelButton: true,
			confirmButtonText: 'Sí, rechazar',
			cancelButtonText: 'Cancelar'
		});

		if (result.isConfirmed) {
			try {
				await updatePet(petId, { gps_status: 'none' });
				Swal.fire('Rechazado', 'La solicitud fue rechazada.', 'success');
				await loadRequests();
			} catch (error) {
				console.error("Error rejecting request:", error);
				Swal.fire('Error', 'No se pudo rechazar la solicitud.', 'error');
			}
		}
	}

	async function editIMEI(petId, petName, currentImei) {
		const { value: imei } = await Swal.fire({
			title: 'Editar IMEI',
			text: `Actualiza el IMEI para ${petName}:`,
			input: 'text',
			inputValue: currentImei,
			showCancelButton: true,
			confirmButtonText: 'Guardar cambios',
			cancelButtonText: 'Cancelar',
			inputValidator: (value) => {
				if (!value) {
					return '¡El IMEI no puede estar vacío!'
				}
			}
		});

		if (imei && imei !== currentImei) {
			try {
				await updatePet(petId, { gps_imei: imei });
				Swal.fire('Actualizado', 'El IMEI ha sido actualizado correctamente.', 'success');
				await loadRequests();
			} catch (error) {
				console.error("Error updating IMEI:", error);
				Swal.fire('Error', 'No se pudo actualizar el IMEI.', 'error');
			}
		}
	}

	async function revokeGPS(petId, petName) {
		const result = await Swal.fire({
			title: '¿Revocar acceso GPS?',
			text: `Se eliminará el acceso GPS para la mascota ${petName}.`,
			icon: 'warning',
			showCancelButton: true,
			confirmButtonColor: '#d33',
			confirmButtonText: 'Sí, revocar acceso',
			cancelButtonText: 'Cancelar'
		});

		if (result.isConfirmed) {
			try {
				await updatePet(petId, { 
					gps_status: 'none',
					gps_imei: null 
				});
				Swal.fire('Acceso Revocado', 'El servicio de GPS ha sido desactivado para esta mascota.', 'success');
				await loadRequests();
			} catch (error) {
				console.error("Error revoking GPS:", error);
				Swal.fire('Error', 'No se pudo revocar el acceso.', 'error');
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
							<th>Mascota</th>
							<th>Dueño</th>
							<th>Fecha de Solicitud</th>
							<th class="text-end">Acciones</th>
						</tr>
					</thead>
					<tbody>
						{#each pendingRequests as req}
							<tr>
								<td><strong>{req.name}</strong> ({req.species})</td>
								<td>{req.adopter_name || 'Desconocido'}</td>
								<td>Pendiente</td>
								<td class="text-end">
									<button class="btn btn-sm btn-success me-2" on:click={() => approveRequest(req.id, req.name, req.adopter_name)}>
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

	<div class="card mb-5 p-3 shadow-sm border-0">
		<h4 class="mb-3 text-success">Mascotas con GPS Activo</h4>
		
		{#if loading}
			<div class="text-center py-3">
				<div class="spinner-border text-success" role="status"></div>
			</div>
		{:else if approvedPets.length === 0}
			<div class="alert alert-light text-center mb-0">
				Aún no hay mascotas con GPS activado.
			</div>
		{:else}
			<div class="table-responsive">
				<table class="table table-hover align-middle">
					<thead class="table-success">
						<tr>
							<th>Mascota</th>
							<th>Dueño</th>
							<th>IMEI Asignado</th>
							<th class="text-end">Acciones</th>
						</tr>
					</thead>
					<tbody>
						{#each approvedPets as pet}
							<tr>
								<td><strong>{pet.name}</strong></td>
								<td>{pet.adopter_name || 'N/A'}</td>
								<td><code>{pet.gps_imei || 'N/A'}</code></td>
								<td class="text-end">
									<button class="btn btn-sm btn-outline-primary me-2" on:click={() => editIMEI(pet.id, pet.name, pet.gps_imei)}>
										<i class="bi bi-pencil"></i>
									</button>
									<button class="btn btn-sm btn-outline-danger" on:click={() => revokeGPS(pet.id, pet.name)}>
										<i class="bi bi-trash"></i>
									</button>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		{/if}
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
