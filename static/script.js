// Main JavaScript functions for the Text Summarizer app

document.addEventListener('DOMContentLoaded', function() {
    // Range slider value display
    const rangeSliders = document.querySelectorAll('input[type="range"]');
    
    rangeSliders.forEach(slider => {
        const valueDisplay = slider.nextElementSibling.querySelector('span');
        
        // Initial position
        if (valueDisplay) {
            const percent = (slider.value - slider.min) / (slider.max - slider.min) * 100;
            valueDisplay.style.left = `${percent}%`;
            valueDisplay.textContent = `${Math.round(slider.value * 100)}%`;
        }
        
        // Update on change
        slider.addEventListener('input', function() {
            const percent = (this.value - this.min) / (this.max - this.min) * 100;
            valueDisplay.style.left = `${percent}%`;
            valueDisplay.textContent = `${Math.round(this.value * 100)}%`;
        });
    });
    
    // Copy to clipboard functionality
    window.copyToClipboard = function(className) {
        const element = document.querySelector('.' + className);
        if (!element) return;
        
        const text = element.innerText;
        
        // Create temporary textarea
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.setAttribute('readonly', '');
        textarea.style.position = 'absolute';
        textarea.style.left = '-9999px';
        document.body.appendChild(textarea);
        
        // Select text and copy
        textarea.select();
        document.execCommand('copy');
        
        // Remove textarea
        document.body.removeChild(textarea);
        
        // Show feedback
        alert('Summary copied to clipboard!');
    };
});