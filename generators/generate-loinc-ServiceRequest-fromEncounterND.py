import ndjson
import random
import pandas as pd
import uuid
import json

# Read the CSV file
# Read the CSV file
practitionerdata = pd.read_csv('./input/npi_practitioner.csv')

loinc_dict = {
    '4544-3': 'Hemoglobin A1c/Hemoglobin.total in Blood',
    '2708-6': 'Oxygen [Partial pressure] in Arterial blood',
    '2085-9': 'Cholesterol in LDL [Mass/volume] in Serum or Plasma',
    '33914-3': 'Platelets [#/volume] in Blood by Automated count',
    '777-3': 'Platelets [#/volume] in Blood by Manual count',
    '2823-3': 'Potassium [Moles/volume] in Serum or Plasma',
    '2160-0': 'Creatinine [Mass/volume] in Serum or Plasma',
    '718-7': 'Erythrocytes [#/volume] in Blood by Automated count',
    '4548-4': 'Hemoglobin [Mass/volume] in Blood',
    '20565-8': 'Glucose [Mass/volume] in Blood',
    '3016-3': 'Glucose [Mass/volume] in Urine',
    '1920-8': 'Albumin [Mass/volume] in Serum or Plasma',
    '2345-7': 'Glucose [Mass/volume] in Serum or Plasma',
    '17861-6': 'Glucose [Mass/volume] in Blood by Glucometer',
    '6690-2': 'Leukocytes [#/volume] in Blood by Automated count',
    '6768-6': 'Leukocytes [#/volume] in Blood by Manual count',
    '14749-6': 'Lipase [Enzymatic activity/volume] in Serum or Plasma by Photometry',
    '4547-6': 'Hematocrit [Volume Fraction] of Blood',
    '2276-4': 'Ferritin [Mass/volume] in Serum or Plasma',
    '711-2': 'Erythrocytes [#/volume] in Blood by Manual count',
    '1751-7': 'Albumin [Mass/volume] in Urine',
    '1975-2': 'Aspartate aminotransferase [Enzymatic activity/volume] in Serum or Plasma',
    '2000-8': 'Alanine aminotransferase [Enzymatic activity/volume] in Serum or Plasma',
    '2069-3': 'Cholesterol [Mass/volume] in Serum or Plasma',
    '2093-3': 'Cholesterol in HDL [Mass/volume] in Serum or Plasma',
    '2571-8': 'Triglyceride [Mass/volume] in Serum or Plasma',
    '2885-2': 'Protein [Mass/volume] in Serum or Plasma',
    '2951-2': 'Protein [Mass/volume] in Urine',
    '3094-0': 'Urea nitrogen [Mass/volume] in Serum or Plasma',
    '1759-0': 'Bilirubin.total [Mass/volume] in Serum or Plasma',
    '17856-6': 'Coagulation factor X activity in Platelet poor plasma by Coagulation assay',
    '1923-2': 'Iron [Mass/volume] in Serum or Plasma',
    '20438-7': 'Folate [Mass/volume] in Serum or Plasma',
    '20448-6': 'Vitamin B12 [Mass/volume] in Serum or Plasma',
    '2089-1': 'Urea nitrogen [Mass/volume] in Blood',
    '2091-7': 'Calcium [Mass/volume] in Serum or Plasma',
    '2500-7': 'Sodium [Moles/volume] in Serum or Plasma',
    '27353-2': 'Vitamin D2 [Mass/volume] in Serum or Plasma',
    '27354-0': 'Vitamin D3 [Mass/volume] in Serum or Plasma',
    '2888-6': 'Thyrotropin [Units/volume] in Serum or Plasma',
    '30140-4': 'Calcium [Moles/volume] in Urine',
    '35200-5': 'Mean platelet volume [Entitic volume] in Blood by Automated count',
    '35434-0': 'Creatinine [Mass/volume] in 24 hour Urine',
    '35592-6': 'Phosphate [Mass/volume] in Serum or Plasma',
    '35741-8': 'Prostate specific Ag free [Mass/volume] in Serum or Plasma',
    '35754-1': 'C reactive protein [Mass/volume] in Serum or Plasma by High sensitivity method',
    '57905-2': 'Erythrocyte sedimentation rate by Westergren method',
    '5804-0': 'Bicarbonate [Moles/volume] in Serum or Plasma',
    '5905-5': 'Lactate [Moles/volume] in Serum or Plasma',
    '787-2': 'White blood cells [#/volume] in Blood by Manual count',
}

# List of LOINC codes
loinc_codes = list(loinc_dict.keys())


# Read NDJSON file
with open('./input/Encounter.ndjson', encoding='utf-8') as f:
    data = ndjson.load(f)
with open('./output/ServiceRequest.ndjson', 'a') as f:

    # Process each line
    for line in data:
        # Get encounter id
        encounter_id = line['id']
        patient_id = line['subject']['reference'].split('/')[1]
        random_row = practitionerdata.sample(n=1)
        practitioner_id = random_row['NPI']
        # Generate a random index to select a LOINC code
        rand_index = random.randint(0, 49)

        # Create a ServiceRequest
        service_request = {
            "resourceType": "ServiceRequest",
            "id": str(uuid.uuid4()),
            "meta": {
                "profile": [
                    "http://hl7.org/fhir/us/core/StructureDefinition/us-core-servicerequest"
                ]
            },
            "status": "active", # Assume all ServiceRequests are active
            "intent": "order",  # Assume these are all orders
            "code": {
                "coding": [{
                    "system": "http://loinc.org",
                    "code": loinc_codes[rand_index],
                    "display": loinc_dict[loinc_codes[rand_index]]
                }],
            },
            "subject": {
                "reference": "Patient/" + patient_id
            },
            "encounter" :{
                "reference": "Encounter/" + encounter_id
            },
            "authoredOn": "2020-01-01T00:00:0",
            "requester": {"reference": "Practitioner/" + str(practitioner_id)},
            "reasonCode": [{
                "coding": [{
                    "system": "http://hl7.org/fhir/sid/icd-10-cm",
                    "code": "I10",
                    "display": "ICD-10"
                }],
                "text": "Diabetes"
            }]
        }
        f.write(json.dumps(service_request, separators=(',', ':')))
        f.write('\n')
