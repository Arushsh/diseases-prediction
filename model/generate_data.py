import pandas as pd
import numpy as np
import os

def generate_parkinsons_data(n=500):
    np.random.seed(42)
    # Status: 0 = healthy, 1 = Parkinson's
    status = np.random.choice([0, 1], size=n, p=[0.25, 0.75])
    
    # Generate features with some correlation to status
    avg_f0 = np.random.normal(150, 40, n) - status * 20
    jitter = np.random.normal(0.006, 0.003, n) + status * 0.005
    shimmer = np.random.normal(0.03, 0.015, n) + status * 0.02
    nhr = np.random.normal(0.02, 0.01, n) + status * 0.01
    hnr = np.random.normal(25, 5, n) - status * 10
    rpde = np.random.normal(0.5, 0.1, n) + status * 0.1
    dfa = np.random.normal(0.7, 0.05, n) + status * 0.05
    spread1 = np.random.normal(-5, 1, n) + status * 2
    age = np.random.randint(40, 85, n)
    
    df = pd.DataFrame({
        'avg_f0': avg_f0,
        'jitter': jitter.clip(0, 0.1),
        'shimmer': shimmer.clip(0, 0.2),
        'nhr': nhr.clip(0, 0.1),
        'hnr': hnr.clip(0, 40),
        'rpde': rpde.clip(0, 1),
        'dfa': dfa.clip(0, 1),
        'spread1': spread1,
        'age': age,
        'status': status
    })
    
    df.to_csv('../parkinsons.csv', index=False)
    print(f"✅ Generated parkinsons.csv with {n} rows")

def generate_breast_cancer_data(n=500):
    np.random.seed(42)
    # Diagnosis: 0 = Benign, 1 = Malignant
    diagnosis = np.random.choice([0, 1], size=n, p=[0.63, 0.37])
    
    # Generate features
    radius = np.random.normal(14, 3, n) + diagnosis * 4
    texture = np.random.normal(19, 4, n) + diagnosis * 3
    perimeter = radius * 6.3 # rough approximation
    area = np.pi * (radius**2)
    smoothness = np.random.normal(0.1, 0.01, n) + diagnosis * 0.02
    compactness = np.random.normal(0.1, 0.05, n) + diagnosis * 0.05
    concavity = np.random.normal(0.08, 0.05, n) + diagnosis * 0.08
    concave_points = np.random.normal(0.05, 0.03, n) + diagnosis * 0.04
    symmetry = np.random.normal(0.18, 0.02, n) + diagnosis * 0.02
    fractal_dim = np.random.normal(0.06, 0.01, n)
    
    df = pd.DataFrame({
        'radius_mean': radius,
        'texture_mean': texture,
        'perimeter_mean': perimeter,
        'area_mean': area,
        'smoothness_mean': smoothness,
        'compactness_mean': compactness,
        'concavity_mean': concavity,
        'concave_points_mean': concave_points,
        'symmetry_mean': symmetry,
        'fractal_dimension_mean': fractal_dim,
        'diagnosis': diagnosis
    })
    
    df.to_csv('../breast_cancer.csv', index=False)
    print(f"✅ Generated breast_cancer.csv with {n} rows")

if __name__ == "__main__":
    generate_parkinsons_data()
    generate_breast_cancer_data()
