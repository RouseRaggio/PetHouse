<script>
	import { fade, slide } from 'svelte/transition';
	export let data;

	let selectedPet = null;

	const pets = [
		{
			id: 1,
			name: "Luna",
			species: "Perro",
			race: "Labrador",
			age: "2 años",
			gender: "Hembra",
			description: "Cariñosa y sociable.",
			image_url: "https://placedog.net/400/300?id=1"
		}
	];

	function toggleDetails(pet) {
		selectedPet = selectedPet?.id === pet.id ? null : pet;
	}
</script>

{#each data.pets as pet}
	<!-- tarjeta -->
{/each}

{#if selectedPet}
    <!-- detalles -->
{/if}

