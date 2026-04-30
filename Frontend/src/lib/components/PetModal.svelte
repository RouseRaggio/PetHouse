<script>
	import { fade, scale } from 'svelte/transition';
	import { createEventDispatcher, onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { formatAge } from '$lib/utils/formatAge.js'; 	

	export let selectedPet;

	$: ageText = formatAge(selectedPet.birth_date);

	$: notAvailable = selectedPet.status !== 'AVAILABLE';

	const statusMap = {
		'AVAILABLE': 'Disponible',
		'ADOPTED': 'Adoptado',
		'RESERVED': 'Reservado',
		'UNAVAILABLE': 'No disponible'
	};
	$: statusText = statusMap[selectedPet.status] || selectedPet.status;
	
	const statusClassMap = {
		'AVAILABLE': 'disponible',
		'ADOPTED': 'adoptado',
		'RESERVED': 'reservado',
		'UNAVAILABLE': 'no-disponible'
	};
	$: statusClass = statusClassMap[selectedPet.status] || 'adoptado';

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
		class="modal-card"
		on:click|stopPropagation
		in:scale={{ duration: 220, start: 0.9 }}
		out:scale={{ duration: 150 }}
	>
		<button class="close-btn" on:click={close}>×</button>

		<div class="modal-body">
			<div class="image-container">
				<img src={selectedPet.image_url || 'https://via.placeholder.com/400x300?text=Sin+imagen'} alt={selectedPet.name} />
			</div>

			<div class="info-container">
				<h3>{selectedPet.name}</h3>

				<div class="status-badge {statusClass}">
					{statusText}
				</div>

				<p><strong>Edad:</strong> {ageText}</p>
				<p><strong>Sexo:</strong> {selectedPet.gender}</p>
				<p><strong>Raza:</strong> {selectedPet.race}</p>
				<p><strong>Descripción:</strong> {selectedPet.description}</p>

				<button class="btn-adopt" disabled={notAvailable} on:click={handleAdopt}>
					{notAvailable ? `Estado: ${statusText}` : 'Quiero Adoptar 🐾'}
				</button>
			</div>
		</div>
	</div>
</div>
