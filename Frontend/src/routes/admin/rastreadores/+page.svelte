<script>
	import AdminNavbar from '$lib/components/AdminNavbar.svelte';

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
</script>

<AdminNavbar />

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
