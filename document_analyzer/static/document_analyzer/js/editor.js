document.addEventListener('DOMContentLoaded', function() {
    // Initialize editable cells
    initEditableCells();
    
    // Apply section box styles
    applySectionBoxStyles();

    // Listen for HTMX after swap events to re-initialize editable cells
    document.body.addEventListener('htmx:afterSwap', function(event) {
        initEditableCells();
        applySectionBoxStyles();
    });

    // Add event listener for sections-updated event to trigger layout preview update
    document.body.addEventListener('sections-updated', function() {
        const previewContainer = document.getElementById('preview-container');
        if (previewContainer) {
            htmx.trigger(previewContainer, 'load');
        }
    });
});

function initEditableCells() {
    // Find all editable cells
    const editableCells = document.querySelectorAll('.editable-cell');
    
    editableCells.forEach(cell => {
        // Skip if already initialized
        if (cell.dataset.initialized) return;
        
        // Mark as initialized
        cell.dataset.initialized = 'true';
        
        // Add click event listener
        cell.addEventListener('click', function() {
            // Skip if already editing
            if (this.classList.contains('editing')) return;
            
            // Get original value
            const originalValue = this.dataset.originalValue || this.textContent.trim();
            
            // Create input element
            const input = document.createElement('input');
            input.type = 'text';
            input.value = originalValue;
            
            // Add editing class to cell
            this.classList.add('editing');
            
            // Clear cell and append input
            this.textContent = '';
            this.appendChild(input);
            
            // Focus input
            input.focus();
            
            // Handle blur event (when focus is lost)
            input.addEventListener('blur', function() {
                finishEditing(cell, input);
            });
            
            // Handle enter key
            input.addEventListener('keydown', function(e) {
                if (e.key === 'Enter') {
                    finishEditing(cell, input);
                } else if (e.key === 'Escape') {
                    // Revert to original value on escape
                    cell.classList.remove('editing');
                    cell.textContent = originalValue;
                }
            });
        });
    });
}

function finishEditing(cell, input) {
    // Get the new value
    const newValue = input.value.trim();
    const originalValue = cell.dataset.originalValue || '';
    
    // Remove editing class
    cell.classList.remove('editing');
    
    // Update cell content
    cell.textContent = newValue;
    
    // Only send HTMX request if value changed
    if (newValue !== originalValue) {
        // Update the original value
        cell.dataset.originalValue = newValue;
        
        // Trigger HTMX request with custom event
        cell.dispatchEvent(new CustomEvent('edited', {
            detail: { value: newValue }
        }));
        
        // Trigger preview update
        document.body.dispatchEvent(new CustomEvent('sections-updated'));
    }
}

// New function added to apply styles from data attributes
function applySectionBoxStyles() {
    const sectionBoxes = document.querySelectorAll('.section-box');
    
    console.log('Found ' + sectionBoxes.length + ' section boxes to style');
    
    // Remove any existing labels (in case of re-rendering)
    document.querySelectorAll('.section-box .section-label').forEach(label => {
        label.remove();
    });
    
    sectionBoxes.forEach((box, index) => {
        // Get values from data attributes
        const x = parseFloat(box.getAttribute('data-x'));
        const y = parseFloat(box.getAttribute('data-y'));
        const width = parseFloat(box.getAttribute('data-width'));
        const height = parseFloat(box.getAttribute('data-height'));
        const name = box.getAttribute('data-name') || `Section ${index+1}`;
        
        // Ensure we have valid numbers
        if (isNaN(x) || isNaN(y) || isNaN(width) || isNaN(height)) {
            console.error('Invalid dimension data for section box', index, box);
            return;
        }
        
        console.log(`Section box ${index} (${name}):`, { x, y, width, height });
        
        // Apply styles directly - convert decimal values (0-1) to percentages
        // The values in the database are stored as decimals, not percentages
        box.style.left = (x * 100) + '%';
        box.style.top = (y * 100) + '%';
        box.style.width = (width * 100) + '%';
        box.style.height = (height * 100) + '%';
        box.style.backgroundColor = `hsl(${(index * 60) % 360}, 70%, 85%)`;
        
        // Add section number for debugging
        const label = document.createElement('div');
        label.className = 'section-label absolute top-0 right-0 px-1 bg-white text-xs font-bold rounded-bl';
        label.textContent = `#${index+1}`;
        box.appendChild(label);
    });
}
