<script>
	import { onMount, tick } from 'svelte';
	import { Grid, h } from 'gridjs';
	import 'gridjs/dist/theme/mermaid.css';
	import Swal from 'sweetalert2';

	import { getPets, deletePet, updatePet } from '../../../api/pet_service.js';
	import AdminNavbar from '$lib/components/AdminNavbar.svelte';

	let pets = [];
	let grid;

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
		if (grid) grid.destroy();

		grid = new Grid({
			columns: [
				'Nombre',
				'Especie',
				'Raza',
				'Estado',
				{
					name: 'Acciones',
					formatter: (_, row) => {
						const pet = row.cells[4]?.data;

						if (!pet) return '';

						return h('div', {}, [
							h(
								'button',
								{
									className: 'btn btn-sm btn-warning me-1',
									onClick: () => editPetStatus(pet)
								},
								'Editar Estado'
							),
							h(
								'button',
								{
									className: 'btn btn-sm btn-danger',
									onClick: () => removePet(pet.id)
								},
								'Eliminar'
							)
						]);
					}
				}
			],
			data: pets.map((p) => [p.name, p.species, p.race, p.status === 'AVAILABLE' ? 'Disponible' : p.status, p]),
			search: true,
			sort: true,
			pagination: { limit: 10 }
		});

		grid.render(document.getElementById('pets-table-wrapper'));
	}

	// =========================
	// ACTIONS
	// =========================
	async function removePet(id) {
		const result = await Swal.fire({
			title: '¿Eliminar mascota?',
			text: 'La publicación será eliminada permanentemente.',
			icon: 'warning',
			showCancelButton: true,
			confirmButtonText: 'Sí, eliminar',
			cancelButtonText: 'Cancelar'
		});

		if (!result.isConfirmed) return;

		try {
			await deletePet(id);

			await Swal.fire({
				title: 'Eliminada',
				text: 'La publicación fue eliminada correctamente',
				icon: 'success'
			});

			await loadPets();
		} catch (error) {
			console.error('Error eliminando mascota:', error);

			Swal.fire({
				title: 'Error',
				text: 'No se pudo eliminar la mascota',
				icon: 'error'
			});
		}
	}

	async function editPetStatus(pet) {
		const { value: formValues } = await Swal.fire({
			title: 'Editar Estado de Mascota',
			html: `
				<label for="swal-status" class="form-label">Estado:</label>
				<select id="swal-status" class="form-select">
					<option value="AVAILABLE" ${pet.status === 'AVAILABLE' ? 'selected' : ''}>Disponible</option>
					<option value="ADOPTED" ${pet.status === 'ADOPTED' ? 'selected' : ''}>Adoptado</option>
					<option value="RESERVED" ${pet.status === 'RESERVED' ? 'selected' : ''}>Reservado</option>
					<option value="UNAVAILABLE" ${pet.status === 'UNAVAILABLE' ? 'selected' : ''}>No disponible</option>
				</select>
				
				<label for="swal-name" class="form-label mt-3">Nombre:</label>
				<input id="swal-name" class="form-control" value="${pet.name}">
			`,
			focusConfirm: false,
			showCancelButton: true,
			confirmButtonText: 'Guardar',
			cancelButtonText: 'Cancelar',
			preConfirm: () => {
				return {
					status: document.getElementById('swal-status').value,
					name: document.getElementById('swal-name').value,
				};
			}
		});

		if (formValues) {
			try {
				await updatePet(pet.id, { 
					status: formValues.status,
					name: formValues.name 
				});
				
				await Swal.fire('¡Actualizado!', 'La mascota ha sido actualizada.', 'success');
				await loadPets();
			} catch (error) {
				console.error('Error al actualizar mascota:', error);
				Swal.fire('Error', 'Hubo un problema al actualizar.', 'error');
			}
		}
	}
</script>

<AdminNavbar />

<section class="container my-4">
	<h2 class="mb-4">Gestión de Mascotas y Publicaciones</h2>

	<div class="card p-3 shadow-sm">
		<div id="pets-table-wrapper"></div>
	</div>
</section>
