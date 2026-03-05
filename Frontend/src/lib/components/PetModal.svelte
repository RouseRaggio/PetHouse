<script>
	import { fade, scale } from "svelte/transition";
	import { createEventDispatcher, onMount } from "svelte";

	export let selectedPet;
    
	const dispatch = createEventDispatcher();

	function close() {
		dispatch("close");
	}

	function handleKey(e) {
		if (e.key === "Escape") close();
	}

	onMount(() => {
		window.addEventListener("keydown", handleKey);
		return () => window.removeEventListener("keydown", handleKey);
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
				<img src={selectedPet.image_url} alt={selectedPet.name} />
			</div>

			<div class="info-container">
				<h3>{selectedPet.name}</h3>

				<div class="status-badge {selectedPet.status}">
					{selectedPet.status === "disponible"
						? "Disponible"
						: "Adoptado"}
				</div>

				<p><strong>Edad:</strong> {selectedPet.age} meses</p>
				<p><strong>Sexo:</strong> {selectedPet.gender}</p>
				<p><strong>Raza:</strong> {selectedPet.race}</p>
				<p><strong>Descripción:</strong> {selectedPet.description}</p>

				<button
					class="btn-adopt"
					disabled={selectedPet.status === "adoptado"}
				>
					{selectedPet.status === "disponible"
						? "Quiero Adoptar 🐾"
						: "Ya fue adoptado"}
				</button>
			</div>
		</div>
	</div>
</div>

