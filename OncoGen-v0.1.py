import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from faker import Faker

# Initialize Faker
fake = Faker()

# Constants
NUM_PATIENTS = 4900000
LUNG_CANCER_RATIO = 2.1 / (2.1 + 1.8 + 1.0)
COLORECTAL_CANCER_RATIO = 1.8 / (2.1 + 1.8 + 1.0)
STOMACH_CANCER_RATIO = 1.0 / (2.1 + 1.8 + 1.0)

# Generate Patient IDs
patient_ids = np.arange(1, NUM_PATIENTS + 1)

# Generate Cancer Types
cancer_types = np.random.choice(
    ['lung', 'colorectal', 'stomach'], 
    size=NUM_PATIENTS, 
    p=[LUNG_CANCER_RATIO, COLORECTAL_CANCER_RATIO, STOMACH_CANCER_RATIO]
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
    elif cancer_type == 'colorectal':
        treatment = np.random.choice(['surgery', 'chemotherapy', 'radiation', 'combination'], p=[0.4, 0.3, 0.1, 0.2])
        medication = np.random.choice(['5-FU', 'capecitabine', 'oxaliplatin', 'bevacizumab'], p=[0.3, 0.3, 0.2, 0.2])
        if treatment == 'surgery':
            base_survival_rate = 0.90 if ages[i] < 70 else 0.80
        elif medication == 'oxaliplatin':
            base_survival_rate = 0.60
        else:
            base_survival_rate = 0.65
    elif cancer_type == 'stomach':
        treatment = np.random.choice(['surgery', 'chemotherapy', 'radiation', 'combination'], p=[0.3, 0.3, 0.2, 0.2])
        medication = np.random.choice(['fluorouracil', 'cisplatin', 'capecitabine', 'trastuzumab'], p=[0.3, 0.3, 0.2, 0.2])
        if treatment == 'surgery':
            base_survival_rate = 0.70
        elif medication == 'trastuzumab':
            base_survival_rate = 0.40
        else:
            base_survival_rate = 0.31

    adjusted_survival_rate = base_survival_rate * comorbidity_factor
    outcomes.append('survived' if np.random.rand() < adjusted_survival_rate else 'deceased')

    treatments.append(treatment)
    medications.append(medication)

# Create DataFrame
data = pd.DataFrame({
    'patient_id': patient_ids,
    'cancer_type': cancer_types,
    'age': ages,
    'gender': genders,
    'smoking_status': smoking_status,
    'country': countries,
    'treatment': treatments,
    'medication': medications,
    'outcome': outcomes,
    'comorbidities': comorbidities
})

# Save to CSV
data.to_csv('synthetic_oncology_data.csv', index=False)

# Save to Parquet
table = pa.Table.from_pandas(data)
pq.write_table(table, 'synthetic_oncology_data.parquet')

print("Synthetic oncology data generated and saved to 'synthetic_oncology_data.csv' and 'synthetic_oncology_data.parquet'.")
