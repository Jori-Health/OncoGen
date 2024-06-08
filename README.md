# OncoGen
Best-in-class Oncology dataset generator that mirrors reality as much as possible. Synthetic data is the next-best-thing if you wanted to experiment with AI and/or decentralized storage. 

# Dataset Overview
Dataset covers three major types of cancer: lung, colorectal, and stomach cancers. It includes 4.9 million records, reflecting detailed patient demographics, treatments, medications, real-world outcomes, and comorbidities. This dataset is stored in both CSV and Parquet formats, making it suitable for various data processing and machine learning workflows.

**Cancer Types and Distribution**
The dataset is designed with the following proportions, based on global incidence rates:

Lung cancer: 2.1 million records (approx. 42.86%)
Colorectal cancer: 1.8 million records (approx. 36.73%)
Stomach cancer: 1.0 million records (approx. 20.41%)

**Ground Truths Reflected in the Data**
Understanding the ground truths embedded in this dataset is crucial for accurate interpretation and validation of AI models.


**Demographics**
Age: Normal distribution around 65 years, range 18-90.
Gender: Approximately equal distribution.
Smoking Status: 40% current, 40% former, 20% never for lung cancer; 'never' for others.
Countries: Major countries reflecting global distribution.
**Treatments and Medications**
Lung Cancer: Surgery (50% survival), chemotherapy (cisplatin, carboplatin - 20%), targeted therapy (osimertinib - 40%).
Colorectal Cancer: Surgery (90% survival under 70, 80% over 70), chemotherapy (oxaliplatin - 60%).
Stomach Cancer: Surgery (70% survival), targeted therapy (trastuzumab - 40%).
**Real-World Outcomes**
Survival Rates: Adjusted for comorbidities, each reducing survival probability by 5%.
**Comorbidities:**
Average of 2 per patient, impacting survival outcomes.




# How does OncoGen approach random distribution?

**Demographics**
To ensure realistic representation, the dataset includes:

Age: Normally distributed around 65 years, with a range of 18 to 90 years.
Gender: Approximately equal distribution between males and females.
Smoking Status: For lung cancer patients, 40% are current smokers, 40% are former smokers, and 20% have never smoked. Other cancer types are marked as 'never' smokers.
Countries: Randomly assigned from a list of major countries, reflecting a global patient base.

**Treatments and Medications: Each cancer type is associated with common treatments and medications:**
Lung Cancer: Includes surgery, chemotherapy (cisplatin, carboplatin, paclitaxel), targeted therapy (osimertinib), and immunotherapy (pembrolizumab).
Colorectal Cancer: Includes surgery, chemotherapy (5-FU, capecitabine, oxaliplatin), and targeted therapy (bevacizumab).
Stomach Cancer: Includes surgery, chemotherapy (fluorouracil, cisplatin, capecitabine), and targeted therapy (trastuzumab).

**Real-World Outcomes (survival rates adjusted for comorbidities):**
Lung Cancer: Overall survival rate of 19%, with specific rates for treatments such as 50% for surgery and 40% for osimertinib.
Colorectal Cancer: Overall survival rate of 65%, with 90% for surgery in patients under 70.
Stomach Cancer: Overall survival rate of 31%, with 70% for surgery.
Each comorbidity reduces the survival probability by 5%.

**Comorbidities**
Patients typically have an average of 2 comorbid conditions, randomly selected from a list including hypertension, diabetes, COPD, cardiovascular disease, and chronic kidney disease.
