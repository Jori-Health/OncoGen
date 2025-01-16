import os
import numpy as np
import pandas as pd
import h5py
from faker import Faker

# Initialize Faker
fake = Faker()

# Constants
NUM_PATIENTS = 10
LUNG_CANCER_RATIO = 0.25
BREAST_CANCER_RATIO = 0.30
LEUKEMIA_CANCER_RATIO = 0.15
COLORECTAL_CANCER_RATIO = 0.30
GENES = ['BRCA1', 'BRCA2', 'TP53', 'EGFR', 'KRAS', 'ALK', 'PIK3CA', 'PTEN', 'RB1', 'NRAS']

# Ensure the ratios sum to 1
assert abs((LUNG_CANCER_RATIO + BREAST_CANCER_RATIO + LEUKEMIA_CANCER_RATIO + COLORECTAL_CANCER_RATIO) - 1.0) < 1e-6, "Ratios must sum to 1."

# Generate Cancer Types
cancer_types = np.random.choice(
    ['lung', 'breast', 'leukemia', 'colorectal'], 
    size=NUM_PATIENTS, 
    p=[LUNG_CANCER_RATIO, BREAST_CANCER_RATIO, LEUKEMIA_CANCER_RATIO, COLORECTAL_CANCER_RATIO]
)

# Generate Demographics
ages = np.random.normal(loc=65, scale=10, size=NUM_PATIENTS).astype(int)
ages = np.clip(ages, 18, 90)
genders = np.random.choice(['male', 'female'], size=NUM_PATIENTS)
smoking_status = np.where(cancer_types == 'lung', np.random.choice(['current', 'former', 'never'], size=NUM_PATIENTS, p=[0.4, 0.4, 0.2]), 'never')
countries = np.random.choice(['US', 'China', 'India', 'Japan', 'Germany', 'UK'], size=NUM_PATIENTS)

# Generate Comorbidities and Adjust Survival Rates
comorbidities = []
comorbidity_factors = []

for i in range(NUM_PATIENTS):
    num_comorbidities = np.random.poisson(2)
    patient_comorbidities = fake.words(nb=num_comorbidities, ext_word_list=['hypertension', 'diabetes', 'COPD', 'cardiovascular disease', 'chronic kidney disease'])
    comorbidities.append(','.join(patient_comorbidities))
    comorbidity_factor = 1.0 - 0.05 * num_comorbidities  # Each comorbidity reduces survival probability by 5%
    comorbidity_factors.append(comorbidity_factor)

# Generate Treatments, Medications, and Outcomes with Comorbidity Impact
treatments = []
medications = []
outcomes = []
gene_mutations_list = []  # New list to store gene mutations for each patient

for i in range(NUM_PATIENTS):
    cancer_type = cancer_types[i]
    comorbidity_factor = comorbidity_factors[i]

    if cancer_type == 'lung':
        treatment = np.random.choice(['surgery', 'chemotherapy', 'radiation', 'combination'], p=[0.2, 0.4, 0.2, 0.2])
        medication = np.random.choice(['cisplatin', 'carboplatin', 'paclitaxel', 'osimertinib'], p=[0.3, 0.3, 0.2, 0.2])
        if treatment == 'surgery':
            base_survival_rate = 0.50
        elif treatment == 'chemotherapy' and medication in ['cisplatin', 'carboplatin']:
            base_survival_rate = 0.20
        elif medication == 'osimertinib':
            base_survival_rate = 0.40
        else:
            base_survival_rate = 0.19
    elif cancer_type == 'breast':
        treatment = np.random.choice(['surgery', 'chemotherapy', 'radiation', 'combination'], p=[0.3, 0.3, 0.2, 0.2])
        medication = np.random.choice(['tamoxifen', 'anastrozole', 'letrozole', 'trastuzumab'], p=[0.3, 0.3, 0.2, 0.2])
        if treatment == 'surgery':
            base_survival_rate = 0.85
        elif medication == 'trastuzumab':
            base_survival_rate = 0.70
        else:
            base_survival_rate = 0.60
    elif cancer_type == 'leukemia':
        treatment = np.random.choice(['chemotherapy', 'radiation', 'stem cell transplant'], p=[0.5, 0.2, 0.3])
        medication = np.random.choice(['imatinib', 'dasatinib', 'nilotinib', 'bosutinib'], p=[0.3, 0.3, 0.2, 0.2])
        if treatment == 'stem cell transplant':
            base_survival_rate = 0.60
        else:
            base_survival_rate = 0.50
    elif cancer_type == 'colorectal':
        treatment = np.random.choice(['surgery', 'chemotherapy', 'radiation', 'combination'], p=[0.4, 0.3, 0.1, 0.2])
        medication = np.random.choice(['5-FU', 'capecitabine', 'oxaliplatin', 'bevacizumab'], p=[0.3, 0.3, 0.2, 0.2])
        if treatment == 'surgery':
            base_survival_rate = 0.90 if ages[i] < 70 else 0.80
        elif medication == 'oxaliplatin':
            base_survival_rate = 0.60
        else:
            base_survival_rate = 0.65

    adjusted_survival_rate = base_survival_rate * comorbidity_factor
    outcomes.append('survived' if np.random.rand() < adjusted_survival_rate else 'deceased')

    treatments.append(treatment)
    medications.append(medication)

# Create DATA directory if it doesn't exist
os.makedirs('DATA', exist_ok=True)

# Generate Patient Data with NGS Information
patient_data = []

for patient_id in range(NUM_PATIENTS):
    # Generate synthetic gene mutations for each patient
    num_mutations = np.random.randint(1, 5)  # Each patient has 1 to 4 mutations
    mutations = np.random.choice(GENES, size=num_mutations, replace=False)
    patient_data.append({
        'patient_id': patient_id,
        'mutations': ','.join(mutations)
    })
    gene_mutations_list.append(','.join(mutations))  # Add mutations to the list for CSV

    # Generate synthetic NGS data and store in HDF5
    with h5py.File(f'DATA/patient_{patient_id}.h5', 'w') as h5file:
        # Create a dataset for gene mutations using special string dtype
        dt = h5py.string_dtype(encoding='utf-8')
        h5file.create_dataset('mutations', data=mutations.astype(dt))

        # Optionally, add more datasets for other NGS data aspects
        # For example, synthetic read data
        reads = np.random.randint(0, 100, size=(100, 4))  # 100 reads with 4 bases each
        h5file.create_dataset('reads', data=reads)

        # Add metadata
        h5file.attrs['patient_id'] = patient_id

# Save patient data to CSV
patient_df = pd.DataFrame(patient_data)
patient_df.to_csv('DATA/patient_data.csv', index=False)

# Save original patient data to CSV with gene mutations
data = pd.DataFrame({
    'patient_id': np.arange(NUM_PATIENTS),
    'cancer_type': cancer_types,
    'age': ages,
    'gender': genders,
    'smoking_status': smoking_status,
    'country': countries,
    'treatment': treatments,
    'medication': medications,
    'outcome': outcomes,
    'comorbidities': comorbidities,
    'gene_mutations': gene_mutations_list  # New field for gene mutations
})

data.to_csv('DATA/synthetic_oncology_data.csv', index=False)

print("Synthetic oncology and NGS data generated and saved in the DATA directory.")
