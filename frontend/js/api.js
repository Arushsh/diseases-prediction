/**
 * API Utility for HealthSense Dashboard
 */
const API_BASE_URL = 'http://127.0.0.1:5000/api';

const API = {
    /**
     * Fetch dashboard statistics
     */
    async getStatistics() {
        const response = await fetch(`${API_BASE_URL}/statistics`);
        if (!response.ok) throw new Error('Failed to fetch statistics');
        return await response.json();
    },

    /**
     * Predict Diabetes
     * @param {Array} data - [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigree, Age]
     */
    async predictDiabetes(data) {
        const response = await fetch(`${API_BASE_URL}/predict/diabetes`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ diabetes: data })
        });
        if (!response.ok) throw new Error('Diabetes prediction failed');
        return await response.json();
    },

    /**
     * Predict Heart Disease
     * @param {Array} data - [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
     */
    async predictHeart(data) {
        const response = await fetch(`${API_BASE_URL}/predict/heart`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ heart: data })
        });
        if (!response.ok) throw new Error('Heart disease prediction failed');
        return await response.json();
    },

    /**
     * Predict Parkinson's Disease
     * @param {Array} data - [avg_f0, jitter, shimmer, nhr, hnr, rpde, dfa, spread1, age]
     */
    async predictParkinsons(data) {
        const response = await fetch(`${API_BASE_URL}/predict/parkinsons`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ parkinsons: data })
        });
        if (!response.ok) throw new Error('Parkinsons prediction failed');
        return await response.json();
    },

    /**
     * Predict Breast Cancer
     * @param {Array} data - [radius, texture, perimeter, area, smoothness, compactness, concavity, concave_points, symmetry, fractal_dim]
     */
    async predictBreastCancer(data) {
        const response = await fetch(`${API_BASE_URL}/predict/breast_cancer`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ breast_cancer: data })
        });
        if (!response.ok) throw new Error('Breast cancer prediction failed');
        return await response.json();
    },

    /**
     * Fetch recent predictions
     */
    async getRecentPredictions(limit = 10) {
        const response = await fetch(`${API_BASE_URL}/predictions?limit=${limit}`);
        if (!response.ok) throw new Error('Failed to fetch predictions');
        return await response.json();
    }
};
