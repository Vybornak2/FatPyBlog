document.addEventListener('DOMContentLoaded', function() {
    // Ensure all images in posts are properly constrained
    const postImages = document.querySelectorAll('.post-content-frame img');
    postImages.forEach(img => {
        img.classList.add('md-image-override');
        img.removeAttribute('width');
        img.removeAttribute('height');
        img.style.maxWidth = '100%';
        img.style.height = 'auto';
        
        // Handle image loading error
        img.addEventListener('error', function() {
            this.src = '/static/img/image-placeholder.png';
            this.alt = 'Image could not be loaded';
        });
    });
});
