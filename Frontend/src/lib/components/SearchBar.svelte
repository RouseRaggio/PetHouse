<script>
	export let search = "";
</script>

<div class="search-wrapper">
	<div class="search-container">
		<span class="search-icon">🔍</span>
		<input
			type="text"
			class="search-input"
			placeholder="Buscar por nombre, especie o raza..."
			bind:value={search}
		/>
		{#if search}
			<button class="search-clear" on:click={() => search = ''}>✕</button>
		{/if}
	</div>
</div>

<style>
	.search-wrapper {
		display: flex;
		justify-content: center;
		padding: 0 1rem;
		max-width: 550px;
		margin: 0 auto;
	}

	.search-container {
		position: relative;
		width: 100%;
		display: flex;
		align-items: center;
	}

	.search-icon {
		position: absolute;
		left: 18px;
		font-size: 1.2rem;
		z-index: 2;
		animation: float 3s ease-in-out infinite;
	}

	@keyframes float {
		0%, 100% { transform: translateY(0); }
		50% { transform: translateY(-4px); }
	}

	.search-input {
		width: 100%;
		padding: 16px 50px 16px 52px;
		font-family: var(--font-body);
		font-size: 1rem;
		font-weight: 600;
		color: var(--ink);
		background: white;
		border: 3px solid var(--ink);
		border-radius: 50px;
		box-shadow: 4px 4px 0 var(--ink);
		outline: none;
		transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
	}

	.search-input::placeholder {
		color: var(--warm-gray);
		font-weight: 400;
	}

	.search-input:focus {
		border-color: var(--coral);
		box-shadow: 5px 5px 0 var(--coral);
		transform: translateY(-2px);
	}

	.search-clear {
		position: absolute;
		right: 16px;
		background: var(--coral);
		color: white;
		border: 2px solid var(--ink);
		width: 28px;
		height: 28px;
		border-radius: 50%;
		cursor: pointer;
		font-size: 0.8rem;
		display: flex;
		align-items: center;
		justify-content: center;
		font-weight: bold;
		transition: all 0.2s ease;
		box-shadow: 2px 2px 0 var(--ink);
	}

	.search-clear:hover {
		background: var(--coral-dark);
		transform: rotate(90deg) scale(1.1);
	}
</style>