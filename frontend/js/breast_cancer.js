document.getElementById('bcForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const form = e.target;
    const loading = document.getElementById('loading');
    const resultDisplay = document.getElementById('resultDisplay');
    
    // Get form data
    const data = [
        parseFloat(document.getElementById('radius').value),
        parseFloat(document.getElementById('texture').value),
        parseFloat(document.getElementById('perimeter').value),
        parseFloat(document.getElementById('area').value),
        parseFloat(document.getElementById('smoothness').value),
        parseFloat(document.getElementById('compactness').value),
        parseFloat(document.getElementById('concavity').value),
        parseFloat(document.getElementById('concave_points').value),
        parseFloat(document.getElementById('symmetry').value),
        parseFloat(document.getElementById('fractal_dim').value)
    ];

    const saveToDB = document.getElementById('saveToDB').checked;

    // Show loading
    form.style.display = 'none';
    loading.style.display = 'block';

    try {
        const result = await API.predictBreastCancer(data);
        
        loading.style.display = 'none';
        resultDisplay.classList.add('show');

        // Update result display
        const prob = (result.probability * 100).toFixed(1);
        const isHighRisk = result.result === 1;

        document.getElementById('resultProb').textContent = prob + '%';
        document.getElementById('resultProb').style.color = isHighRisk ? 'var(--danger)' : 'var(--success)';
        
        const icon = document.getElementById('resultIcon');
        const title = document.getElementById('resultTitle');
        const message = document.getElementById('resultMessage');

        if (isHighRisk) {
            icon.className = 'bi bi-exclamation-octagon-fill';
            icon.style.color = 'var(--danger)';
            title.textContent = 'Malignant Risk Detected';
            message.textContent = 'Our analysis indicates a high probability of malignancy (cancerous) based on the diagnostic parameters. Immediate consultation with an oncologist and further testing (e.g., biopsy confirmation) is critical.';
        } else {
            icon.className = 'bi bi-shield-check';
            icon.style.color = 'var(--success)';
            title.textContent = 'Benign Assessment';
            message.textContent = 'Our analysis indicates a low probability of malignancy. The features suggest a benign (non-cancerous) condition. However, always follow your doctor\'s advice for follow-up care.';
        }

    } catch (error) {
        console.error('Error predicting breast cancer:', error);
        form.style.display = 'block';
        loading.style.display = 'none';
        alert('An error occurred during risk analysis. Please check your backend connection.');
    }
});
