<script>
	import { fade, scale } from 'svelte/transition';
	import { createEventDispatcher, onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { formatAge } from '$lib/utils/formatAge.js';

	export let selectedPet;

	$: ageText = formatAge(selectedPet.birth_date);

	$: notAvailable = selectedPet.status !== 'AVAILABLE';

	const statusMap = {
		AVAILABLE: 'Disponible',
		ADOPTED: 'Adoptado',
		RESERVED: 'Reservado',
		UNAVAILABLE: 'No disponible'
	};
	$: statusText = statusMap[selectedPet.status] || selectedPet.status;

	const statusClassMap = {
		AVAILABLE: 'disponible',
		ADOPTED: 'adoptado',
		RESERVED: 'reservado',
		UNAVAILABLE: 'no-disponible'
	};
	$: statusClass = statusClassMap[selectedPet.status] || 'adoptado';

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
	$: emoji = speciesEmoji[selectedPet.species?.toLowerCase()] || '🐾';

	const dispatch = createEventDispatcher();

	function close() {
		dispatch('close');
	}

	function handleKey(e) {
		if (e.key === 'Escape') close();
	}

	function handleAdopt() {
		localStorage.setItem('selectedPet', JSON.stringify(selectedPet));
		goto(`/usuarios/adoptar?pet_id=${selectedPet.id}`);
		setTimeout(() => close(), 50);
	}

	onMount(() => {
		window.addEventListener('keydown', handleKey);
		return () => window.removeEventListener('keydown', handleKey);
	});
</script>

<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div class="modal-overlay" on:click={close} in:fade>
	<div
		class="modal-card-cartoon"
		on:click|stopPropagation
		in:scale={{ duration: 280, start: 0.85 }}
		out:scale={{ duration: 180 }}
	>
		<button class="close-btn-cartoon" on:click={close}>✕</button>

		<div class="modal-body-cartoon">
			<div class="modal-image-side">
				<img
					src={selectedPet.image_url || 'https://via.placeholder.com/400x300?text=Sin+imagen'}
					alt={selectedPet.name}
				/>
				<span class="modal-species-emoji">{emoji}</span>
			</div>

			<div class="modal-info-side">
				<h3 class="modal-pet-name">{selectedPet.name}</h3>

				<div class="status-badge {statusClass}">
					{statusText}
				</div>

				<div class="info-grid">
					<div class="info-row">
						<span class="info-label">🎂 Edad</span>
						<span class="info-value">{ageText}</span>
					</div>
					<div class="info-row">
						<span class="info-label">{selectedPet.gender === 'macho' ? '♂️' : '♀️'} Sexo</span>
						<span class="info-value">{selectedPet.gender}</span>
					</div>
					<div class="info-row">
						<span class="info-label">🏷️ Raza</span>
						<span class="info-value">{selectedPet.race}</span>
					</div>
				</div>

				{#if selectedPet.description}
					<div class="description-box">
						<span class="desc-label">📖 Sobre {selectedPet.name}</span>
						<p>{selectedPet.description}</p>
					</div>
				{/if}

				<button class="btn-adopt-cartoon" disabled={notAvailable} on:click={handleAdopt}>
					{notAvailable ? `Estado: ${statusText}` : '¡Quiero Adoptar! 🐾'}
				</button>
			</div>
		</div>
	</div>
</div>

<style>
	.modal-card-cartoon {
		background: var(--cream);
		border-radius: 24px;
		border: 3px solid var(--ink);
		width: 100%;
		max-width: 860px;
		max-height: 90vh;
		overflow: hidden;
		box-shadow: 8px 8px 0px var(--ink);
		position: relative;
		animation: bounceIn 0.35s cubic-bezier(0.68, -0.55, 0.265, 1.55);
	}

	@keyframes bounceIn {
		0% { transform: scale(0.8) rotate(-3deg); opacity: 0; }
		60% { transform: scale(1.03) rotate(1deg); }
		100% { transform: scale(1) rotate(0deg); opacity: 1; }
	}

	.modal-body-cartoon {
		display: flex;
	}

	/* Image side */
	.modal-image-side {
		flex: 1;
		position: relative;
		overflow: hidden;
	}

	.modal-image-side img {
		width: 100%;
		height: 100%;
		object-fit: cover;
		transition: transform 0.5s ease;
		border-right: 3px solid var(--ink);
	}

	.modal-image-side:hover img {
		transform: scale(1.05);
	}

	.modal-species-emoji {
		position: absolute;
		bottom: 16px;
		left: 16px;
		font-size: 2.2rem;
		background: var(--mustard);
		width: 52px;
		height: 52px;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 50%;
		border: 3px solid var(--ink);
		box-shadow: 3px 3px 0 var(--ink);
		animation: float 3s ease-in-out infinite;
	}

	@keyframes float {
		0%, 100% { transform: translateY(0); }
		50% { transform: translateY(-6px); }
	}

	/* Info side */
	.modal-info-side {
		flex: 1;
		padding: 2rem;
		display: flex;
		flex-direction: column;
		overflow-y: auto;
	}

	.modal-pet-name {
		font-family: var(--font-display);
		font-size: 2rem;
		font-weight: 800;
		color: var(--ink);
		margin: 0 0 0.6rem 0;
	}

	/* Info grid */
	.info-grid {
		display: flex;
		flex-direction: column;
		gap: 8px;
		margin-bottom: 1rem;
	}

	.info-row {
		display: flex;
		align-items: center;
		gap: 10px;
		padding: 8px 14px;
		background: white;
		border: 2px solid var(--light-gray);
		border-radius: 14px;
		transition: all 0.2s ease;
	}

	.info-row:hover {
		border-color: var(--teal);
		transform: translateX(4px);
	}

	.info-label {
		font-family: var(--font-display);
		font-weight: 700;
		font-size: 0.85rem;
		color: var(--warm-gray);
		min-width: 80px;
	}

	.info-value {
		font-family: var(--font-body);
		font-weight: 600;
		color: var(--ink);
		font-size: 0.95rem;
	}

	/* Description */
	.description-box {
		background: white;
		border: 2px dashed var(--teal);
		border-radius: 16px;
		padding: 1rem;
		margin-bottom: 1rem;
	}

	.desc-label {
		font-family: var(--font-display);
		font-weight: 700;
		font-size: 0.9rem;
		color: var(--teal);
		display: block;
		margin-bottom: 6px;
	}

	.description-box p {
		margin: 0;
		font-size: 0.9rem;
		color: var(--warm-gray);
		line-height: 1.6;
	}

	/* Close button */
	.close-btn-cartoon {
		position: absolute;
		top: 14px;
		right: 16px;
		z-index: 10;
		background: var(--coral);
		border: 2.5px solid var(--ink);
		width: 40px;
		height: 40px;
		border-radius: 50%;
		font-size: 1.1rem;
		cursor: pointer;
		color: white;
		font-weight: bold;
		display: flex;
		align-items: center;
		justify-content: center;
		box-shadow: 3px 3px 0 var(--ink);
		transition: all 0.25s cubic-bezier(0.68, -0.55, 0.265, 1.55);
	}

	.close-btn-cartoon:hover {
		background: var(--coral-dark);
		transform: rotate(90deg) scale(1.15);
		box-shadow: 4px 4px 0 var(--ink);
	}

	/* Adopt button */
	.btn-adopt-cartoon {
		margin-top: auto;
		padding: 14px 1.5rem;
		background: var(--teal);
		color: white;
		border: 3px solid var(--ink);
		border-radius: 50px;
		font-weight: 800;
		font-family: var(--font-display);
		font-size: 1.1rem;
		cursor: pointer;
		transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
		box-shadow: 4px 4px 0 var(--ink);
		letter-spacing: 0.5px;
		text-align: center;
	}

	.btn-adopt-cartoon:hover {
		transform: translateY(-4px) rotate(-1deg);
		box-shadow: 6px 6px 0 var(--ink);
		background: var(--teal-dark);
	}

	.btn-adopt-cartoon:active {
		transform: translateY(1px);
		box-shadow: 1px 1px 0 var(--ink);
	}

	.btn-adopt-cartoon:disabled {
		background: var(--light-gray);
		color: var(--warm-gray);
		cursor: not-allowed;
		transform: none;
		box-shadow: 3px 3px 0 var(--ink);
	}

	@media (max-width: 768px) {
		.modal-body-cartoon {
			flex-direction: column;
		}

		.modal-image-side {
			height: 250px;
		}

		.modal-image-side img {
			border-right: none;
			border-bottom: 3px solid var(--ink);
		}

		.modal-info-side {
			padding: 1.5rem;
		}

		.modal-pet-name {
			font-size: 1.6rem;
		}
	}
</style>
