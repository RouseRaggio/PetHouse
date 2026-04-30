<script>
	import { onMount, tick } from 'svelte';
	import { Grid, h } from 'gridjs';
	import 'gridjs/dist/theme/mermaid.css';
	import Swal from 'sweetalert2';

	import { getAdoptions, changeAdoptionStatus } from '../../../api/adoption_service.js';
	import AdminNavbar from '$lib/components/AdminNavbar.svelte';

	let requests = [];
	let grid;
	let sortOrder = 'recent';

	let activeFilter = 'Todos';
	const filters = ['Todos', 'Pendiente', 'Aprobado', 'Rechazado'];

	const STATUS_ID = {
		Pendiente: 1, // PENDING
		Aprobado: 2, // APPROVED
		Rechazado: 3 // REJECTED
	};

	const STATUS_LABEL = {
		PENDING: 'Pendiente',
		APPROVED: 'Aprobado',
		REJECTED: 'Rechazado'
	};

	onMount(async () => {
		await loadRequests();
	});

	async function loadRequests() {
		try {
			const response = await getAdoptions();
			requests = response.data ?? response;
			await tick();
			renderGrid();
		} catch (error) {
			console.error('Error cargando solicitudes:', error);
		}
	}

	function getStatusName(r) {
		const raw = r.status?.name ?? 'PENDING';
		return STATUS_LABEL[raw] ?? raw;
	}

	function isPending(r) {
		return (r.status?.name ?? 'PENDING') === 'PENDING';
	}

	function getPetName(r) {
		return r.pet?.name ?? '—';
	}

	function getAdoptanteName(r) {
		const name = r.adoptante?.name ?? '';
		const last = r.adoptante?.last_name ?? '';
		return `${name} ${last}`.trim() || '—';
	}

	function getAdoptanteEmail(r) {
		return r.adoptante?.email ?? '—';
	}

	function getFilteredRequests() {
		if (activeFilter === 'Todos') return requests;
		const reverseMap = { Pendiente: 'PENDING', Aprobado: 'APPROVED', Rechazado: 'REJECTED' };
		return requests.filter((r) => r.status?.name === reverseMap[activeFilter]);
	}

	function renderGrid() {
		if (grid) grid.destroy();

		const filtered = getFilteredRequests();

		const statusBadge = (status) => {
			const map = { Pendiente: 'warning', Aprobado: 'success', Rechazado: 'danger' };
			return h('span', { className: `badge bg-${map[status] ?? 'secondary'}` }, status);
		};

		const boolBadge = (val) =>
			h(
				'span',
				{ className: `badge bg-${val ? 'primary' : 'light text-dark'}` },
				val ? 'Sí' : 'No'
			);

		grid = new Grid({
			columns: [
				{ name: 'Mascota', sort: true },
				{ name: 'Adoptante', sort: true },
				{ name: 'Correo', sort: true },
				{ name: 'Tracker', sort: false, formatter: (val) => boolBadge(val) },
				{ name: 'Fecha Solicitud', sort: true },
				{ name: 'Estado', formatter: (val) => statusBadge(val) },
				{
					name: 'Acciones',
					formatter: (_, row) => {
						const request = row.cells[6]?.data;
						if (!request) return '';

						const pending = isPending(request);

						return h('div', { className: 'd-flex gap-1' }, [
							h(
								'button',
								{
									className: `btn btn-sm btn-success${!pending ? ' disabled' : ''}`,
									onClick: () => pending && handleApprove(request)
								},
								'Aprobar'
							),
							h(
								'button',
								{
									className: `btn btn-sm btn-danger${!pending ? ' disabled' : ''}`,
									onClick: () => pending && handleReject(request)
								},
								'Rechazar'
							),
							...(request.cedula_url || request.recibo_url
								? [
										h(
											'button',
											{
												className: 'btn btn-sm btn-outline-secondary',
												onClick: () => showDocs(request)
											},
											'Docs'
										)
									]
								: [])
						]);
					}
				}
			],
			data: filtered
				.sort((a, b) => {
					if (sortOrder === 'recent') {
						return new Date(b.fecha_solicitud) - new Date(a.fecha_solicitud);
					}
					return (a.pet?.name || '').localeCompare(b.pet?.name || '');
				})
				.map((r) => [
					getPetName(r),
					getAdoptanteName(r),
					getAdoptanteEmail(r),
					r.quiere_tracker ?? false,
					r.fecha_solicitud ? new Date(r.fecha_solicitud).toLocaleDateString('es-CO') : '—',
					getStatusName(r),
					r
				]),
			search: true,
			sort: true,
			pagination: { limit: 5 }
		});

		grid.render(document.getElementById('adoption-table-wrapper'));
	}

	async function showDocs(request) {
		const openFile = (dataUrl) => {
			if (!dataUrl) return;
			try {
				const parts = dataUrl.split(',');
				const mime = parts[0].match(/:(.*?);/)[1];
				const b64 = parts[1];
				const bin = atob(b64);
				const len = bin.length;
				const arr = new Uint8Array(len);
				for (let i = 0; i < len; i++) {
					arr[i] = bin.charCodeAt(i);
				}
				const blob = new Blob([arr], { type: mime });
				const blobUrl = URL.createObjectURL(blob);
				window.open(blobUrl, '_blank');
			} catch (e) {
				console.error('Error opening file:', e);
				window.open(dataUrl, '_blank');
			}
		};

		// Hacer que la función esté disponible globalmente para el HTML del Swal
		window.openAdoptionDoc = openFile;

		const cedulaBtn = request.cedula_url
			? `<button onclick="window.openAdoptionDoc('${request.cedula_url}')" class="btn btn-primary w-100 mb-2">Ver Cédula</button>`
			: '<p class="text-muted">Sin cédula adjunta</p>';

		const reciboBtn = request.recibo_url
			? `<button onclick="window.openAdoptionDoc('${request.recibo_url}')" class="btn btn-outline-primary w-100">Ver Recibo</button>`
			: '<p class="text-muted">Sin recibo adjunto</p>';

		await Swal.fire({
			title: 'Documentos adjuntos',
			html: `<div class="p-3">${cedulaBtn}${reciboBtn}</div>`,
			icon: 'info',
			showConfirmButton: true,
			confirmButtonText: 'Cerrar'
		});
	}

	async function handleApprove(request) {
		const result = await Swal.fire({
			title: '¿Aprobar solicitud?',
			html: `¿Confirmas la adopción de <b>${getPetName(request)}</b> por parte de <b>${getAdoptanteName(request)}</b>?`,
			icon: 'question',
			showCancelButton: true,
			confirmButtonColor: '#198754',
			confirmButtonText: 'Sí, aprobar',
			cancelButtonText: 'Cancelar'
		});

		if (!result.isConfirmed) return;

		try {
			await changeAdoptionStatus(request.id, STATUS_ID.Aprobado);
			await Swal.fire({ title: '¡Aprobada!', text: 'La solicitud fue aprobada.', icon: 'success' });
			await loadRequests();
		} catch (error) {
			console.error('Error aprobando:', error);
			Swal.fire({ title: 'Error', text: 'No se pudo aprobar la solicitud.', icon: 'error' });
		}
	}

	async function handleReject(request) {
		const result = await Swal.fire({
			title: '¿Rechazar solicitud?',
			html: `¿Seguro que deseas rechazar la solicitud de <b>${getAdoptanteName(request)}</b>?`,
			icon: 'warning',
			input: 'textarea',
			inputPlaceholder: 'Motivo del rechazo (opcional)...',
			showCancelButton: true,
			confirmButtonColor: '#dc3545',
			confirmButtonText: 'Sí, rechazar',
			cancelButtonText: 'Cancelar'
		});

		if (!result.isConfirmed) return;

		try {
			await changeAdoptionStatus(request.id, STATUS_ID.Rechazado);
			await Swal.fire({ title: 'Rechazada', text: 'La solicitud fue rechazada.', icon: 'info' });
			await loadRequests();
		} catch (error) {
			console.error('Error rechazando:', error);
			Swal.fire({ title: 'Error', text: 'No se pudo rechazar la solicitud.', icon: 'error' });
		}
	}

	function setFilter(f) {
		activeFilter = f;
		renderGrid();
	}
