// js/main.js
document.addEventListener('DOMContentLoaded', () => {
    Reveal.initialize({
        controls: true,
        progress: true,
        center: true,
        hash: true,
        transition: 'slide', // none/fade/slide/convex/concave/zoom
        
        // Push presentation layout slightly larger for wide tables
        width: 1280,
        height: 720,
        margin: 0.04,
        minScale: 0.2,
        maxScale: 2.0,

        // Optional plugins
        plugins: []
    });
});
