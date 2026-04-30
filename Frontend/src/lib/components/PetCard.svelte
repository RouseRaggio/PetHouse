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

	const statusBadgeMap = {
		'AVAILABLE': 'bg-success',
		'ADOPTED': 'bg-secondary',
		'RESERVED': 'bg-warning text-dark',
		'UNAVAILABLE': 'bg-danger'
	};
	$: statusBadgeClass = statusBadgeMap[pet.status] || 'bg-light text-dark';
</script>

<div class="card pet-card border-0 shadow-sm h-100 overflow-hidden" on:click={() => dispatch('view')}>
	<div class="position-relative">
		<img 
			src={pet.image_url || 'https://via.placeholder.com/300x200?text=Sin+imagen'} 
			class="card-img-top pet-img" 
			alt={pet.name} 
		/>
		<span class="badge {statusBadgeClass} position-absolute top-0 start-0 m-3 shadow-sm px-3 py-2 rounded-pill">
			{statusText}
		</span>
		
		{#if pet.gender}
			<span class="gender-badge position-absolute top-0 end-0 m-3 {pet.gender === 'macho' ? 'male' : 'female'}">
				<i class="bi {pet.gender === 'macho' ? 'bi-gender-male' : 'bi-gender-female'}"></i>
			</span>
		{/if}
	</div>

	<div class="card-body p-4">
		<div class="d-flex justify-content-between align-items-start mb-2">
			<h4 class="fw-bold text-dark mb-0">{pet.name}</h4>
			<span class="text-primary small fw-bold text-uppercase ls-1">{pet.species}</span>
		</div>
		
		<p class="text-muted small mb-3">
			<i class="bi bi-clock me-1"></i> {ageText}
			{#if pet.race}
				<span class="mx-1">•</span> <i class="bi bi-tag me-1"></i> {pet.race}
			{/if}
		</p>

		<button class="btn btn-primary w-100 rounded-pill py-2 fw-bold shadow-sm">
			Ver Perfil
		</button>
	</div>
</div>

<style>
	.pet-card {
		cursor: pointer;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		border-radius: 24px;
	}

	.pet-img {
		height: 250px;
		object-fit: cover;
		transition: transform 0.5s ease;
	}

	.pet-card:hover {
		transform: translateY(-10px);
		box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12) !important;
	}

	.pet-card:hover .pet-img {
		transform: scale(1.05);
	}

	.ls-1 {
		letter-spacing: 1px;
	}

	.gender-badge {
		width: 35px;
		height: 35px;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 50%;
		background: rgba(255, 255, 255, 0.9);
		backdrop-filter: blur(4px);
		font-size: 1.2rem;
		box-shadow: 0 4px 10px rgba(0,0,0,0.1);
	}

	.gender-badge.male { color: #0d6efd; }
	.gender-badge.female { color: #d63384; }

	.btn-primary {
		background: #4361ee;
		border: none;
		transition: all 0.3s ease;
	}
	.btn-primary:hover {
		background: #3046bc;
		transform: scale(1.02);
	}
</style>
