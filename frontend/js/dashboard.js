/**
 * Dashboard Logic for HealthSense AI
 */

document.addEventListener('DOMContentLoaded', async () => {
    const totalPredictionsEl = document.getElementById('totalPredictions');
    const highRiskCountEl = document.getElementById('highRiskCount');
    const avgProbabilityEl = document.getElementById('avgProbability');
    const recentPredictionsBody = document.getElementById('recentPredictionsBody');

    try {
        // 1. Fetch Statistics
        const stats = await API.getStatistics();
        totalPredictionsEl.textContent = stats.total_predictions;
        
        const highRiskTotal = (stats.positive_diabetes || 0) + 
                             (stats.positive_heart || 0) + 
                             (stats.positive_parkinsons || 0) + 
                             (stats.positive_breast_cancer || 0);
        highRiskCountEl.textContent = highRiskTotal;

        const avgProb = ((stats.avg_diabetes_probability + 
                         stats.avg_heart_probability + 
                         stats.avg_parkinsons_probability + 
                         stats.avg_breast_cancer_probability) / 4 * 100).toFixed(1);
        avgProbabilityEl.textContent = avgProb + '%';

        // 2. Fetch Recent Predictions
        const recent = await API.getRecentPredictions(10);
        renderRecentPredictions(recent.data);

        // 3. Initialize Chart
        renderTrendChart(recent.data);

    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
});

function renderRecentPredictions(predictions) {
    const body = document.getElementById('recentPredictionsBody');
    body.innerHTML = '';

    predictions.forEach(p => {
        const row = document.createElement('tr');
        row.style.borderBottom = '1px solid rgba(255,255,255,0.05)';
        
        const date = new Date(p.PredictionDate).toLocaleDateString();
        
        let model = 'Unknown';
        let result = 0;
        let prob = 0;
        
        if (p.DiabetesProbability !== null) { model = 'Diabetes'; result = p.DiabetesResult; prob = p.DiabetesProbability; }
        else if (p.HeartProbability !== null) { model = 'Heart'; result = p.HeartResult; prob = p.HeartProbability; }
        else if (p.ParkinsonsProbability !== null) { model = 'Parkinson\'s'; result = p.ParkinsonsResult; prob = p.ParkinsonsProbability; }
        else if (p.BreastCancerProbability !== null) { model = 'Breast Cancer'; result = p.BreastCancerResult; prob = p.BreastCancerProbability; }

        const isHighRisk = result === 1 || result === true;
        const riskLevel = isHighRisk ? 'High' : 'Low';
        const riskColor = isHighRisk ? 'var(--danger)' : 'var(--success)';

        row.innerHTML = `
            <td style="padding: 1rem;">${date}</td>
            <td style="padding: 1rem;">${model}</td>
            <td style="padding: 1rem;">${isHighRisk ? 'Positive' : 'Negative'}</td>
            <td style="padding: 1rem;">${(prob * 100).toFixed(1)}%</td>
            <td style="padding: 1rem; color: ${riskColor}; font-weight: bold;">${riskLevel}</td>
        `;
        body.appendChild(row);
    });
}

function renderTrendChart(data) {
    const ctx = document.getElementById('trendChart').getContext('2d');
    
    // Reverse data to show chronological order
    const chartData = [...data].reverse();
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.map(d => new Date(d.PredictionDate).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})),
            datasets: [{
                label: 'Risk Probability (%)',
                data: chartData.map(d => {
                    const p = d.DiabetesProbability ?? d.HeartProbability ?? d.ParkinsonsProbability ?? d.BreastCancerProbability ?? 0;
                    return (p * 100).toFixed(1);
                }),
                borderColor: '#6366f1',
                backgroundColor: 'rgba(99, 102, 241, 0.1)',
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointBackgroundColor: '#6366f1'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: { color: 'rgba(255,255,255,0.05)' },
                    ticks: { color: 'rgba(255,255,255,0.5)' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: 'rgba(255,255,255,0.5)' }
                }
            }
        }
    });
}
