<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import 'bootstrap/dist/css/bootstrap.min.css';
	import '../app.css';

	const routeTitles = {
		'/login': 'PetHouse Iniciar sesión',
		'/usuarios/mascotas': 'PetHouse Mascotas disponibles',
		'/usuarios/publicar': 'PetHouse Publicar mascota',
		'/usuarios/adoptar': 'PetHouse Adoptar mascota',
		'/admin': 'Panel Admin',
		'/admin/dashboard': 'Dashboard',
		'/admin/mascotas': 'Gestión de mascotas',
		'/admin/adopcion': 'Adopciones',
		'/admin/historial': 'Historial de auditoría'
	};

	const routeDescriptions = {
		'/': 'Adopta una mascota, encuentra tu compañero ideal y descubre el hogar perfecto en PetHouse.',
		'/login': 'Inicia sesión en PetHouse para adoptar o publicar mascotas.',
		'/usuarios/mascotas': 'Explora mascotas disponibles para adopción en PetHouse.',
		'/usuarios/publicar': 'Publica una mascota en adopción y encuentra un hogar amoroso.',
		'/usuarios/adoptar': 'Revisa los requisitos y adopta a tu nueva mascota.',
		'/admin': 'Accede al panel administrativo de PetHouse.',
		'/admin/dashboard': 'Consulta el panel de control y métricas de PetHouse.',
		'/admin/mascotas': 'Administra el catálogo de mascotas de PetHouse.',
		'/admin/adopcion': 'Gestiona las solicitudes de adopción.',
		'/admin/historial': 'Revisa el historial de auditoría de PetHouse.'
	};

	$: title = routeTitles[$page.url.pathname] || 'PetHouse';
	$: description = routeDescriptions[$page.url.pathname] || 'PetHouse - Encuentra tu mejor amigo.';

	onMount(async () => {
		// Importar JS de bootstrap solo en el cliente
		try {
			await import('bootstrap/dist/js/bootstrap.bundle.min.js');
		} catch (e) {
			console.error('Error loading Bootstrap JS:', e);
		}
	});
</script>

<svelte:head>
	<title>{title}</title>
	<meta name="description" content={description} />
</svelte:head>

<slot />
