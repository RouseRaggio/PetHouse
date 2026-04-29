<script>
	import Navbar from '$lib/components/Navbar.svelte';
	import PetCard from '$lib/components/PetCard.svelte';
	import PetModal from '$lib/components/PetModal.svelte';
	import { onMount } from 'svelte';

	let selectedPet = null;
	let search = '';
	let pets = [];

	onMount(async () => {
		try {
			const res = await fetch('http://localhost:8001/pets');
			if (res.ok) {
				pets = await res.json();
			}
		} catch (error) {
			console.error('Error fetching pets:', error);
		}
	});

	function openModal(pet) {
		selectedPet = pet;
	}

	function closeModal() {
		selectedPet = null;
	}

	$: filteredPets = pets?.filter(
		(pet) =>
			pet.name.toLowerCase().includes(search.toLowerCase()) ||
			pet.species.toLowerCase().includes(search.toLowerCase()) ||
			(pet.race && pet.race.toLowerCase().includes(search.toLowerCase()))
	) ?? [];
</script>

<Navbar />
<section class="py-4 bg-light">
	<div class="container">
		<h2 class="text-center mb-5">Catálogo de mascotas</h2>

		<div class="mb-4">
			<input
				type="search"
				class="form-control"
				placeholder="Buscar mascotas..."
				bind:value={search}
			/>
		</div>

		<div class="row g-4">
			{#each filteredPets as pet (pet.id)}
				<div class="col-6 col-md-4 col-lg-3">
					<PetCard {pet} on:view={() => openModal(pet)} />
				</div>
			{/each}
		</div>

		{#if selectedPet}
			<PetModal {selectedPet} on:close={closeModal} />
		{/if}
	</div>
</section>
