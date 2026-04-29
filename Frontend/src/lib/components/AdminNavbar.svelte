<script>
	import { goto } from '$app/navigation';
	import { clearAuth } from '$lib/stores/auth.js';

	function logout() {
		clearAuth();
		goto('/login');
	}
</script>

<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
	<div class="container-fluid">
		<a class="navbar-brand" href="/admin">Admin PetHouse</a>

		<div class="collapse navbar-collapse">
			<ul class="navbar-nav me-auto">
				<li class="nav-item">
					<a class="nav-link active" href="/admin">Usuarios</a>
				</li>
				<li class="nav-item">
					<a class="nav-link active" href="/admin/dashboard">Dashboard</a>
				</li>
				<li class="nav-item">
					<a class="nav-link" href="/admin/rastreadores">Rastreadores</a>
				</li>
				<li class="nav-item">
					<a class="nav-link" href="/admin/adopcion">Adopción</a>
				</li>
			</ul>
			<button class="btn btn-outline-light btn-sm" on:click={logout}>Cerrar sesión</button>
		</div>
	</div>
</nav>
