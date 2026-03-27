document.getElementById('heartForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const form = e.target;
    const loading = document.getElementById('loading');
    const resultDisplay = document.getElementById('resultDisplay');
    
    // Get form data in the exact order expected by the backend
    const data = [
        parseFloat(document.getElementById('age').value),
        parseFloat(document.getElementById('sex').value),
        parseFloat(document.getElementById('cp').value),
        parseFloat(document.getElementById('trestbps').value),
        parseFloat(document.getElementById('chol').value),
        parseFloat(document.getElementById('fbs').value),
        parseFloat(document.getElementById('restecg').value),
        parseFloat(document.getElementById('thalach').value),
        parseFloat(document.getElementById('exang').value),
        parseFloat(document.getElementById('oldpeak').value),
        parseFloat(document.getElementById('slope').value),
        parseFloat(document.getElementById('ca').value),
        parseFloat(document.getElementById('thal').value)
    ];

    const saveToDB = document.getElementById('saveToDB').checked;

    // Show loading
    form.style.display = 'none';
    loading.style.display = 'block';

    try {
        const result = await API.predictHeart(data);
        
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
            icon.className = 'bi bi-heart-pulse-fill';
            icon.style.color = 'var(--danger)';
            title.textContent = 'High Cardiac Risk';
            message.textContent = 'Our analysis indicates a high risk of cardiovascular disease based on the clinical parameters provided. We strongly advice consulting a cardiologist immediately for a professional evaluation.';
        } else {
            icon.className = 'bi bi-heart-fill';
            icon.style.color = 'var(--success)';
            title.textContent = 'Low Cardiac Risk';
            message.textContent = 'Our analysis indicates a low risk of heart disease. Continuing regular exercise and a balanced diet will help maintain your cardiovascular health.';
        }

    } catch (error) {
        console.error('Error predicting heart disease:', error);
        form.style.display = 'block';
        loading.style.display = 'none';
        alert('An error occurred during heart risk analysis. Please check your backend connection.');
    }
});