</script>

<AdminNavbar />

<section class="container my-4">
	<div class="d-flex justify-content-between align-items-center mb-4">
		<h2 class="mb-0">Solicitudes de Adopción</h2>
		<div class="d-flex align-items-center gap-2">
			<span class="text-muted small">Ordenar por:</span>
			<select class="form-select form-select-sm w-auto" bind:value={sortOrder} on:change={renderGrid}>
				<option value="recent">Más recientes</option>
				<option value="alphabetical">Mascota (A-Z)</option>
			</select>
		</div>
	</div>

	<!-- TARJETAS RESUMEN -->
	<div class="row g-3 mb-4">
		<div class="col-md-3">
			<div class="card text-bg-secondary text-center p-3">
				<div class="fs-2 fw-bold">{requests.length}</div>
				<div>Total</div>
			</div>
		</div>
		<div class="col-md-3">
			<div class="card text-bg-warning text-center p-3">
				<div class="fs-2 fw-bold">{requests.filter((r) => isPending(r)).length}</div>
				<div>Pendientes</div>
			</div>
		</div>
		<div class="col-md-3">
			<div class="card text-bg-success text-center p-3">
				<div class="fs-2 fw-bold">
					{requests.filter((r) => r.status?.name === 'APPROVED').length}
				</div>
				<div>Aprobadas</div>
			</div>
		</div>
		<div class="col-md-3">
			<div class="card text-bg-danger text-center p-3">
				<div class="fs-2 fw-bold">
					{requests.filter((r) => r.status?.name === 'REJECTED').length}
				</div>
				<div>Rechazadas</div>
			</div>
		</div>
	</div>

	<!-- FILTROS -->
	<div class="mb-3">
		{#each filters as f}
			<button
				class="btn me-2 {activeFilter === f ? 'btn-dark' : 'btn-outline-secondary'}"
				on:click={() => setFilter(f)}
			>
				{f}
			</button>
		{/each}
	</div>

	<!-- TABLA -->
	<div id="adoption-table-wrapper"></div>
</section>
