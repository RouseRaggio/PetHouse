<script>
	import { onMount, tick } from 'svelte';
	import { fly } from 'svelte/transition';
	import { Grid, h } from 'gridjs';
	import 'gridjs/dist/theme/mermaid.css';
	import Swal from 'sweetalert2';

	import { getPets, deletePet, updatePet } from '../../../api/pet_service.js';
	import AdminNavbar from '$lib/components/AdminNavbar.svelte';

	let pets = [];
	let grid;
	let sortOrder = 'recent';

	// Reactividad para asegurar que cargue sin refrescar
	$: if (pets) {
		tick().then(() => renderGrid());
	}

	// =========================
	// LOAD PETS
	// =========================
	onMount(async () => {
		await loadPets();
	});

	async function loadPets() {
		try {
			const response = await getPets();
			pets = response.data ?? response;

			await tick();
			renderGrid();
		} catch (error) {
			console.error('Error cargando mascotas:', error);
		}
	}

	// =========================
	// GRID
	// =========================
	function renderGrid() {
		const container = document.getElementById('pets-table-wrapper');
		if (!container) return;
		if (grid) grid.destroy();

		grid = new Grid({
			columns: [
				'Nombre',
				{
					name: 'Publicado por',
					formatter: (cell) => h('span', { className: 'fw-bold text-primary' }, cell)
				},
				'Especie',
				'Raza',
				{
					name: 'Estado',
					formatter: (cell) => {
						const statusMap = {
							'PENDING_APPROVAL': { text: '🟠 Solicitud', class: 'badge bg-warning text-dark' },
							'AVAILABLE': { text: '🟢 Publicada', class: 'badge bg-success' },
							'ADOPTED': { text: '🔵 Adoptada', class: 'badge bg-info' },
							'REJECTED': { text: '🔴 Rechazada', class: 'badge bg-danger' }
						};
						const info = statusMap[cell] || { text: cell, class: 'badge bg-secondary' };
						return h('span', { className: info.class + ' p-2 rounded-pill shadow-sm' }, info.text);
					}
				},
				{ name: 'Fecha Registro', sort: true },
				{
					name: 'Acciones',
					formatter: (_, row) => {
						const pet = row.cells[6]?.data;
						if (!pet) return '';

						const buttons = [];

						if (pet.status === 'PENDING_APPROVAL') {
							buttons.push(h('button', {
								className: 'btn btn-sm btn-success me-1 shadow-sm',
								onClick: () => approvePet(pet)
							}, 'Aprobar'));
							
							buttons.push(h('button', {
								className: 'btn btn-sm btn-outline-danger me-1 shadow-sm',
								onClick: () => rejectPet(pet)
							}, 'Rechazar'));
						}

						buttons.push(h('button', {
							className: 'btn btn-sm btn-light border me-1 shadow-sm',
							onClick: () => editPetStatus(pet)
						}, '⚙️'));

						buttons.push(h('button', {
							className: 'btn btn-sm btn-outline-danger shadow-sm',
							onClick: () => removePet(pet.id)
						}, '🗑️'));

						return h('div', { className: 'd-flex' }, buttons);
					}
				}
			],
			data: [...pets]
				.sort((a, b) => {
					if (sortOrder === 'recent') {
						return new Date(b.created_at) - new Date(a.created_at);
					}
					return a.name.localeCompare(b.name);
				})
				.map((p) => [
					p.name,
					p.publisher_name || 'Desconocido',
					p.species,
					p.race,
					p.status,
					p.created_at ? new Date(p.created_at).toLocaleDateString('es-CO') : '—',
					p
				]),
			search: true,
			sort: true,
			pagination: { limit: 10 },
			language: {
				search: { placeholder: '🔍 Buscar mascota o usuario...' },
				pagination: { previous: 'Anterior', next: 'Siguiente' }
			}
		});

		grid.render(container);
	}

	// =========================
	// ACTIONS
	// =========================
	async function approvePet(pet) {
		const result = await Swal.fire({
			title: '¿Aprobar publicación?',
			text: `La mascota "${pet.name}" será visible en el catálogo público.`,
			icon: 'question',
			showCancelButton: true,
			confirmButtonText: 'Sí, publicar',
			confirmButtonColor: '#4361ee'
		});

		if (result.isConfirmed) {
			try {
				await updatePet(pet.id, { status: 'AVAILABLE' });
				Swal.fire('¡Publicada!', 'La mascota ahora es visible.', 'success');
				await loadPets();
			} catch (e) { Swal.fire('Error', e.message, 'error'); }
		}
	}

	async function rejectPet(pet) {
		const result = await Swal.fire({
			title: '¿Rechazar solicitud?',
			text: 'Se le notificará al usuario que la solicitud fue rechazada.',
			icon: 'warning',
			showCancelButton: true,
			confirmButtonText: 'Sí, rechazar',
			confirmButtonColor: '#ff6b6b'
		});

		if (result.isConfirmed) {
			try {
				await updatePet(pet.id, { status: 'REJECTED' });
				Swal.fire('Rechazada', 'La solicitud ha sido marcada como rechazada.', 'success');
				await loadPets();
			} catch (e) { Swal.fire('Error', e.message, 'error'); }
		}
	}

	async function removePet(id) {
		const result = await Swal.fire({
			title: '¿Eliminar permanentemente?',
			text: 'Esta acción borrará todos los datos de la mascota.',
			icon: 'error',
			showCancelButton: true,
			confirmButtonText: 'Sí, borrar',
			confirmButtonColor: '#d33'
		});

		if (!result.isConfirmed) return;

		try {
			await deletePet(id);
			await loadPets();
		} catch (error) { Swal.fire('Error', 'No se pudo eliminar.', 'error'); }
	}

	async function editPetStatus(pet) {
		const { value: formValues } = await Swal.fire({
			title: 'Editar Mascota',
			html: `
				<div class="text-start">
					<label class="form-label small fw-bold">Estado:</label>
					<select id="swal-status" class="form-select mb-3">
						<option value="PENDING_APPROVAL" ${pet.status === 'PENDING_APPROVAL' ? 'selected' : ''}>🟠 Solicitud Pendiente</option>
						<option value="AVAILABLE" ${pet.status === 'AVAILABLE' ? 'selected' : ''}>🟢 Disponible / Publicada</option>
						<option value="ADOPTED" ${pet.status === 'ADOPTED' ? 'selected' : ''}>🔵 Adoptada</option>
						<option value="REJECTED" ${pet.status === 'REJECTED' ? 'selected' : ''}>🔴 Rechazada</option>
					</select>
					
					<label class="form-label small fw-bold">Nombre:</label>
					<input id="swal-name" class="form-control" value="${pet.name}">
				</div>
			`,
			focusConfirm: false,
			showCancelButton: true,
			confirmButtonText: 'Guardar Cambios',
			preConfirm: () => {
				return {
					status: document.getElementById('swal-status').value,
					name: document.getElementById('swal-name').value,
				};
			}
		});

		if (formValues) {
			try {
				await updatePet(pet.id, formValues);
				await loadPets();
				Swal.fire('¡Listo!', 'Cambios guardados correctamente.', 'success');
			} catch (error) { Swal.fire('Error', 'No se pudo actualizar.', 'error'); }
		}
	}
