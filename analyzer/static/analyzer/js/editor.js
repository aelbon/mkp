document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');
    // Initialize everything
    initEditableCells();
    applySectionBoxStyles();
    
    // Setup a mutation observer to detect when cells are updated
    const config = {
        previewUrlPattern: '/analyzer/document/{documentId}/preview/'
    };
    setupTableObserver();
});

function setupTableObserver() {
    // Create a mutation observer to watch for changes to the table
    const tableBody = document.querySelector('table tbody');
    if (!tableBody) return;
    
    console.log('Setting up table observer');
    
    // Observer that watches for changes to the DOM
    const observer = new MutationObserver(function(mutations) {
        console.log('Table mutation detected:', mutations);
        
        // Check if any mutation is related to our editable cells
        const cellChanged = mutations.some(mutation => {
            return mutation.target.classList && 
                   mutation.target.classList.contains('editable-cell');
        });
        
        if (cellChanged) {
            console.log('Cell content changed, refreshing preview');
            // Schedule a refresh of the preview
            setTimeout(directRefreshPreview, 200);
        }
    });
    
    // Start observing the table for DOM changes
    observer.observe(tableBody, { 
        childList: true,     // Watch for changes to child elements
        subtree: true,       // Watch all descendants
        characterData: true, // Watch for changes to text content
        attributes: true     // Watch for attribute changes
    });
}

function directRefreshPreview() {
    console.log('Performing direct preview refresh');
    
    // Get document ID from the table
    const table = document.querySelector('table');
    if (!table || !table.dataset.documentId) {
        console.error('Cannot refresh preview - table or document ID not found');
        return;
    }
    
    const documentId = table.dataset.documentId;
    const previewUrlPattern = config.previewUrlPattern;
    
    // Replace the placeholder with the actual document ID
    const previewUrl = previewUrlPattern.replace('{documentId}', documentId);
    
    console.log('Using preview URL:', previewUrl);
    
    const previewContainer = document.getElementById('preview-container');
    
    if (!previewContainer) {
        console.error('Preview container not found');
        return;
    }
    
    // Show loading indicator
    previewContainer.innerHTML = '<div class="flex items-center justify-center h-full"><p>Refreshing preview...</p></div>';
    
    // Fetch the preview HTML directly
    fetch(previewUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Failed to fetch preview: ${response.status}`);
            }
            return response.text();
        })
        .then(html => {
            previewContainer.innerHTML = html;
            console.log('Preview content updated');
            applySectionBoxStyles();
        })
        .catch(error => {
            console.error('Error refreshing preview:', error);
            previewContainer.innerHTML = '<div class="flex items-center justify-center h-full text-red-500"><p>Error refreshing preview</p></div>';
        });
}

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
            
            // Store original value and clear content
            const originalValue = this.dataset.originalValue || this.textContent.trim();
            const originalContent = this.innerHTML;
            
            // Create input element
            const input = document.createElement('input');
            input.type = 'text';
            input.value = originalValue;
            
            // Add editing class to cell
            this.classList.add('editing');
            
            // IMPORTANT: Completely clear the cell before adding the input
            this.innerHTML = '';
            this.appendChild(input);
            
            // Focus input
            input.focus();
            
            // Handle blur event (when focus is lost)
            input.addEventListener('blur', function() {
                finishEditing(cell, input, originalValue);
            });
            
            // Handle enter key
            input.addEventListener('keydown', function(e) {
                if (e.key === 'Enter') {
                    finishEditing(cell, input, originalValue);
                } else if (e.key === 'Escape') {
                    // Revert to original value and content on escape
                    cell.classList.remove('editing');
                    cell.innerHTML = originalContent;
                }
            });
        });
    });
}

function finishEditing(cell, input, originalValue) {
    // Get the new value
    const newValue = input.value.trim();
    
    // Remove editing class
    cell.classList.remove('editing');
    
    // Update cell content - completely replace innerHTML
    cell.innerHTML = newValue;
    
    // Only trigger custom event if value changed
    if (newValue !== originalValue) {
        // Update the original value
        cell.dataset.originalValue = newValue;
        
        // Trigger custom event to handle the edited cell
        cell.dispatchEvent(new CustomEvent('edited', {
            detail: { value: newValue }
        }));
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
        box.style.position = 'absolute';
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