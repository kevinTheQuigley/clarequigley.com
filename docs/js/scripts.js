/*!
* Start Bootstrap - Clean Blog v6.0.9 (https://startbootstrap.com/theme/clean-blog)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-clean-blog/blob/master/LICENSE)
*/

window.addEventListener('DOMContentLoaded', () => {
    // Navigation functionality
    let scrollPos = 0;
    const mainNav = document.getElementById('mainNav');
    const headerHeight = mainNav ? mainNav.clientHeight : 0;
    
    window.addEventListener('scroll', function() {
        const currentTop = document.body.getBoundingClientRect().top * -1;
        
        // Navigation state based on scroll position
        if (mainNav) {
            if (currentTop < scrollPos) {
                // Scrolling Up
                if (currentTop > 0 && mainNav.classList.contains('is-fixed')) {
                    mainNav.classList.add('is-visible');
                } else {
                    mainNav.classList.remove('is-visible', 'is-fixed');
                }
            } else {
                // Scrolling Down
                mainNav.classList.remove('is-visible');
                
                if (currentTop > headerHeight && !mainNav.classList.contains('is-fixed')) {
                    mainNav.classList.add('is-fixed');
                }
            }
            scrollPos = currentTop;
        }
    });
    
    // Handle mobile navigation toggle
    const navbarToggler = document.querySelector('.navbar-toggler');
    if (navbarToggler) {
        navbarToggler.addEventListener('click', function() {
            const expanded = this.getAttribute('aria-expanded') === 'true';
            this.setAttribute('aria-expanded', !expanded);
            document.querySelector('#navbarResponsive').classList.toggle('show');
        });
    }
    
    // Load header and footer content
    loadComponent('header-placeholder', 'header.html');
    loadComponent('footer-placeholder', 'footer.html');
});

// Helper function to load HTML components
function loadComponent(targetId, sourcePath) {
    const element = document.getElementById(targetId);
    if (element) {
        fetch(sourcePath)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Failed to load ${sourcePath}`);
                }
                return response.text();
            })
            .then(data => {
                element.innerHTML = data;
            })
            .catch(error => {
                console.error(`Error loading ${sourcePath}:`, error);
            });
    }
}