
<script>
	import { onMount, tick } from 'svelte';
	import Swal from 'sweetalert2';
	import { fly, fade } from 'svelte/transition';
	import AdminNavbar from '$lib/components/AdminNavbar.svelte';
	import { PUBLIC_API_URL } from '$env/static/public';

	export let data; // Recibir datos del server load

	let auditLogs = [];
	let filteredLogs = [];
	let loading = false;
	let showDetailModal = false;
	let selectedLog = null;
	let users = [];

	// Filters
	let filterAction = '';
	let filterResource = '';
	let filterUser = '';
	let startDate = '';
	let endDate = '';
	let searchTerm = '';

	// Pagination
	let currentPage = 1;
	let pageSize = 20;
	let pageSizeOptions = [20, 50, 100];

	onMount(async () => {
		// Usar datos del server si están disponibles
		if (data?.historial && Array.isArray(data.historial)) {
			auditLogs = data.historial;
			users = data.users || [];
			applySearch();
		} else {
			await fetchAuditLogs();
		}
	});

	async function fetchAuditLogs() {
		loading = true;
		try {
			const token = localStorage.getItem('token');
			const headers = {
				'Content-Type': 'application/json',
				...(token ? { 'Authorization': `Bearer ${token}` } : {})
			};

			const apiUrl = PUBLIC_API_URL || 'http://localhost:8000';
			const params = new URLSearchParams({
				limit: pageSize,
				offset: (currentPage - 1) * pageSize
			});

			if (filterAction) params.append('action', filterAction);
			if (filterResource) params.append('resource', filterResource);
			if (filterUser) params.append('user_id', filterUser);
			if (startDate) params.append('start_date', new Date(startDate).toISOString());
			if (endDate) params.append('end_date', new Date(endDate).toISOString());

			const response = await fetch(`${apiUrl}/audit-logs/?${params}`, { headers });
			
			if (!response.ok) {
				throw new Error('Error al cargar el historial');
			}

			auditLogs = await response.json();
			applySearch();
		} catch (error) {
			console.error('Error fetching audit logs:', error);
			Swal.fire({
				icon: 'error',
				title: 'Error de Carga',
				text: 'No se pudo obtener el historial. Verifica tu conexión.',
				confirmButtonColor: '#ff6b6b'
			});
		} finally {
			loading = false;
		}
	}

	function applySearch() {
		if (searchTerm.trim() === '') {
			filteredLogs = auditLogs;
		} else {
			const term = searchTerm.toLowerCase();
			filteredLogs = auditLogs.filter(
				(log) =>
					log.action.toLowerCase().includes(term) ||
					log.resource.toLowerCase().includes(term) ||
					(log.details && log.details.toLowerCase().includes(term)) ||
					(getUserName(log.user_id) && getUserName(log.user_id).toLowerCase().includes(term))
			);
		}
	}

	async function exportToCSV() {
		try {
			const token = localStorage.getItem('token');
			const headers = {
				'Content-Type': 'application/json',
				...(token ? { 'Authorization': `Bearer ${token}` } : {})
			};

			const apiUrl = PUBLIC_API_URL || 'http://localhost:8000';
			const params = new URLSearchParams();

			if (filterAction) params.append('action', filterAction);
			if (filterResource) params.append('resource', filterResource);
			if (filterUser) params.append('user_id', filterUser);
			if (startDate) params.append('start_date', new Date(startDate).toISOString());
			if (endDate) params.append('end_date', new Date(endDate).toISOString());

			const response = await fetch(`${apiUrl}/audit-logs/export/csv?${params}`, { headers });
			
			if (!response.ok) {
				throw new Error('Error al exportar');
			}

			const csv = await response.text();
			const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
			const url = URL.createObjectURL(blob);
			const element = document.createElement('a');
			element.setAttribute('href', url);
			element.setAttribute('download', `auditoria_${new Date().toISOString().slice(0, 10)}.csv`);
			element.style.display = 'none';
			document.body.appendChild(element);
			element.click();
			document.body.removeChild(element);
			URL.revokeObjectURL(url);

			Swal.fire({
				icon: 'success',
				title: '¡Exportado!',
				text: 'El archivo CSV se ha descargado.',
				confirmButtonColor: '#4361ee'
			});
		} catch (error) {
			console.error('Error:', error);
			Swal.fire('Error', 'No se pudo exportar el historial.', 'error');
		}
	}

	async function resetFilters() {
		filterAction = '';
		filterResource = '';
		filterUser = '';
		startDate = '';
		endDate = '';
		searchTerm = '';
		currentPage = 1;
		await fetchAuditLogs();
	}

	function viewDetails(log) {
		selectedLog = log;
		showDetailModal = true;
	}

	function formatDate(dateString) {
		if (!dateString) return '-';
		return new Date(dateString).toLocaleString('es-CO', {
			day: '2-digit',
			month: '2-digit',
			year: 'numeric',
			hour: '2-digit',
			minute: '2-digit',
			second: '2-digit'
		});
	}

	function getUserName(userId) {
		if (!userId) return 'Sistema';
		const user = users.find(u => u.id === userId);
		return user ? user.nombre || user.email || `Usuario #${userId}` : `Usuario #${userId}`;
	}

	function getActionBadge(action) {
		const config = {
			create: { class: 'badge-create', label: 'Crear', icon: 'bi-plus-circle' },
			update: { class: 'badge-update', label: 'Editar', icon: 'bi-pencil' },
			delete: { class: 'badge-delete', label: 'Borrar', icon: 'bi-trash' },
			login: { class: 'badge-login', label: 'Login', icon: 'bi-box-arrow-in-right' },
			login_failed: { class: 'badge-failed', label: 'Fallo', icon: 'bi-exclamation-triangle' }
		};
		return config[action] || { class: 'bg-secondary', label: action, icon: 'bi-dot' };
	}

	function getResourceLabel(resource) {
		const labels = {
			user: 'Usuario',
			pet: 'Mascota',
			adoption: 'Adopción',
			tracker: 'Rastreador',
			role: 'Rol',
			permission: 'Permiso'
		};
		return labels[resource] || resource;
	}

	function getDetailDescription(log) {
		const userName = getUserName(log.user_id);
		const resourceLabel = getResourceLabel(log.resource);
		const actionLabel = getActionBadge(log.action).label;

		if (log.details) {
			return log.details;
		}

		if (log.action === 'login') {
			return `${userName} inició sesión`;
		} else if (log.action === 'login_failed') {
			return `Intento fallido de inicio de sesión desde ${log.ip_address || 'desconocido'}`;
		} else {
			return `${userName} ${actionLabel.toLowerCase()} ${resourceLabel.toLowerCase()} #${log.resource_id || 'N/A'}`;
		}
	}
