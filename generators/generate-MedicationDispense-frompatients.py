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

with open('./output/MedicationDispense.ndjson', 'w') as f:
# Process each line
    for line in data:

        # Get encounter id
        patient_id = line['id']
        random_row = practitionerdata.sample(n=1)
        practitioner_id = random_row['NPI']

        medication_dispense = {
            "resourceType": "MedicationDispense",
            "id": uuid.uuid4(),
            "status": "completed",
            "subject": {
                "reference": "Patient/" + patient_id,
                "display": "Jane Doe"
            },
            "performer": [
                {
                    "actor": {
                        "reference": "Practitioner/" + practitioner_id ,
                        "display": "Dr. Johnson"
                    }
                }
            ],
            "authorizingPrescription": [
                {
                    "reference": "MedicationRequest/medreq001",
                    "display": "Aspirin Prescription"
                }
            ],
            "type": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                        "code": "FP",
                        "display": "Finished Product"
                    }
                ],
                "text": "Finished Product"
            },
            "quantity": {
                "value": 30,
                "unit": "tablets",
                "system": "http://unitsofmeasure.org",
                "code": "tbl"
            },
            "daysSupply": {
                "value": 30,
                "unit": "days",
                "system": "http://unitsofmeasure.org",
                "code": "d"
            },
            "medicationReference": {
                "reference": "Medication/med1",
                "display": "Aspirin"
            },
            "whenPrepared": "2023-07-03T14:42:00+00:00",
            "whenHandedOver": "2023-07-03T15:00:00+00:00",
        }



         # Write the Practitioner to the file
        f.write(json.dumps(medication_dispense, separators=(',', ':')))
        f.write('\n')