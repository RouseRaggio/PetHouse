<script>
	import { fade, scale } from 'svelte/transition';
	import { createEventDispatcher, onMount } from 'svelte';
	import { goto } from '$app/navigation';

	export let selectedPet;

	$: age = selectedPet.birth_date ? Math.floor((new Date() - new Date(selectedPet.birth_date)) / (365.25 * 24 * 60 * 60 * 1000)) : 'Desconocida';

	$: adoptado = selectedPet.status !== 'AVAILABLE';

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

				<div class="status-badge {adoptado ? 'adoptado' : 'disponible'}">
					{adoptado ? 'Adoptado' : 'Disponible'}
				</div>

				<p><strong>Edad:</strong> {age} años</p>
				<p><strong>Sexo:</strong> {selectedPet.gender}</p>
				<p><strong>Raza:</strong> {selectedPet.race}</p>
				<p><strong>Descripción:</strong> {selectedPet.description}</p>

				<button class="btn-adopt" disabled={adoptado} on:click={handleAdopt}>
					{adoptado ? 'Ya fue adoptado' : 'Quiero Adoptar 🐾'}
				</button>
			</div>
		</div>
	</div>
</div>