</script>

<AdminNavbar />

<main class="history-page py-5">
	<div class="container" in:fade>
		<header
			class="d-flex flex-column flex-md-row justify-content-between align-items-end mb-4 gap-3"
		>
			<div in:fly={{ x: -20, duration: 600 }}>
				<span class="history-badge mb-2">📋 Auditoría General</span>
				<h1 class="fw-bold display-6 mb-0">Historial de Actividad</h1>
				<p class="text-muted">Monitorea cada cambio y acción realizada en el sistema.</p>
			</div>

			<div class="d-flex gap-2">
				<button class="btn btn-export shadow-sm" on:click={exportToCSV}>
					<i class="bi bi-download me-2"></i> Exportar CSV
				</button>
			</div>
		</header>

		<!-- Filtros Premium -->
		<div class="card filter-card mb-4 p-4 shadow-sm" in:fly={{ y: 20, duration: 600, delay: 100 }}>
			<div class="row g-3">
				<div class="col-md-2">
					<label class="cartoon-label">Usuario</label>
					<select class="form-select cartoon-input" bind:value={filterUser}>
						<option value="">Todos los usuarios</option>
						{#each users as user}
							<option value={user.id}>{user.nombre || user.email}</option>
						{/each}
					</select>
				</div>
				<div class="col-md-2">
					<label class="cartoon-label">Acción</label>
					<select class="form-select cartoon-input" bind:value={filterAction}>
						<option value="">Todas las acciones</option>
						<option value="create">Crear</option>
						<option value="update">Actualizar</option>
						<option value="delete">Eliminar</option>
						<option value="login">Inicio Sesión</option>
					</select>
				</div>
				<div class="col-md-2">
					<label class="cartoon-label">Recurso</label>
					<select class="form-select cartoon-input" bind:value={filterResource}>
						<option value="">Todos los recursos</option>
						<option value="user">Usuarios</option>
						<option value="pet">Mascotas</option>
						<option value="adoption">Adopciones</option>
					</select>
				</div>
				<div class="col-md-3">
					<label class="cartoon-label">Rango de Fechas</label>
					<div class="input-group">
						<input type="date" class="form-control cartoon-input" bind:value={startDate} />
						<span class="input-group-text bg-transparent border-0">al</span>
						<input type="date" class="form-control cartoon-input" bind:value={endDate} />
					</div>
				</div>
				<div class="col-md-3 d-flex align-items-end gap-2">
					<button class="btn btn-search w-100" on:click={fetchAuditLogs}>
						<i class="bi bi-search"></i>
					</button>
					<button class="btn btn-outline-secondary rounded-pill" on:click={resetFilters}>
						<i class="bi bi-arrow-counterclockwise"></i>
					</button>
				</div>
			</div>
		</div>

		<!-- Búsqueda rápida -->
		<div class="search-box mb-4" in:fly={{ y: 20, duration: 600, delay: 200 }}>
			<input
				type="text"
				class="form-control form-control-lg cartoon-input ps-4"
				placeholder="🔍 Buscar por detalles, recurso o usuario..."
				bind:value={searchTerm}
				on:input={applySearch}
			/>
		</div>

		<!-- Tabla Premium -->
		<div
			class="card border-0 shadow-sm rounded-4 overflow-hidden mb-4"
			in:fly={{ y: 20, duration: 600, delay: 300 }}
		>
			<div class="table-responsive">
				<table class="table table-hover align-middle mb-0">
					<thead class="table-ink text-white">
						<tr>
							<th class="ps-4">Usuario</th>
							<th>Acción</th>
							<th>Recurso</th>
							<th>Fecha y Hora</th>
							<th>Estado</th>
							<th class="text-center pe-4">Detalle</th>
						</tr>
					</thead>
					<tbody>
						{#if loading}
							<tr>
								<td colspan="6" class="text-center py-5">
									<div class="spinner-border text-mustard" role="status"></div>
									<p class="mt-2 fw-bold">Cargando bitácora...</p>
								</td>
							</tr>
						{:else if filteredLogs.length === 0}
							<tr>
								<td colspan="6" class="text-center py-5 text-muted">
									<i class="bi bi-journal-x display-4 d-block mb-3 opacity-20"></i>
									<p class="fw-bold">No se encontraron registros con esos filtros.</p>
									<button class="btn btn-sm btn-outline-primary" on:click={resetFilters}>
										<i class="bi bi-arrow-counterclockwise"></i> Limpiar filtros
									</button>
								</td>
							</tr>
						{:else}
							{#each filteredLogs as log (log.id)}
								<tr class="log-row">
									<td class="ps-4">
										<div class="d-flex align-items-center gap-2">
											<div class="user-avatar-small">
												{log.user_id ? '👤' : '⚙️'}
											</div>
											<div>
												<div class="fw-bold small">
													{getUserName(log.user_id)}
												</div>
												<div class="text-muted x-small">{log.ip_address || 'Sin IP'}</div>
											</div>
										</div>
									</td>
									<td>
										<span class="badge-cartoon {getActionBadge(log.action).class}">
											<i class="bi {getActionBadge(log.action).icon} me-1"></i>
											{getActionBadge(log.action).label}
										</span>
									</td>
									<td>
										<span class="fw-bold text-dark">{getResourceLabel(log.resource)}</span>
										<span class="text-muted small">#{log.resource_id || '-'}</span>
									</td>
									<td class="text-muted small">{formatDate(log.timestamp)}</td>
									<td>
										{#if log.status === 'success'}
											<span class="text-success small fw-bold"
												><i class="bi bi-check-circle-fill"></i> Ok</span
											>
										{:else}
											<span class="text-danger small fw-bold"
												><i class="bi bi-x-circle-fill"></i> Error</span
											>
										{/if}
									</td>
									<td class="text-center pe-4">
										<button class="btn btn-detail-circle" on:click={() => viewDetails(log)} title="Ver detalles">
											<i class="bi bi-eye"></i>
										</button>
									</td>
								</tr>
							{/each}
						{/if}
					</tbody>
				</table>
			</div>
		</div>

		<!-- Paginación -->
		{#if filteredLogs.length > 0}
			<div class="card border-0 shadow-sm rounded-4 p-4 pagination-card" in:fly={{ y: 20, duration: 600, delay: 400 }}>
				<div class="d-flex flex-wrap justify-content-between align-items-center gap-3">
					<div class="d-flex align-items-center gap-2">
						<span class="text-muted">Registros por página:</span>
						<select class="form-select form-select-sm cartoon-input" bind:value={pageSize} on:change={fetchAuditLogs} style="width: 80px;">
							{#each pageSizeOptions as size}
								<option value={size}>{size}</option>
							{/each}
						</select>
					</div>

					<div class="text-center">
						<span class="fw-bold text-ink">Página {currentPage}</span>
					</div>

					<div class="d-flex gap-2">
						<button
							class="btn btn-outline-ink rounded-pill"
							disabled={currentPage === 1}
							on:click={() => {
								currentPage = Math.max(1, currentPage - 1);
								fetchAuditLogs();
							}}
						>
							<i class="bi bi-chevron-left"></i> Anterior
						</button>
						<button
							class="btn btn-outline-ink rounded-pill"
							disabled={filteredLogs.length < pageSize}
							on:click={() => {
								currentPage = currentPage + 1;
								fetchAuditLogs();
							}}
						>
							Siguiente <i class="bi bi-chevron-right"></i>
						</button>
					</div>
				</div>
			</div>
		{/if}
	</div>
</main>

<!-- Modal Detalle Cartoon -->
{#if showDetailModal && selectedLog}
	<div class="modal d-block" tabindex="-1" in:fade>
		<div class="modal-dialog modal-dialog-centered modal-lg">
			<div class="modal-content cartoon-modal">
				<div class="modal-header border-0 pb-0">
					<h5 class="fw-bold mb-0">Detalle del Registro #{selectedLog.id}</h5>
					<button type="button" class="btn-close" on:click={() => (showDetailModal = false)}
					></button>
				</div>
				<div class="modal-body">
					<div class="row g-4">
						<!-- Descripción general de la acción -->
						<div class="col-12">
							<div class="detail-item p-3 rounded-4 bg-light">
								<label class="x-small text-muted text-uppercase fw-bold d-block mb-2">📝 Descripción</label>
								<div class="fw-bold fs-5">{getDetailDescription(selectedLog)}</div>
							</div>
						</div>

						<!-- Usuario que realizó la acción -->
						<div class="col-md-6">
							<div class="detail-item p-3 rounded-4">
								<label class="x-small text-muted text-uppercase fw-bold">👤 Actor</label>
								<div class="fw-bold">
									{getUserName(selectedLog.user_id)}
								</div>
								{#if selectedLog.user_id}
									<div class="text-muted small">ID: {selectedLog.user_id}</div>
								{:else}
									<div class="text-muted small">Proceso automático</div>
								{/if}
							</div>
						</div>

						<!-- Fecha y hora exacta -->
						<div class="col-md-6">
							<div class="detail-item p-3 rounded-4">
								<label class="x-small text-muted text-uppercase fw-bold">🕐 Fecha y Hora</label>
								<div class="fw-bold">{formatDate(selectedLog.timestamp)}</div>
							</div>
						</div>

						<!-- Acción realizada -->
						<div class="col-md-4">
							<div class="detail-item p-3 rounded-4">
								<label class="x-small text-muted text-uppercase fw-bold">⚡ Acción</label>
								<span class="badge-cartoon {getActionBadge(selectedLog.action).class}">
									<i class="bi {getActionBadge(selectedLog.action).icon}"></i>
									{getActionBadge(selectedLog.action).label}
								</span>
							</div>
						</div>

						<!-- Recurso afectado -->
						<div class="col-md-4">
							<div class="detail-item p-3 rounded-4">
								<label class="x-small text-muted text-uppercase fw-bold">🎯 Recurso</label>
								<div class="fw-bold">{getResourceLabel(selectedLog.resource)}</div>
								<div class="text-muted small">ID: {selectedLog.resource_id || '-'}</div>
							</div>
						</div>

						<!-- Estado de la operación -->
						<div class="col-md-4">
							<div class="detail-item p-3 rounded-4">
								<label class="x-small text-muted text-uppercase fw-bold">✓ Estado</label>
								{#if selectedLog.status === 'success'}
									<span class="text-success fw-bold">
										<i class="bi bi-check-circle-fill"></i> Exitosa
									</span>
								{:else}
									<span class="text-danger fw-bold">
										<i class="bi bi-x-circle-fill"></i> Fallida
									</span>
								{/if}
							</div>
						</div>

						<!-- IP Address si está disponible -->
						{#if selectedLog.ip_address}
							<div class="col-12">
								<div class="detail-item p-3 rounded-4">
									<label class="x-small text-muted text-uppercase fw-bold">🌐 Dirección IP</label>
									<div class="fw-bold font-monospace">{selectedLog.ip_address}</div>
								</div>
							</div>
						{/if}

						<!-- Detalles adicionales -->
						{#if selectedLog.details}
							<div class="col-12">
								<div class="detail-item p-3 rounded-4">
									<label class="x-small text-muted text-uppercase fw-bold">📌 Detalles Adicionales</label>
									<div class="mt-2">{selectedLog.details}</div>
								</div>
							</div>
						{/if}

						<!-- Cambios realizados (JSON) -->
						{#if selectedLog.changes}
							<div class="col-12">
								<div class="detail-item p-3 rounded-4">
									<label class="x-small text-muted text-uppercase fw-bold">📊 Cambios (JSON)</label>
									<pre class="changes-pre mt-2">{JSON.stringify(
										selectedLog.changes,
										null,
										2
									)}</pre>
								</div>
							</div>
						{/if}
					</div>
				</div>
				<div class="modal-footer border-0">
					<button
						type="button"
						class="btn btn-ink text-white px-4 rounded-pill"
						on:click={() => (showDetailModal = false)}>Cerrar</button
					>
				</div>
			</div>
		</div>
	</div>
	<div class="modal-backdrop fade show"></div>
{/if}

<style>
	.history-page {
		background: var(--cream);
		min-height: 100vh;
		font-family: var(--font-body);
	}

	.history-badge {
		background: var(--mustard);
		color: var(--ink);
		font-weight: 800;
		padding: 4px 16px;
		border-radius: 50px;
		display: inline-block;
		border: 2px solid var(--ink);
		font-size: 0.85rem;
	}

	.filter-card {
		border: 3px solid var(--ink);
		border-radius: 20px;
		box-shadow: 6px 6px 0 var(--ink);
	}

	.cartoon-label {
		font-family: var(--font-display);
		font-weight: 700;
		font-size: 0.9rem;
		color: var(--ink);
		margin-bottom: 5px;
	}

	.cartoon-input {
		border: 2.5px solid var(--ink) !important;
		border-radius: 12px !important;
		font-weight: 600;
		font-size: 0.9rem;
	}

	.btn-search {
		background: var(--coral);
		color: white;
		border: 2.5px solid var(--ink);
		border-radius: 12px;
		height: 45px;
		box-shadow: 3px 3px 0 var(--ink);
		transition: all 0.2s;
	}

	.btn-search:hover {
		transform: translate(-2px, -2px);
		box-shadow: 5px 5px 0 var(--ink);
	}

	.btn-export {
		background: white;
		border: 2.5px solid var(--ink);
		border-radius: 50px;
		font-weight: 700;
		padding: 8px 20px;
		box-shadow: 4px 4px 0 var(--ink);
		transition: all 0.2s;
	}

	.btn-export:hover {
		background: var(--mustard);
		transform: translateY(-2px);
	}

	.table-ink {
		background: var(--ink);
	}

	.table-ink th {
		font-family: var(--font-display);
		font-weight: 700;
		font-size: 0.8rem;
		letter-spacing: 1px;
		border: none;
		padding: 15px;
	}

	.log-row:hover {
		background-color: rgba(245, 183, 49, 0.05);
	}

	.user-avatar-small {
		width: 32px;
		height: 32px;
		background: var(--mustard);
		border: 2px solid var(--ink);
		border-radius: 8px;
		display: flex;
		align-items: center;
		justify-content: center;
		font-weight: 900;
		font-size: 0.8rem;
	}

	.badge-cartoon {
		padding: 4px 12px;
		border-radius: 8px;
		font-size: 0.75rem;
		font-weight: 800;
		border: 2px solid var(--ink);
		display: inline-flex;
		align-items: center;
	}

	.badge-create {
		background: #c8e6c9;
		color: #2e7d32;
	}
	.badge-update {
		background: #bbdefb;
		color: #1565c0;
	}
	.badge-delete {
		background: #ffcdd2;
		color: #c62828;
	}
	.badge-login {
		background: #e1bee7;
		color: #6a1b9a;
	}
	.badge-failed {
		background: #fff9c4;
		color: #f9a825;
	}

	.btn-detail-circle {
		width: 35px;
		height: 35px;
		border-radius: 50%;
		border: 2px solid var(--ink);
		background: white;
		display: inline-flex;
		align-items: center;
		justify-content: center;
		transition: all 0.2s;
	}

	.btn-detail-circle:hover {
		background: var(--mustard);
		transform: scale(1.1);
	}

	.cartoon-modal {
		border: 4px solid var(--ink);
		border-radius: 30px;
		box-shadow: 10px 10px 0 var(--ink);
	}

	.detail-item {
		background: #f8f9fa;
		border: 2px solid #eee;
	}

	.changes-pre {
		background: #222;
		color: #00ff00;
		padding: 15px;
		border-radius: 10px;
		max-height: 300px;
		overflow-y: auto;
		font-size: 0.8rem;
	}

	.btn-ink {
		background: var(--ink);
		color: white;
	}

	.x-small {
		font-size: 0.7rem;
	}
	.opacity-20 {
		opacity: 0.2;
	}

	.pagination-card {
		border: 3px solid var(--ink);
		border-radius: 20px;
		box-shadow: 6px 6px 0 var(--ink);
	}

	.btn-outline-ink {
		border: 2.5px solid var(--ink);
		color: var(--ink);
		background: white;
		font-weight: 700;
		transition: all 0.2s;
	}

	.btn-outline-ink:hover:not(:disabled) {
		background: var(--mustard);
		transform: translateY(-2px);
		box-shadow: 3px 3px 0 var(--ink);
	}

	.btn-outline-ink:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.search-box .cartoon-input {
		box-shadow: 3px 3px 0 var(--ink);
	}

	.filter-card .btn:focus {
		outline: none;
		box-shadow: 0 0 0 3px rgba(78, 67, 54, 0.25);
	}
</style>
