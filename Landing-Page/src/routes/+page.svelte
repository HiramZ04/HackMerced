<script lang="ts">
	import { onMount } from 'svelte';

	type CarouselSlide = {
		title: string;
		description: string;
		imageUrl: string;
	};

	const slides: CarouselSlide[] = [
		{
			title: 'Team Navis at HackMerced',
			description: 'Our team with the robot prototype during HackMerced.',
			imageUrl: '/CarouselImages/MLH3personoHORIZONTAL.jpeg'
		},
		{
			title: 'Prototype navigation setup',
			description: 'Front view of the robot with the simulator in the background.',
			imageUrl: '/CarouselImages/RobotandSimulator.jpeg'
		},
		{
			title: 'Side view of the prototype',
			description: 'A closer look at the robot hardware and structure.',
			imageUrl: '/CarouselImages/robotsideview.jpeg'
		}
	];

	let currentSlide = $state(0);

	const nextSlide = () => {
		currentSlide = (currentSlide + 1) % slides.length;
	};

	const goToSlide = (index: number) => {
		currentSlide = index;
	};

	function animateCount(el: HTMLElement, target: number, prefix: string, suffix: string) {
		const duration = 1200;
		const startTime = performance.now();
		const step = (now: number) => {
			const progress = Math.min((now - startTime) / duration, 1);
			const eased = 1 - Math.pow(1 - progress, 3);
			const current = Math.floor(eased * target);
			el.textContent = `${prefix}${current.toLocaleString()}${suffix}`;
			if (progress < 1) requestAnimationFrame(step);
		};
		requestAnimationFrame(step);
	}

	onMount(() => {
		const autoSlide = window.setInterval(nextSlide, 5000);

		/* ── 2. Hero content stagger ── */
		const heroContent = document.querySelector<HTMLElement>('.hero-content');
		const heroLines = document.querySelectorAll<HTMLElement>('.hero-line');
		const heroLabel = document.querySelector<HTMLElement>('.hero .label');
		const heroSub = document.querySelector<HTMLElement>('.hero-sub');
		const heroNavEl = document.querySelector<HTMLElement>('.hero-nav');

		const heroObserver = new IntersectionObserver(
			(entries, obs) => {
				for (const entry of entries) {
					if (entry.isIntersecting) {
						if (heroLabel) heroLabel.classList.add('is-visible');
						heroLines.forEach((line, i) => {
							setTimeout(() => line.classList.add('is-visible'), 150 + i * 100);
						});
						const linesDelay = 150 + heroLines.length * 100;
						if (heroSub) setTimeout(() => heroSub.classList.add('is-visible'), linesDelay + 80);
						if (heroNavEl) setTimeout(() => heroNavEl.classList.add('is-visible'), linesDelay + 180);
						obs.unobserve(entry.target);
					}
				}
			},
			{ threshold: 0.1 }
		);
		if (heroContent) heroObserver.observe(heroContent);

		/* ── 3. Scroll-reveal (Apple timing) ── */
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

		/* ── 4. Heading scale-in ── */
		const scaleElements = document.querySelectorAll<HTMLElement>('[data-scale-in]');
		const scaleObserver = new IntersectionObserver(
			(entries, obs) => {
				for (const entry of entries) {
					if (entry.isIntersecting) {
						entry.target.classList.add('is-scaled');
						obs.unobserve(entry.target);
					}
				}
			},
			{ threshold: 0.2, rootMargin: '0px 0px -5% 0px' }
		);
		for (const el of scaleElements) scaleObserver.observe(el);

		/* ── 5. Number count-up ── */
		const countElements = document.querySelectorAll<HTMLElement>('[data-count-up]');
		const countObserver = new IntersectionObserver(
			(entries, obs) => {
				for (const entry of entries) {
					if (entry.isIntersecting) {
						const el = entry.target as HTMLElement;
						const target = parseInt(el.dataset.countUp || '0', 10);
						const prefix = el.dataset.countPrefix || '';
						const suffix = el.dataset.countSuffix || '';
						animateCount(el, target, prefix, suffix);
						obs.unobserve(el);
					}
				}
			},
			{ threshold: 0.5 }
		);
		for (const el of countElements) countObserver.observe(el);

		return () => {
			window.clearInterval(autoSlide);
			revealObserver.disconnect();
			heroObserver.disconnect();
			scaleObserver.disconnect();
			countObserver.disconnect();
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
	<div class="hero-shell">
		<div class="hero-content">
			<p class="label">Navis</p>
			<h1>
				<span class="hero-line">Guiding mobility through</span><br />
				<span class="hero-line"><em>intelligent&nbsp;robotics</em></span>
			</h1>
			<p class="hero-sub">
				Safer, more confident movement in unfamiliar environments powered by real-time obstacle
				detection.
			</p>
			<nav class="hero-nav" aria-label="Jump to section">
				<a href="#problem">Problem</a>
				<a href="#how">How it works</a>
				<a href="#demo">Demo</a>
				<a href="#cost">Cost context</a>
				<a href="#impact">Impact</a>
			</nav>
		</div>

		<div class="hero-visual">
			{#key currentSlide}
				{#if slides[currentSlide].imageUrl}
					<div class="hero-photo-card">
						<img
							class="hero-photo"
							src={slides[currentSlide].imageUrl}
							alt={slides[currentSlide].title}
						/>
						<div class="hero-photo-caption">
							<h3>{slides[currentSlide].title}</h3>
							<p>{slides[currentSlide].description}</p>
						</div>
					</div>
				{:else}
					<div class="hero-photo-card hero-photo-card--placeholder" aria-hidden="true">
						<div class="hero-placeholder-content">
							<span>Team / prototype visual</span>
						</div>
					</div>
				{/if}
			{/key}
		</div>
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

<!-- ─── DEMO ─── -->
<section class="demo-section" id="demo">
	<div class="demo-inner reveal" data-reveal>
		<p class="label">Prototype demo</p>
		<h2 data-scale-in>See it in action</h2>
		<p>
			Watch how the robot responds to obstacles and supports navigation in a real world scenario.
		</p>
		<div class="video-frame">
			<video controls playsinline preload="metadata" poster="/CarouselImages/robot.JPG">
				<source src="/videos/demo.mp4" type="video/mp4" />
				Your browser does not support the video tag.
			</video>
		</div>
	</div>
</section>

<!-- ─── PROBLEM ─── -->
<section class="split split--img-right" id="problem">
	<div class="split__text reveal" data-reveal>
		<p class="label">The problem</p>
		<h2 data-scale-in>Mobility should not<br />depend on uncertainty</h2>
		<p>
			Navigating unfamiliar environments is challenging and stressful for blind or visually
			impaired individuals. Traditional aids leave gaps in spatial awareness that can compromise
			safety and independence.
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
		<h2 data-scale-in>Detect. Decide.<br />Guide.</h2>
		<p>
			The robot senses nearby obstacles in real time, analyzes the safest path, and provides
			haptic and audio feedback to support guided mobility with no screen required.
		</p>
	</div>
</section>

<!-- ─── COST CONTEXT ─── -->
<section class="split split--img-right" id="cost">
	<div class="split__text reveal" data-reveal>
		<p class="label">Why it matters</p>
		<h2 data-scale-in>Guide dogs cost<br /><em><span data-count-up="20000" data-count-prefix="over $">over $20,000</span></em></h2>
		<p>
			A professionally trained guide dog can exceed $20,000 USD and availability is limited.
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
		<h2 data-scale-in>Built to support<br />independence</h2>
		<p>
			Our goal is to make assistive mobility more intelligent, responsive, and accessible
			through robotics and AI that adapt to real world conditions.
		</p>
	</div>
</section>

<!-- ─── FOOTER ─── -->
<footer class="site-footer reveal" data-reveal>
	<p class="footer-brand">Navis</p>
	<p>Made by Hugo, Hiram &amp; Fernando</p>
	<a
		class="footer-github"
		href="https://github.com/HiramZ04/HackMerced"
		target="_blank"
		rel="noopener noreferrer"
	>
		<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
			<path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61-.546-1.385-1.335-1.755-1.335-1.755-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.418-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23A11.52 11.52 0 0 1 12 6.803c1.02.005 2.047.138 3.006.404 2.29-1.552 3.297-1.23 3.297-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 21.795 24 17.295 24 12c0-6.63-5.37-12-12-12z"/>
		</svg>
		Team Navis / HackMerced
	</a>
</footer>
