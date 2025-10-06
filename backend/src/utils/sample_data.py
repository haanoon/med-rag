"""
Sample medical data for MVP demonstration
This file contains sample medical Q&A pairs and facts for testing
"""

SAMPLE_MEDICAL_DATA = [
    {
        "question": "What is diabetes?",
        "answer": "Diabetes is a chronic health condition that affects how your body turns food into energy. Most of the food you eat is broken down into sugar (glucose) and released into your bloodstream. When your blood sugar goes up, it signals your pancreas to release insulin. Insulin acts like a key to let the blood sugar into your body's cells for use as energy.",
        "metadata": {"category": "disease", "source": "medical_textbook"}
    },
    {
        "question": "What are the symptoms of hypertension?",
        "answer": "Hypertension (high blood pressure) often has no symptoms. However, some people may experience headaches, shortness of breath, or nosebleeds. These symptoms aren't specific and usually don't occur until high blood pressure has reached a severe or life-threatening stage. Regular blood pressure checks are important for early detection.",
        "metadata": {"category": "symptoms", "source": "clinical_guidelines"}
    },
    {
        "question": "What is aspirin used for?",
        "answer": "Aspirin is a common medication used to reduce pain, fever, and inflammation. It's also used in low doses to prevent heart attacks and strokes in people at high risk. Aspirin works by blocking the production of certain natural substances that cause inflammation and blood clotting.",
        "metadata": {"category": "drug", "source": "pharmacology"}
    },
    {
        "question": "How is Type 2 diabetes treated?",
        "answer": "Type 2 diabetes is typically treated with lifestyle changes first, including healthy eating, regular physical activity, and weight loss. If lifestyle changes aren't enough, diabetes medications or insulin therapy may be prescribed. Metformin is usually the first medication prescribed. Blood sugar monitoring is essential for managing the condition.",
        "metadata": {"category": "treatment", "source": "clinical_guidelines"}
    },
    {
        "question": "What are the side effects of ibuprofen?",
        "answer": "Common side effects of ibuprofen include upset stomach, heartburn, nausea, vomiting, gas, diarrhea, and dizziness. More serious side effects can include stomach bleeding, kidney problems, high blood pressure, and heart problems. Taking ibuprofen with food can help reduce stomach upset.",
        "metadata": {"category": "side_effects", "source": "drug_database"}
    },
    {
        "question": "What causes pneumonia?",
        "answer": "Pneumonia is an infection that inflames air sacs in one or both lungs, which may fill with fluid. It can be caused by various organisms including bacteria (most commonly Streptococcus pneumoniae), viruses (such as influenza), and fungi. Bacterial pneumonia is the most common form. Risk factors include age, smoking, weakened immune system, and chronic diseases.",
        "metadata": {"category": "disease", "source": "infectious_diseases"}
    },
    {
        "question": "How to diagnose high cholesterol?",
        "answer": "High cholesterol is diagnosed through a blood test called a lipid panel or lipid profile. This test measures total cholesterol, LDL (bad) cholesterol, HDL (good) cholesterol, and triglycerides. Adults should have their cholesterol checked every 4-6 years. The test requires fasting for 9-12 hours before blood is drawn.",
        "metadata": {"category": "diagnosis", "source": "lab_procedures"}
    },
    {
        "question": "What is the flu vaccine?",
        "answer": "The flu vaccine is an annual vaccine that protects against influenza viruses. It stimulates the immune system to produce antibodies against flu viruses. The vaccine is reformulated each year to match circulating strains. It's recommended for everyone 6 months and older. Common side effects include soreness at injection site, low-grade fever, and muscle aches.",
        "metadata": {"category": "prevention", "source": "immunology"}
    },
    {
        "question": "What are antibiotics?",
        "answer": "Antibiotics are medications used to treat bacterial infections by either killing bacteria or preventing them from reproducing. They work in various ways - some break down bacterial cell walls, others interfere with protein synthesis. Antibiotics are not effective against viral infections like the common cold or flu. Misuse can lead to antibiotic resistance.",
        "metadata": {"category": "drug", "source": "pharmacology"}
    },
    {
        "question": "What is a heart attack?",
        "answer": "A heart attack (myocardial infarction) occurs when blood flow to part of the heart is blocked, usually by a blood clot. This prevents oxygen from reaching heart tissue, causing damage or death to heart muscle. Common symptoms include chest pain or discomfort, shortness of breath, nausea, and pain in the arms, back, neck, or jaw. Immediate medical attention is critical.",
        "metadata": {"category": "emergency", "source": "cardiology"}
    },
    {
        "question": "What is asthma?",
        "answer": "Asthma is a chronic respiratory condition where airways become inflamed, narrow, and produce extra mucus, making breathing difficult. Symptoms include wheezing, coughing, chest tightness, and shortness of breath. Triggers can include allergens, exercise, cold air, and respiratory infections. Treatment typically involves inhaled corticosteroids and bronchodilators.",
        "metadata": {"category": "disease", "source": "respiratory_medicine"}
    },
    {
        "question": "What is blood pressure?",
        "answer": "Blood pressure is the force of blood pushing against artery walls as the heart pumps blood. It's measured in millimeters of mercury (mmHg) and recorded as two numbers: systolic pressure (when heart beats) over diastolic pressure (when heart rests). Normal blood pressure is less than 120/80 mmHg. High blood pressure increases risk of heart disease and stroke.",
        "metadata": {"category": "physiology", "source": "medical_textbook"}
    },
    {
        "question": "How does insulin work?",
        "answer": "Insulin is a hormone produced by the pancreas that regulates blood sugar levels. When you eat, blood sugar rises, signaling the pancreas to release insulin. Insulin acts like a key, allowing glucose to enter cells for energy or storage. In diabetes, the body either doesn't produce enough insulin (Type 1) or can't use it effectively (Type 2).",
        "metadata": {"category": "physiology", "source": "endocrinology"}
    },
    {
        "question": "What is arthritis?",
        "answer": "Arthritis is inflammation of one or more joints, causing pain and stiffness. The two most common types are osteoarthritis (wear-and-tear damage to cartilage) and rheumatoid arthritis (autoimmune disorder). Symptoms include joint pain, stiffness, swelling, and decreased range of motion. Treatment includes medications, physical therapy, and sometimes surgery.",
        "metadata": {"category": "disease", "source": "rheumatology"}
    },
    {
        "question": "What is the immune system?",
        "answer": "The immune system is the body's defense mechanism against infections and diseases. It consists of white blood cells, antibodies, the lymphatic system, spleen, thymus, and bone marrow. It identifies and destroys pathogens like bacteria, viruses, and parasites. A healthy immune system can distinguish between self and foreign cells.",
        "metadata": {"category": "physiology", "source": "immunology"}
    }
]


