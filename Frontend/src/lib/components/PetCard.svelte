<script>
	import { createEventDispatcher } from 'svelte';
	import '../../app.css';
	import { formatAge } from '$lib/utils/formatAge.js';
	export let pet;
	const dispatch = createEventDispatcher();

	// Calcular edad aproximada
	$: ageText = formatAge(pet.birth_date);

	// Traducir status
	const statusMap = {
		'AVAILABLE': 'Disponible',
		'ADOPTED': 'Adoptado',
		'RESERVED': 'Reservado',
		'UNAVAILABLE': 'No disponible'
	};
	$: statusText = statusMap[pet.status] || pet.status;
	// Clases de color para el status
	const statusColorMap = {
		'AVAILABLE': 'text-success',
		'ADOPTED': 'text-secondary',
		'RESERVED': 'text-warning',
		'UNAVAILABLE': 'text-danger'
	};
	$: statusColorClass = statusColorMap[pet.status] || 'text-muted';
</script>

<div class="card shadow-sm h-100 small-card">
	<img src={pet.image_url || 'https://via.placeholder.com/300x200?text=Sin+imagen'} class="card-img-top" alt={pet.name} />

	<div class="card-body text-center">
		<h5 class="fw-bold">{pet.name}</h5>
		<p class="text-muted">{pet.species} - {ageText}</p>
		<p class="{statusColorClass} small fw-bold">{statusText}</p>

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
