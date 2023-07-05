import ndjson
import random
import pandas as pd
import uuid
import json
# Read the CSV file
practitionerdata = pd.read_csv('./input/npi_practitioner.csv')

# Read NDJSON file
with open('./input/Patient.ndjson', encoding='utf-8') as f:
    data = ndjson.load(f)

with open('./output/AllergyIntolerance.ndjson', 'w') as f:
# Process each line
    for line in data:
        # Get encounter id
        patient_id = line['id']
        random_row = practitionerdata.sample(n=1)
        practitioner_id = 1234

        # Define the base structure for an AllergyIntolerance resource
        allergy_intolerance = {
            "resourceType": "AllergyIntolerance",
            "id": str(uuid.uuid4()),  # Unique id
            "clinicalStatus": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical",
                        "code": "active"
                    }
                ]
            },
            "verificationStatus": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification",
                        "code": "confirmed"
                    }
                ]
            },
            "type": "allergy",
            "category": ["food"],
            "criticality": "high",
            "code": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "91935009",
                        "display": "Allergy to peanuts (disorder)"
                    }
                ]
            },
            "patient": {
                "reference": "Patient/" + patient_id
            },
            "onsetDateTime": "2000-01-01T00:00:00-04:00",
            "recordedDate": "2023-07-02T00:00:00-04:00",
            "recorder": {
                "reference": "Practitioner/" + str(practitioner_id)
            },
            "asserter": {
                "reference": "Patient/" + patient_id
            },
            "reaction": [
                {
                    "substance": {
                        "coding": [
                            {
                                "system": "http://snomed.info/sct",
                                "code": "91935009",
                                "display": "Allergy to peanuts (disorder)"
                            }
                        ]
                    }
                }
            ]
        }

        f.write(json.dumps(allergy_intolerance, separators=(',', ':')))
        f.write('\n')