SAMPLE_KG_DATA = {
    "entities": [
        {"type": "Disease", "id": "diabetes", "name": "Diabetes", "description": "Chronic metabolic disorder"},
        {"type": "Disease", "id": "hypertension", "name": "Hypertension", "description": "High blood pressure"},
        {"type": "Disease", "id": "pneumonia", "name": "Pneumonia", "description": "Lung infection"},
        {"type": "Disease", "id": "asthma", "name": "Asthma", "description": "Chronic respiratory condition"},
        {"type": "Drug", "id": "aspirin", "name": "Aspirin", "description": "Pain reliever and anti-inflammatory"},
        {"type": "Drug", "id": "ibuprofen", "name": "Ibuprofen", "description": "Nonsteroidal anti-inflammatory drug"},
        {"type": "Drug", "id": "metformin", "name": "Metformin", "description": "Diabetes medication"},
        {"type": "Drug", "id": "insulin", "name": "Insulin", "description": "Hormone for blood sugar regulation"},
        {"type": "Symptom", "id": "headache", "name": "Headache", "description": "Pain in the head"},
        {"type": "Symptom", "id": "fever", "name": "Fever", "description": "Elevated body temperature"},
        {"type": "Symptom", "id": "cough", "name": "Cough", "description": "Respiratory reflex"},
        {"type": "Symptom", "id": "chest_pain", "name": "Chest Pain", "description": "Pain in chest area"},
    ],
    "relationships": [
        {"from": "metformin", "to": "diabetes", "type": "TREATS", "from_type": "Drug", "to_type": "Disease"},
        {"from": "insulin", "to": "diabetes", "type": "TREATS", "from_type": "Drug", "to_type": "Disease"},
        {"from": "aspirin", "to": "headache", "type": "TREATS", "from_type": "Drug", "to_type": "Symptom"},
        {"from": "ibuprofen", "to": "fever", "type": "TREATS", "from_type": "Drug", "to_type": "Symptom"},
        {"from": "diabetes", "to": "fever", "type": "HAS_SYMPTOM", "from_type": "Disease", "to_type": "Symptom"},
        {"from": "pneumonia", "to": "cough", "type": "HAS_SYMPTOM", "from_type": "Disease", "to_type": "Symptom"},
        {"from": "pneumonia", "to": "fever", "type": "HAS_SYMPTOM", "from_type": "Disease", "to_type": "Symptom"},
        {"from": "asthma", "to": "cough", "type": "HAS_SYMPTOM", "from_type": "Disease", "to_type": "Symptom"},
    ]
}
