<script>
	import { createEventDispatcher } from 'svelte';
	import '../../app.css';
	export let pet;
	const dispatch = createEventDispatcher();

	// Calcular edad aproximada en años
	$: age = pet.birth_date ? Math.floor((new Date() - new Date(pet.birth_date)) / (365.25 * 24 * 60 * 60 * 1000)) : 'Desconocida';

	// Traducir status
	$: statusText = pet.status === 'AVAILABLE' ? 'Disponible' : pet.status;
</script>

<div class="card shadow-sm h-100 small-card">
	<img src={pet.image_url || 'https://via.placeholder.com/300x200?text=Sin+imagen'} class="card-img-top" alt={pet.name} />

	<div class="card-body text-center">
		<h5 class="fw-bold">{pet.name}</h5>
		<p class="text-muted">{pet.species} - {age} años</p>
		<p class="text-success small">{statusText}</p>

		<button class="btn btn-outline-primary btn-sm" on:click={() => dispatch('view')}>
			Ver detalles
		</button>
	</div>
</div>

<style>
	.small-card img {
		height: 200px;
		object-fit: cover;
	}

	.small-card .card-body {
		padding: 0.8rem;
	}

	.card {
		transition:
			transform 0.3s ease,
			box-shadow 0.3s ease;
	}

	.card:hover {
		transform: translateY(-8px);
		box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
	}
</style>
