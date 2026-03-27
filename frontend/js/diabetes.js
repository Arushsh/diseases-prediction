document.getElementById('diabetesForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const form = e.target;
    const loading = document.getElementById('loading');
    const resultDisplay = document.getElementById('resultDisplay');
    
    // Get form data
    const data = [
        parseFloat(document.getElementById('pregnancies').value),
        parseFloat(document.getElementById('glucose').value),
        parseFloat(document.getElementById('bp').value),
        parseFloat(document.getElementById('skin').value),
        parseFloat(document.getElementById('insulin').value),
        parseFloat(document.getElementById('bmi').value),
        parseFloat(document.getElementById('pedigree').value),
        parseFloat(document.getElementById('age').value)
    ];

    const saveToDB = document.getElementById('saveToDB').checked;

    // Show loading
    form.style.display = 'none';
    loading.style.display = 'block';

    try {
        const result = await API.predictDiabetes(data);
        
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
            title.textContent = 'High Risk Detected';
            message.textContent = 'Our AI model indicates a high probability of diabetes. We strongly recommend consulting a healthcare professional for clinical validation and further testing.';
        } else {
            icon.className = 'bi bi-check-circle-fill';
            icon.style.color = 'var(--success)';
            title.textContent = 'Low Risk Assessment';
            message.textContent = 'Our AI model indicates a low probability of diabetes based on the parameters provided. However, maintaining a healthy lifestyle is always recommended.';
        }

    } catch (error) {
        console.error('Error predicting diabetes:', error);
        form.style.display = 'block';
        loading.style.display = 'none';
        alert('An error occurred during risk analysis. Please check your backend connection.');
    }
});
