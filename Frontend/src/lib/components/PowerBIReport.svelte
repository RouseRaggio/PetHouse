<script>
	export let title = 'Reporte';
	export let src = '';
	export let height = '400px';
	export let width = '100%';
</script>

<div class="card mt-5 p-3">
	<h5>{title}</h5>

	<iframe {title} {width} {height} {src} frameborder="0" allowFullScreen></iframe>
</div>
