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

	const statusColorMap = {
		'AVAILABLE': 'status-available',
		'ADOPTED': 'status-adopted',
		'RESERVED': 'status-reserved',
		'UNAVAILABLE': 'status-unavailable'
	};
	$: statusColorClass = statusColorMap[pet.status] || 'status-adopted';

	// Emoji por especie
	const speciesEmoji = {
		'perro': '🐕',
		'gato': '🐱',
		'conejo': '🐰',
		'ave': '🐦',
		'hamster': '🐹',
		'tortuga': '🐢',
		'pez': '🐟',
	};
	$: emoji = speciesEmoji[pet.species?.toLowerCase()] || '🐾';
</script>

<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div class="pet-card-cartoon" on:click={() => dispatch('view')}>
	<div class="card-image-wrap">
		<img 
			src={pet.image_url || 'https://via.placeholder.com/300x200?text=Sin+imagen'} 
			class="card-img" 
			alt={pet.name} 
		/>
		<span class="status-tag {statusColorClass}">
			{statusText}
		</span>
		
		{#if pet.gender}
			<span class="gender-tag {pet.gender === 'macho' ? 'male' : 'female'}">
				{pet.gender === 'macho' ? '♂' : '♀'}
			</span>
		{/if}

		<span class="species-emoji">{emoji}</span>
	</div>

	<div class="card-content">
		<h4 class="pet-name">{pet.name}</h4>
		
		<div class="pet-details">
			<span class="detail-chip">
				<i class="bi bi-clock"></i> {ageText}
			</span>
			{#if pet.race}
				<span class="detail-chip">
					<i class="bi bi-tag"></i> {pet.race}
				</span>
			{/if}
		</div>

		<button class="btn-view-profile">
			Ver Perfil 🐾
		</button>
	</div>
</div>

<style>
	.pet-card-cartoon {
		cursor: pointer;
		background: white;
		border: 3px solid var(--ink);
		border-radius: 20px;
		overflow: hidden;
		box-shadow: 4px 4px 0px var(--ink);
		transition: all 0.35s cubic-bezier(0.68, -0.55, 0.265, 1.55);
		height: 100%;
		display: flex;
		flex-direction: column;
	}

	.pet-card-cartoon:hover {
		transform: translateY(-8px) rotate(-1deg);
		box-shadow: 7px 7px 0px var(--ink);
	}

	.pet-card-cartoon:active {
		transform: translateY(-2px) rotate(0deg);
		box-shadow: 2px 2px 0px var(--ink);
	}

	/* Image area */
	.card-image-wrap {
		position: relative;
		overflow: hidden;
		aspect-ratio: 4 / 3;
	}

	.card-img {
		width: 100%;
		height: 100%;
		object-fit: cover;
		transition: transform 0.5s ease;
		border-bottom: 3px solid var(--ink);
		display: block;
	}

	.pet-card-cartoon:hover .card-img {
		transform: scale(1.08);
	}

	/* Status tag */
	.status-tag {
		position: absolute;
		top: 12px;
		left: 12px;
		padding: 4px 14px;
		border-radius: 50px;
		font-size: 0.75rem;
		font-weight: 800;
		font-family: var(--font-display);
		border: 2.5px solid var(--ink);
		box-shadow: 2px 2px 0 var(--ink);
		letter-spacing: 0.3px;
	}

	.status-available {
		background: #B8F0B0;
		color: #1B5E20;
	}
	.status-adopted {
		background: var(--light-gray);
		color: var(--warm-gray);
	}
	.status-reserved {
		background: #FFE082;
		color: #6D4C00;
	}
	.status-unavailable {
		background: #FFAB91;
		color: #B71C1C;
	}

	/* Gender badge */
	.gender-tag {
		position: absolute;
		top: 12px;
		right: 12px;
		width: 32px;
		height: 32px;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 50%;
		border: 2.5px solid var(--ink);
		font-size: 1rem;
		font-weight: bold;
		box-shadow: 2px 2px 0 var(--ink);
		background: white;
	}

	.gender-tag.male { color: #2196F3; }
	.gender-tag.female { color: #E91E63; }

	/* Species emoji float */
	.species-emoji {
		position: absolute;
		bottom: -16px;
		right: 16px;
		font-size: 2rem;
		background: var(--mustard);
		width: 42px;
		height: 42px;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 50%;
		border: 2.5px solid var(--ink);
		box-shadow: 2px 2px 0 var(--ink);
		z-index: 2;
		transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
	}

	.pet-card-cartoon:hover .species-emoji {
		transform: scale(1.15) rotate(-10deg);
	}

	/* Card content */
	.card-content {
		padding: 1.2rem 1.2rem 1rem;
		display: flex;
		flex-direction: column;
		flex: 1;
	}

	.pet-name {
		font-family: var(--font-display);
		font-size: 1.3rem;
		font-weight: 800;
		color: var(--ink);
		margin: 0 0 0.5rem 0;
	}

	.pet-details {
		display: flex;
		flex-wrap: wrap;
		gap: 6px;
		margin-bottom: 0.8rem;
	}

	.detail-chip {
		font-size: 0.78rem;
		font-weight: 600;
		color: var(--warm-gray);
		background: var(--cream-dark);
		padding: 3px 10px;
		border-radius: 50px;
		border: 1.5px solid var(--light-gray);
		font-family: var(--font-body);
	}

	.detail-chip i {
		margin-right: 2px;
	}

	/* View profile button */
	.btn-view-profile {
		margin-top: auto;
		width: 100%;
		padding: 10px;
		background: var(--teal);
		color: white;
		border: 2.5px solid var(--ink);
		border-radius: 50px;
		font-family: var(--font-display);
		font-weight: 700;
		font-size: 0.95rem;
		cursor: pointer;
		box-shadow: 3px 3px 0 var(--ink);
		transition: all 0.25s cubic-bezier(0.68, -0.55, 0.265, 1.55);
	}

	.btn-view-profile:hover {
		background: var(--coral);
		transform: translateY(-3px);
		box-shadow: 4px 4px 0 var(--ink);
	}

	.btn-view-profile:active {
		transform: translateY(1px);
		box-shadow: 1px 1px 0 var(--ink);
	}
</style>
