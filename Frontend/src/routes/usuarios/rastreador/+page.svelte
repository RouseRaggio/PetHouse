<script>
	import Navbar from '$lib/components/Navbar.svelte';

	// Datos simulados
	let trackers = [
		{ id: 1, name: 'Collar Fido', type: 'GPS', status: 'Activo', location: 'Barranquilla' },
		{ id: 2, name: 'Collar Mimi', type: 'GPS', status: 'Activo', location: 'Cartagena' }
	];
</script>

<section class="container my-4">
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

	<div class="card mt-5 p-3">
		<h5>Ubicación en Mapa</h5>
		<!-- svelte-ignore a11y_missing_attribute -->
		<div
			class="map-placeholder d-flex align-items-center justify-content-center"
			style="height: 300px; background-color: #e9ecef;"
		>
			<span
				class="text-muted
        ">Aquí se mostrará un mapa con la ubicación de los rastreadores</span
			>
		</div>
	</div>
</section>
