<script>
	import { onMount } from 'svelte';
	import { getUsers, createUser, updateUser, deleteUser } from '../../api/user_service.js';
	import PowerBI from '$lib/components/PowerBIReport.svelte';
	import AdminNavbar from '$lib/components/AdminNavbar.svelte';

	let users = [];
	let editUserId = null;

	let newUser = {
		name: '',
		last_name: '',
		email: '',
		password: '',
		role: 'Usuario',
		status: 'Activo'
	};

	// Cargar usuarios
	onMount(async () => {
		try {
			users = await getUsers();
		} catch (error) {
			console.error('Error cargando usuarios:', error);
		}
	});

	// Crear usuario
	async function addUser() {
		const userData = {
			name: newUser.name,
			last_name: newUser.last_name,
			email: newUser.email,
			password: newUser.password,
			role_id: newUser.role === 'Admin' ? 1 : 2
		};

		console.log('Enviando:', userData);

		try {
			const created = await createUser(userData);

			users = [...users, created];

			resetForm();
		} catch (error) {
			console.error('Error creando usuario:', error);
			alert('Error creando usuario');
		}
	}

	// Eliminar usuario
	async function removeUser(id) {
		if (!confirm('¿Eliminar usuario?')) return;

		try {
			await deleteUser(id);

			users = users.filter((u) => u.id !== id);
		} catch (error) {
			console.error('Error eliminando usuario:', error);
		}
	}

	// Iniciar edición
	function startEdit(user) {
		editUserId = user.id;

		newUser = {
			name: user.name,
			last_name: user.last_name,
			email: user.email,
			password: user.password,
			role: user.role ?? 'Usuario',
			status: user.status ?? 'Activo'
		};
	}

	// Guardar edición
	async function saveEdit() {
		const userData = {
			name: newUser.name,
			last_name: newUser.last_name,
			email: newUser.email,
			password: newUser.password,
			role_id: newUser.role === 'Admin' ? 1 : 2
		};

		if (newUser.password && newUser.password.length > 0) {
			userData.password = newUser.password;
		}

		try {
			const updated = await updateUser(editUserId, userData);

			users = await getUsers();

			resetForm();
			editUserId = null;
		} catch (error) {
			console.error('Error actualizando usuario:', error);
		}
	}

	function cancelEdit() {
		editUserId = null;

		resetForm();
	}

	function resetForm() {
		newUser = {
			name: '',
			last_name: '',
			email: '',
			password: '',
			role: 'Usuario',
			status: 'Activo'
		};
	}
</script>

<AdminNavbar />

<section class="container my-4">
	<h2 class="mb-4">Gestión de Usuarios</h2>

	<!-- Formulario -->
	<div class="card mb-4 p-3">
		<h5>{editUserId ? 'Editar Usuario' : 'Agregar Usuario'}</h5>

		<div class="row g-2">
			<div class="col-md-2">
				<input class="form-control" placeholder="Nombre" bind:value={newUser.name} />
			</div>

			<div class="col-md-2">
				<input class="form-control" placeholder="Apellido" bind:value={newUser.last_name} />
			</div>

			<div class="col-md-3">
				<input class="form-control" type="email" placeholder="Correo" bind:value={newUser.email} />
			</div>

			<div class="col-md-2">
				<input
					class="form-control"
					type="password"
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
		</div>

		<div class="mt-3">
			{#if editUserId}
				<button class="btn btn-success me-2" on:click={saveEdit}> Guardar </button>

				<button class="btn btn-secondary" on:click={cancelEdit}> Cancelar </button>
			{:else}
				<button
					class="btn btn-primary"
					on:click={addUser}
					disabled={!newUser.name || !newUser.last_name || !newUser.email || !newUser.password}
				>
					Agregar Usuario
				</button>
			{/if}
		</div>
	</div>

	<!-- Tabla -->
	<table class="table table-striped table-hover">
		<thead class="table-dark">
			<tr>
				<th>Nombre</th>
				<th>Apellido</th>
				<th>Correo</th>
				<th>Rol</th>
				<th>Acciones</th>
			</tr>
		</thead>

		<tbody>
			{#each users as u (u.id)}
				<tr>
					<td>{u.name}</td>
					<td>{u.last_name}</td>
					<td>{u.email}</td>
					<td>{u.role ?? 'Usuario'}</td>

					<td>
						<button class="btn btn-sm btn-warning me-1" on:click={() => startEdit(u)}>
							Editar
						</button>

						<button class="btn btn-sm btn-danger" on:click={() => removeUser(u.id)}>
							Eliminar
						</button>
					</td>
				</tr>
			{/each}
		</tbody>
	</table>
</section>
