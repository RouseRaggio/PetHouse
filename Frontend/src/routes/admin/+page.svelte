<script>
	import { fade } from 'svelte/transition';
	import PowerBI from '$lib/components/PowerBIReport.svelte';
	// Datos simulados
	export let users = [
		{ id: 1, name: 'Juan Perez', email: 'juan@example.com', role: 'Admin', status: 'Activo' },
		{ id: 2, name: 'Maria Gomez', email: 'maria@example.com', role: 'Usuario', status: 'Inactivo' }
	];

	let newUser = {
		name: '',
		apellido: '',
		email: '',
		password: '',
		role: 'Usuario',
		status: 'Activo'
	};
	let editUserId = null;

	function addUser() {
		if (!newUser.name.trim() || !newUser.email.trim() || !newUser.password?.trim()) {
			alert('Debes llenar todos los campos obligatorios');
			return;
		}

		const id = users.length ? Math.max(...users.map((u) => u.id)) + 1 : 1;

		users = [...users, { ...newUser, id }];

		newUser = {
			name: '',
			email: '',
			apellido: '',
			password: '',
			role: 'Usuario',
			status: 'Activo'
		};
	}

	function deleteUser(id) {
		users = users.filter((u) => u.id !== id);
	}

	function startEdit(user) {
		editUserId = user.id;
		newUser = { ...user };
	}

	function saveEdit() {
		users = users.map((u) => (u.id === editUserId ? { ...newUser, id: editUserId } : u));
		editUserId = null;
		newUser = { name: '', email: '', role: 'Usuario', status: 'Activo' };
	}

	function cancelEdit() {
		editUserId = null;
		newUser = { name: '', email: '', role: 'Usuario', status: 'Activo' };
	}
</script>

<!-- Navbar Admin -->
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
	<div class="container-fluid">
		<a class="navbar-brand" href="/admin">Admin PetHouse</a>
		<button
			class="navbar-toggler"
			type="button"
			data-bs-toggle="collapse"
			data-bs-target="#adminNav"
			aria-controls="adminNav"
			aria-expanded="false"
			aria-label="Toggle navigation"
		>
			<span class="navbar-toggler-icon"></span>
		</button>
		<div class="collapse navbar-collapse" id="adminNav">
			<ul class="navbar-nav me-auto mb-2 mb-lg-0">
				<!-- <li class="nav-item"><a class="nav-link" href="/admin/mascotas">Mascotas</a></li> -->
				<li class="nav-item"><a class="nav-link active" href="/admin">Usuarios</a></li>
				<li class="nav-item"><a class="nav-link" href="../">Inicio</a></li>
			</ul>
		</div>
	</div>
</nav>

<section class="container my-4">
	<h2 class="mb-4">Gestión de Usuarios</h2>

	<!-- Formulario agregar/editar -->
	<div class="card mb-4 p-3">
		<h5>{editUserId ? 'Editar Usuario' : 'Agregar Nuevo Usuario'}</h5>
		<div class="row g-2">
			<div class="col-md-2">
				<input
					type="text"
					class="form-control"
					placeholder="Nombre"
					bind:value={newUser.name}
					required
				/>
			</div>
			<div class="col-md-2">
				<input
					type="text"
					class="form-control"
					placeholder="Apellido"
					bind:value={newUser.apellido}
				/>
			</div>
			<div class="col-md-3">
				<input
					type="email"
					class="form-control"
					placeholder="Correo"
					bind:value={newUser.email}
					required
				/>
			</div>

			<div class="col-md-2">
				<input
					type="password"
					class="form-control"
					placeholder="Contraseña"
					bind:value={newUser.password}
				/>
			</div>
			<div class="col-md-2">
				<select class="form-select" bind:value={newUser.role}>
					<option>Admin</option>
					<option>Usuario</option>
				</select>
			</div>
			<div class="col-md-1">
				<select class="form-select" bind:value={newUser.status}>
					<option>Activo</option>
					<option>Inactivo</option>
				</select>
			</div>
		</div>
		<div class="mt-2">
			{#if editUserId}
				<button class="btn btn-success me-2" on:click={saveEdit}>Guardar</button>
				<button class="btn btn-secondary" on:click={cancelEdit}>Cancelar</button>
			{:else}
				<button
					class="btn btn-primary"
					on:click={addUser}
					disabled={!newUser.name || !newUser.email || !newUser.password}
				>
					Agregar Usuario
				</button>
			{/if}
		</div>
	</div>

	<!-- Tabla de usuarios -->
	<table class="table table-striped table-hover">
		<thead class="table-dark">
			<tr>
				<th>Nombre</th>
				<th>Apellido</th>
				<th>Correo</th>
				<th>Contraseña</th>
				<th>Rol</th>
				<th>Estado</th>
				<th>Acciones</th>
			</tr>
		</thead>
		<tbody>
			{#each users as u (u.id)}
				<tr>
					<td>{u.name}</td>
					<td>{u.apellido}</td>
					<td>{u.email}</td>
					<td>{u.password}</td>
					<td>{u.role}</td>
					<td>{u.status}</td>
					<td>
						<button class="btn btn-sm btn-warning me-1" on:click={() => startEdit(u)}>Editar</button
						>
						<button class="btn btn-sm btn-danger" on:click={() => deleteUser(u.id)}>Eliminar</button
						>
					</td>
				</tr>
			{/each}
		</tbody>
	</table>

	<section class="container">
		<PowerBI
			title="Reporte"
			src="https://app.powerbi.com/view?r=eyJrIjoiZjU0ZWNhMjEtYjIyMy00MTllLTlmZmYtOTNhZjI0ZjA4MjY0IiwidCI6IjFlOWFhYmU4LTY3ZjgtNGYxYy1hMzI5LWE3NTRlOTI0OTlhZSIsImMiOjR9"
			height="600px"
			width="100%"
		/>
	</section>
</section>

<style>
</style>