</script>

<AdminNavbar />

<main class="admin-pets-page py-5 bg-light min-vh-100">
	<div class="container" in:fly={{ y: 20, duration: 600 }}>
		<div class="d-flex flex-column flex-md-row justify-content-between align-items-center mb-4 gap-3">
			<div>
				<h1 class="fw-bold h2 mb-1">Mascotas y Publicaciones</h1>
				<p class="text-muted mb-0">Gestiona las solicitudes de la comunidad y el catálogo público.</p>
			</div>
			
			<div class="d-flex align-items-center gap-2 bg-white p-2 rounded-3 border shadow-sm">
				<i class="bi bi-sort-alpha-down text-primary ms-2"></i>
				<select class="form-select form-select-sm border-0 shadow-none w-auto" bind:value={sortOrder} on:change={renderGrid}>
					<option value="recent">Más recientes</option>
					<option value="alphabetical">Nombre (A-Z)</option>
				</select>
			</div>
		</div>

		<div class="card border-0 shadow-sm rounded-4 overflow-hidden">
			<div class="card-body p-0">
				<div id="pets-table-wrapper"></div>
			</div>
		</div>
	</div>
</main>

<style>
	:global(.gridjs-container) {
		border-radius: 0 !important;
		padding: 0 !important;
	}
	:global(.gridjs-wrapper) {
		border: none !important;
		box-shadow: none !important;
	}
	:global(.gridjs-th) {
		background-color: #f8f9fa !important;
		color: #495057 !important;
		text-transform: uppercase !important;
		font-size: 0.75rem !important;
		letter-spacing: 1px !important;
		padding: 15px !important;
	}
	:global(.gridjs-td) {
		padding: 15px !important;
		vertical-align: middle !important;
	}
</style>
