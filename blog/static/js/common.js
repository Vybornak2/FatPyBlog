/**
 * Common JavaScript functions for the FatPyBlog application
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all dropdown elements
    const dropdownToggleElements = document.querySelectorAll('.dropdown-toggle');
    if (typeof bootstrap !== 'undefined') {
        dropdownToggleElements.forEach(element => {
            new bootstrap.Dropdown(element);
        });
    }
    
    // Image handling for post content
    const postImages = document.querySelectorAll('.post-content img');
    postImages.forEach(img => {
        // Add click handler for images to show fullscreen if needed
        img.addEventListener('click', function() {
            if (this.classList.contains('fullscreen')) {
                this.classList.remove('fullscreen');
            } else {
                // Only if image is larger than display viewport
                if (this.naturalWidth > this.width) {
                    this.classList.add('fullscreen');
                }
            }
        });
        
        // Add loading="lazy" for better performance
        img.setAttribute('loading', 'lazy');
    });
    
    // Form validation highlights
    const formControls = document.querySelectorAll('.form-control');
    formControls.forEach(control => {
        control.addEventListener('blur', function() {
            if (this.checkValidity()) {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            } else if (this.value !== '') {
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
            }
        });
    });
});
