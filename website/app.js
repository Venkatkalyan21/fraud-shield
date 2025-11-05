// Fraud Shield - Smooth Interface Enhancements
// Optimized for 60fps performance and glitch-free animations

(function() {
  'use strict';

  // Performance optimizations
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
  
  // Smooth scroll with easing
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href === '#' || href === '#!') return;
        
        const target = document.querySelector(href);
        if (target) {
          e.preventDefault();
          const offset = 80;
          const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - offset;
          
          window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
          });
        }
      });
    });
  }

  // Intersection Observer for fade-in animations
  function initScrollAnimations() {
    if (prefersReducedMotion) return;
    
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);

    // Observe elements with fade-in class
    document.querySelectorAll('.fade-in, .feature-card, .metric-card, .step, .testimonial').forEach(el => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(20px)';
      el.style.transition = 'opacity 0.6s cubic-bezier(0.19, 1, 0.22, 1), transform 0.6s cubic-bezier(0.19, 1, 0.22, 1)';
      el.style.willChange = 'opacity, transform';
      observer.observe(el);
    });
  }

  // Parallax effect for hero section
  function initParallax() {
    if (prefersReducedMotion || isMobile) return;
    
    const hero = document.querySelector('.hero');
    if (!hero) return;

    let ticking = false;
    window.addEventListener('scroll', () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          const scrolled = window.pageYOffset;
          const rate = scrolled * 0.3;
          hero.style.transform = `translateY(${rate}px)`;
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });
  }

  // Enhanced button hover effects
  function initButtonEffects() {
    document.querySelectorAll('.btn, .btn-primary, .btn-ghost, .btn-outline').forEach(btn => {
      btn.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-4px) scale(1.02)';
      });
      
      btn.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1)';
      });

      btn.addEventListener('mousedown', function() {
        this.style.transform = 'translateY(-2px) scale(0.98)';
      });

      btn.addEventListener('mouseup', function() {
        this.style.transform = 'translateY(-4px) scale(1.02)';
      });
    });
  }

  // Card hover effects with 3D transform
  function initCardEffects() {
    document.querySelectorAll('.feature-card, .metric-card, .hero-card').forEach(card => {
      if (prefersReducedMotion) return;
      
      card.addEventListener('mousemove', function(e) {
        const rect = this.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = (y - centerY) / 20;
        const rotateY = (centerX - x) / 20;

        this.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-12px)`;
      });

      card.addEventListener('mouseleave', function() {
        this.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)';
      });
    });
  }

  // Loading state for forms
  function initFormLoading() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
      form.addEventListener('submit', function() {
        const submitBtn = this.querySelector('button[type="submit"], .btn-primary');
        if (submitBtn) {
          const originalText = submitBtn.textContent;
          submitBtn.disabled = true;
          submitBtn.innerHTML = '<span style="display:inline-flex;align-items:center;gap:8px;"><span style="animation:spin 1s linear infinite;display:inline-block;">⟳</span> Processing...</span>';
          submitBtn.style.opacity = '0.7';
          submitBtn.style.cursor = 'wait';
          
          // Add spinner animation
          if (!document.getElementById('spin-keyframes')) {
            const style = document.createElement('style');
            style.id = 'spin-keyframes';
            style.textContent = '@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }';
            document.head.appendChild(style);
          }
        }
      });
    });
  }

  // Enhanced file drag and drop
  function initDragDrop() {
    const dropzones = document.querySelectorAll('.dropzone');
    dropzones.forEach(dropzone => {
      const input = dropzone.querySelector('input[type="file"]');
      if (!input) return;

      ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, preventDefaults, false);
      });

      function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
      }

      ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, () => {
          dropzone.style.borderColor = 'rgba(74, 208, 255, 0.85)';
          dropzone.style.background = 'rgba(12, 16, 34, 0.95)';
          dropzone.style.transform = 'scale(1.02)';
        }, false);
      });

      ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, () => {
          dropzone.style.borderColor = 'rgba(122, 130, 255, 0.5)';
          dropzone.style.background = 'rgba(14, 16, 33, 0.65)';
          dropzone.style.transform = 'scale(1)';
        }, false);
      });

      dropzone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length > 0) {
          input.files = files;
          const label = dropzone.querySelector('label');
          if (label) {
            label.textContent = `✓ ${files[0].name}`;
            label.style.color = '#86f7b9';
          }
        }
      }, false);

      // Show filename when file is selected
      input.addEventListener('change', function() {
        if (this.files && this.files[0]) {
          const label = dropzone.querySelector('label');
          if (label) {
            label.textContent = `✓ ${this.files[0].name}`;
            label.style.color = '#86f7b9';
          }
        }
      });
    });
  }

  // Smooth number counter animation
  function animateCounter(element, target, duration = 2000) {
    if (prefersReducedMotion) {
      element.textContent = target;
      return;
    }

    const start = parseFloat(element.textContent) || 0;
    const increment = target / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
      current += increment;
      if ((increment > 0 && current >= target) || (increment < 0 && current <= target)) {
        element.textContent = target;
        clearInterval(timer);
      } else {
        element.textContent = Math.floor(current);
      }
    }, 16);
  }

  // Initialize counters on results page
  function initCounters() {
    document.querySelectorAll('.metric-card strong, .metric .value').forEach(el => {
      const text = el.textContent.trim();
      const number = parseFloat(text.replace(/[^\d.]/g, ''));
      if (!isNaN(number) && number > 0) {
        el.setAttribute('data-target', number);
        el.textContent = '0';
        setTimeout(() => animateCounter(el, number), 300);
      }
    });
  }

  // Navbar scroll effect
  function initNavbarScroll() {
    const navbar = document.querySelector('.navbar, header');
    if (!navbar) return;

    let lastScroll = 0;
    window.addEventListener('scroll', () => {
      const currentScroll = window.pageYOffset;
      
      if (currentScroll > 100) {
        navbar.style.backdropFilter = 'blur(28px)';
        navbar.style.background = 'rgba(7, 9, 23, 0.88)';
        navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.3)';
      } else {
        navbar.style.backdropFilter = 'blur(24px)';
        navbar.style.background = 'rgba(7, 9, 23, 0.75)';
        navbar.style.boxShadow = '0 1px 0 rgba(255, 255, 255, 0.05)';
      }
      
      lastScroll = currentScroll;
    }, { passive: true });
  }

  // Smooth page transitions (optional - can be enabled if needed)
  function initPageTransitions() {
    // Disabled by default to avoid navigation delays
    // Uncomment if you want page transitions
    /*
    document.querySelectorAll('a[href^="/"]').forEach(link => {
      link.addEventListener('click', function(e) {
        if (this.getAttribute('href').startsWith('/') && !this.getAttribute('download')) {
          e.preventDefault();
          const href = this.getAttribute('href');
          
          // Add fade out effect
          document.body.style.opacity = '0';
          document.body.style.transition = 'opacity 0.2s ease';
          
          setTimeout(() => {
            window.location.href = href;
          }, 200);
        }
      });
    });
    */
  }

  // Performance: Debounce function
  function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  // Optimize scroll listeners
  const optimizedScroll = debounce(() => {
    // Any scroll-based logic here
  }, 10);

  // Initialize everything when DOM is ready
  function init() {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', init);
      return;
    }

    // Add fade-in class to body
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.4s ease';
    setTimeout(() => {
      document.body.style.opacity = '1';
    }, 10);

    initSmoothScroll();
    initScrollAnimations();
    initParallax();
    initButtonEffects();
    initCardEffects();
    initFormLoading();
    initDragDrop();
    initCounters();
    initNavbarScroll();
    // initPageTransitions(); // Uncomment if you want page transitions

    // Clean up will-change after animations
    setTimeout(() => {
      document.querySelectorAll('[style*="will-change"]').forEach(el => {
        el.style.willChange = 'auto';
      });
    }, 2000);
  }

  // Start initialization
  init();

  // Expose utility functions globally if needed
  window.FraudShield = {
    animateCounter,
    initCounters
  };

})();
