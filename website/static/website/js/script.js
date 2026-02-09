// ROI Calculator - Updated for Django
function calculateROI() {
    const monthlySpend = parseFloat(document.getElementById('monthly-spend').value) || 100000;
    const currentROAS = parseFloat(document.getElementById('current-roas').value) || 3.0;
    
    // Get CSRF token
    const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
    
    // Try to use Django backend, fallback to client-side calculation
    if (csrfTokenElement) {
        const csrftoken = csrfTokenElement.value;
        
        // Make AJAX request to Django backend
        fetch('/calculate-roi/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken
            },
            body: `monthly_spend=${monthlySpend}&current_roas=${currentROAS}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('savings').textContent = data.formatted_savings;
            } else {
                console.error('Error calculating ROI:', data.error);
                // Fallback to client-side
                calculateROIClientSide(monthlySpend, currentROAS);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            // Fallback to client-side calculation
            calculateROIClientSide(monthlySpend, currentROAS);
        });
    } else {
        // No CSRF token, use client-side calculation
        calculateROIClientSide(monthlySpend, currentROAS);
    }
}

// Client-side ROI calculation (fallback)
function calculateROIClientSide(monthlySpend, currentROAS) {
    const wastedSpendPercentage = 0.15; // Average of 10-20%
    const potentialSavings = monthlySpend * wastedSpendPercentage;
    document.getElementById('savings').textContent = `$${potentialSavings.toLocaleString(undefined, {maximumFractionDigits: 0})}`;
}

// Initialize calculator on page load
document.addEventListener('DOMContentLoaded', function() {
    calculateROI();
    
    // Add event listeners to inputs
    const monthlySpendInput = document.getElementById('monthly-spend');
    const currentROASInput = document.getElementById('current-roas');
    
    if (monthlySpendInput) {
        monthlySpendInput.addEventListener('input', calculateROI);
    }
    if (currentROASInput) {
        currentROASInput.addEventListener('input', calculateROI);
    }
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Mobile menu toggle
const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
const navLinks = document.querySelector('.nav-links');

if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', function() {
        navLinks.classList.toggle('active');
        mobileMenuToggle.classList.toggle('active');
    });
}

// Navbar scroll effect
let lastScroll = 0;
const navbar = document.querySelector('.navbar');

if (navbar) {
    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 100) {
            navbar.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.boxShadow = 'none';
        }
        
        lastScroll = currentScroll;
    });
}

// Intersection Observer for fade-in animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe elements for animation
document.addEventListener('DOMContentLoaded', function() {
    const animateElements = document.querySelectorAll('.problem-card, .feature-card, .testimonial, .pricing-card, .step');
    
    animateElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});

// Form validation
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Add loading states to buttons
document.querySelectorAll('.btn-primary, .btn-secondary').forEach(button => {
    button.addEventListener('click', function(e) {
        if (this.href === '#demo' || this.href === '#contact') {
            // Add loading state
            const originalText = this.textContent;
            this.textContent = 'Loading...';
            this.disabled = true;
            
            // Simulate API call (replace with actual implementation)
            setTimeout(() => {
                this.textContent = originalText;
                this.disabled = false;
            }, 2000);
        }
    });
});
