<script>
	import Navbar from '$lib/components/Navbar.svelte';
	import PetCard from '$lib/components/PetCard.svelte';
	import PetModal from '$lib/components/PetModal.svelte';
	import SearchBar from '$lib/components/SearchBar.svelte';
	import { fade } from 'svelte/transition';
	import '../app.css';

	export let data;
    let selectedPet = null;

	function openModal(pet) {
		selectedPet = pet;
	}
    
	function closeModal() {
		selectedPet = null;
	}

	function togglePet(id) {
		openPetId = openPetId === id ? null : id;
	}

	let search = '';

	$: filteredPets = data.pets.filter(
		(pet) =>
			pet.name.toLowerCase().includes(search.toLowerCase()) ||
			pet.species.toLowerCase().includes(search.toLowerCase()) ||
			(pet.race && pet.race.toLowerCase().includes(search.toLowerCase()))
	);
</script>

<section class="hero-section mt-10 text-white text-center d-flex align-items-center">
	<div class="overlay"></div>

	<div class="container position-relative">
		<h1 in:fade={{ duration: 800 }} class="display-4 fw-bold">En Busca de un Hogar</h1>

		<p in:fade={{ delay: 200, duration: 800 }} class="lead">
			Encuentra tu mejor amigo para toda la vida
		</p>

		<div in:fade={{ delay: 400, duration: 800 }}>
			<SearchBar bind:search />
		</div>
	</div>
</section>

<section class="py-4 bg-light">
	<div class="container">
		<h2 class="text-center mb-5">Nuestras Mascotas</h2>

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
	<br>
	<br>
</section>

<section class="text-center py-5 text-black bg-red"> 
	<div class="container">
		<h3>¿Tienes una mascota para dar en adopción?</h3>
		<p>Publica su información y ayúdale a encontrar un nuevo hogar.</p>
		<a href="/publicar" class="btn btn-lg btn-warning">Publicar Mascota</a>
	</div>
</section>

<!--  
<footer class="bg-dark text-center text-white py-3">
    
    <small>© 2026 PetHouse</small>
</footer>-->
