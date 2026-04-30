<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import 'bootstrap/dist/css/bootstrap.min.css';
	import '../app.css';

	onMount(async () => {
		// Importar JS de bootstrap solo en el cliente
		try {
			await import('bootstrap/dist/js/bootstrap.bundle.min.js');
		} catch (e) {
			console.error('Error loading Bootstrap JS:', e);
		}
	});
</script>

<slot />
