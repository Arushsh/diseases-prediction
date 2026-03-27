document.getElementById('parkinsonsForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const form = e.target;
    const loading = document.getElementById('loading');
    const resultDisplay = document.getElementById('resultDisplay');
    
    // Get form data
    const data = [
        parseFloat(document.getElementById('avg_f0').value),
        parseFloat(document.getElementById('jitter').value),
        parseFloat(document.getElementById('shimmer').value),
        parseFloat(document.getElementById('nhr').value),
        parseFloat(document.getElementById('hnr').value),
        parseFloat(document.getElementById('rpde').value),
        parseFloat(document.getElementById('dfa').value),
        parseFloat(document.getElementById('spread1').value),
        parseFloat(document.getElementById('age').value)
    ];

    const saveToDB = document.getElementById('saveToDB').checked;

    // Show loading
    form.style.display = 'none';
    loading.style.display = 'block';

    try {
        const result = await API.predictParkinsons(data);
        
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
            icon.className = 'bi bi-exclamation-triangle-fill';
            icon.style.color = 'var(--danger)';
            title.textContent = 'Parkinsons Risk Detected';
            message.textContent = 'Our analysis indicates a high probability of Parkinson\'s disease based on the provided biomedical data. We recommend scheduling an appointment with a neurologist for further evaluation.';
        } else {
            icon.className = 'bi bi-check-circle-fill';
            icon.style.color = 'var(--success)';
            title.textContent = 'Low Risk Assessment';
            message.textContent = 'Our analysis indicates a low probability of Parkinson\'s disease. Regular health check-ups and monitoring are still advisable as you age.';
        }

    } catch (error) {
        console.error('Error predicting parkinsons:', error);
        form.style.display = 'block';
        loading.style.display = 'none';
        alert('An error occurred during risk analysis. Please check your backend connection.');
    }
});
