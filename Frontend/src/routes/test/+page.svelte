<script>
    import Navbar from '$lib/components/Navbar.svelte';
</script>

<svelte:head>
    <title>Test Page - PetHouse</title>
</svelte:head>

<Navbar />

<main class="container py-5">
    <div class="text-center">
        <h1>Test Page</h1>
        <p>If you can see this, the frontend is working!</p>
        <div class="alert alert-success">
            PetHouse is loading correctly
        </div>
    </div>
</main>