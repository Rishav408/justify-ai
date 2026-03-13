// Main Application JavaScript

// Initialize AOS (Animate On Scroll)
document.addEventListener('DOMContentLoaded', () => {
    AOS.init({
        duration: 800,
        offset: 100,
        once: true,
        easing: 'ease-in-out'
    });
});


// Mobile Navigation Menu Controller
class MobileNavController {
    constructor() {
        this.mobileToggle = document.getElementById('mobile-toggle');
        this.navLinks = document.getElementById('nav-links');
        this.isOpen = false;
    }

    init() {
        if (!this.mobileToggle || !this.navLinks) return;

        // Toggle menu on button click
        this.mobileToggle.addEventListener('click', () => this.toggleMenu());

        // Close menu when clicking on a link
        const links = this.navLinks.querySelectorAll('.nav-link');
        links.forEach(link => {
            link.addEventListener('click', () => {
                if (this.isOpen) {
                    this.closeMenu();
                }
            });
        });

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (this.isOpen && 
                !this.navLinks.contains(e.target) && 
                !this.mobileToggle.contains(e.target)) {
                this.closeMenu();
            }
        });

        // Handle escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.closeMenu();
            }
        });
    }

    toggleMenu() {
        if (this.isOpen) {
            this.closeMenu();
        } else {
            this.openMenu();
        }
    }

    openMenu() {
        this.isOpen = true;
        this.navLinks.classList.add('mobile-open');
        this.mobileToggle.classList.add('active');
        this.mobileToggle.setAttribute('aria-expanded', 'true');
        document.body.style.overflow = 'hidden'; // Prevent scrolling when menu is open
    }

    closeMenu() {
        this.isOpen = false;
        this.navLinks.classList.remove('mobile-open');
        this.mobileToggle.classList.remove('active');
        this.mobileToggle.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = ''; // Restore scrolling
    }
}

// Initialize mobile navigation
document.addEventListener('DOMContentLoaded', () => {
    const mobileNav = new MobileNavController();
    mobileNav.init();
});


// Particle Network Animation for Hero Section
class ParticleNetwork {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) return;
        
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.particleCount = 50;
        this.maxDistance = 150;
        this.animationId = null;
        
        this.init();
    }

    init() {
        this.resizeCanvas();
        this.createParticles();
        this.animate();
        
        // Handle window resize
        window.addEventListener('resize', () => {
            this.resizeCanvas();
            this.createParticles();
        });
    }

    resizeCanvas() {
        const parent = this.canvas.parentElement;
        this.canvas.width = parent.offsetWidth;
        this.canvas.height = parent.offsetHeight;
    }

    createParticles() {
        this.particles = [];
        for (let i = 0; i < this.particleCount; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                radius: Math.random() * 2 + 1
            });
        }
    }

    drawParticle(particle) {
        this.ctx.beginPath();
        this.ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
        this.ctx.fillStyle = this.getParticleColor();
        this.ctx.fill();
    }

    drawLine(p1, p2, distance) {
        const opacity = 1 - (distance / this.maxDistance);
        this.ctx.beginPath();
        this.ctx.moveTo(p1.x, p1.y);
        this.ctx.lineTo(p2.x, p2.y);
        this.ctx.strokeStyle = this.getLineColor(opacity);
        this.ctx.lineWidth = 0.5;
        this.ctx.stroke();
    }

    getParticleColor() {
        const theme = document.documentElement.getAttribute('data-theme');
        return theme === 'dark' ? 'rgba(108, 99, 255, 0.8)' : 'rgba(26, 42, 68, 0.8)';
    }

    getLineColor(opacity) {
        const theme = document.documentElement.getAttribute('data-theme');
        return theme === 'dark' 
            ? `rgba(0, 194, 168, ${opacity * 0.3})` 
            : `rgba(108, 99, 255, ${opacity * 0.3})`;
    }

    updateParticle(particle) {
        particle.x += particle.vx;
        particle.y += particle.vy;

        // Bounce off edges
        if (particle.x < 0 || particle.x > this.canvas.width) {
            particle.vx *= -1;
        }
        if (particle.y < 0 || particle.y > this.canvas.height) {
            particle.vy *= -1;
        }

        // Keep particles within bounds
        particle.x = Math.max(0, Math.min(this.canvas.width, particle.x));
        particle.y = Math.max(0, Math.min(this.canvas.height, particle.y));
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Update and draw particles
        this.particles.forEach(particle => {
            this.updateParticle(particle);
            this.drawParticle(particle);
        });

        // Draw connections
        for (let i = 0; i < this.particles.length; i++) {
            for (let j = i + 1; j < this.particles.length; j++) {
                const dx = this.particles[i].x - this.particles[j].x;
                const dy = this.particles[i].y - this.particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < this.maxDistance) {
                    this.drawLine(this.particles[i], this.particles[j], distance);
                }
            }
        }

        this.animationId = requestAnimationFrame(() => this.animate());
    }

    destroy() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
    }
}

// Initialize particle network on hero page
document.addEventListener('DOMContentLoaded', () => {
    const particleCanvas = document.getElementById('particle-canvas');
    if (particleCanvas) {
        const particleNetwork = new ParticleNetwork('particle-canvas');
        
        // Reinitialize on theme change for color updates
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                // Small delay to ensure theme has changed
                setTimeout(() => {
                    if (particleNetwork) {
                        particleNetwork.animate();
                    }
                }, 50);
            });
        }
    }
});
