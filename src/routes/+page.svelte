<script lang="ts">
	import { onMount } from 'svelte';

	type CarouselSlide = {
		title: string;
		description: string;
		imageUrl: string;
	};

	const slides: CarouselSlide[] = [
		{
			title: 'Prototype navigation scene',
			description: 'Add your first project photo here.',
			imageUrl: ''
		},
		{
			title: 'Obstacle detection testing',
			description: 'Add a second photo of the robot in action.',
			imageUrl: ''
		},
		{
			title: 'Guided mobility demo',
			description: 'Add a third photo for the final preview.',
			imageUrl: ''
		}
	];

	let currentSlide = $state(0);

	const nextSlide = () => {
		currentSlide = (currentSlide + 1) % slides.length;
	};

	const goToSlide = (index: number) => {
		currentSlide = index;
	};

	onMount(() => {
		const autoSlide = window.setInterval(nextSlide, 5000);

		const revealElements = Array.from(document.querySelectorAll<HTMLElement>('[data-reveal]'));
		const revealObserver = new IntersectionObserver(
			(entries, observer) => {
				for (const entry of entries) {
					if (entry.isIntersecting) {
						entry.target.classList.add('is-visible');
						observer.unobserve(entry.target);
					}
				}
			},
			{ threshold: 0.1, rootMargin: '0px 0px -6% 0px' }
		);

		for (const el of revealElements) revealObserver.observe(el);

		return () => {
			window.clearInterval(autoSlide);
			revealObserver.disconnect();
		};
	});
</script>

<svelte:head>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link
		href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&display=swap"
		rel="stylesheet"
	/>
</svelte:head>

<!-- ─── HERO ─── -->
<section class="hero">
	<div class="hero-carousel">
		{#key currentSlide}
			{#if slides[currentSlide].imageUrl}
				<img
					class="hero-bg"
					src={slides[currentSlide].imageUrl}
					alt={slides[currentSlide].title}
				/>
			{:else}
				<div class="hero-bg hero-bg--placeholder" aria-hidden="true"></div>
			{/if}
		{/key}
	</div>

	<div class="hero-content">
		<p class="label">Assistive Robotics</p>
		<h1>Guiding mobility through<br /><em>intelligent&nbsp;robotics</em></h1>
		<p class="hero-sub">
			Safer, more confident movement in unfamiliar environments — powered by real-time obstacle
			detection and AI-driven navigation.
		</p>
		<nav class="hero-nav" aria-label="Jump to section">
			<a href="#problem">Problem</a>
			<a href="#how">How it works</a>
			<a href="#demo">Demo</a>
			<a href="#cost">Cost context</a>
			<a href="#impact">Impact</a>
		</nav>
	</div>

	<div class="hero-dots" aria-label="Carousel navigation">
		{#each slides as _, i}
			<button
				type="button"
				class="dot"
				class:is-active={i === currentSlide}
				aria-label={`Slide ${i + 1}`}
				onclick={() => goToSlide(i)}
			></button>
		{/each}
	</div>
</section>

<!-- ─── PROBLEM ─── -->
<section class="split split--img-right" id="problem">
	<div class="split__text reveal" data-reveal>
		<p class="label">The problem</p>
		<h2>Mobility should not<br />depend on uncertainty</h2>
		<p>
			Navigating unfamiliar environments is challenging and stressful for blind or visually
			impaired individuals. Traditional aids leave gaps in spatial awareness that can compromise
			safety—and independence.
		</p>
	</div>
	<div class="split__media split__media--png reveal" data-reveal style="--reveal-delay:120ms">
		<img
			src="/images/Mobility%20should%20not%20depend%20on%20uncertainty.png"
			alt="Mobility should not depend on uncertainty"
		/>
	</div>
</section>

<!-- ─── HOW IT WORKS ─── -->
<section class="split split--img-left" id="how">
	<div class="split__media split__media--png reveal" data-reveal>
		<img src="/images/Detect.%20Decide.%20Guide.png" alt="Detect. Decide. Guide." />
	</div>
	<div class="split__text reveal" data-reveal style="--reveal-delay:120ms">
		<p class="label">How it works</p>
		<h2>Detect. Decide.<br />Guide.</h2>
		<p>
			The robot senses nearby obstacles in real time, analyzes the safest path, and provides
			haptic and audio feedback to support guided mobility — no screen required.
		</p>
	</div>
</section>

<!-- ─── DEMO ─── -->
<section class="demo-section" id="demo">
	<div class="demo-inner reveal" data-reveal>
		<p class="label">Prototype demo</p>
		<h2>See it in action</h2>
		<p>
			Watch how the robot responds to obstacles and supports navigation in a real-world scenario.
		</p>
		<div class="video-frame">
			<div class="video-placeholder">Video preview area</div>
		</div>
	</div>
</section>

<!-- ─── COST CONTEXT ─── -->
<section class="split split--img-right" id="cost">
	<div class="split__text reveal" data-reveal>
		<p class="label">Why it matters</p>
		<h2>Guide dogs cost<br /><em>over $20,000</em></h2>
		<p>
			A professionally trained guide dog can exceed $20,000 USD — and availability is limited.
			This project explores an assistive robotics approach to provide scalable, affordable
			guidance support.
		</p>
	</div>
	<div class="split__media reveal" data-reveal style="--reveal-delay:120ms">
		<img src="/images/perroguia.jpg" alt="Guide dog support context" />
	</div>
</section>

<!-- ─── IMPACT ─── -->
<section class="split split--img-left" id="impact">
	<div class="split__media split__media--png reveal" data-reveal>
		<img
			src="/images/Built%20to%20support%20independence.png"
			alt="Built to support independence"
		/>
	</div>
	<div class="split__text reveal" data-reveal style="--reveal-delay:120ms">
		<p class="label">Impact</p>
		<h2>Built to support<br />independence</h2>
		<p>
			Our goal is to make assistive mobility more intelligent, responsive, and accessible —
			through robotics and AI that adapt to real-world conditions.
		</p>
	</div>
</section>

<!-- ─── FOOTER ─── -->
<footer class="site-footer reveal" data-reveal>
	<p class="footer-brand">Navis</p>
	<p>Made by Hugo, Hiram &amp; Fernando</p>
</footer>
