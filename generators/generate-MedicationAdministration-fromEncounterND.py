import ndjson
import random
import pandas as pd
import uuid
import json

# Read the CSV file
# Read the CSV file
practitionerdata = pd.read_csv('./input/npi_practitioner.csv')

# Read NDJSON file
with open('./input/Encounter.ndjson', encoding='utf-8') as f:
    data = ndjson.load(f)

with open('./output/MedicationDispense.ndjson', 'w') as f:
# Process each line
    for line in data:

        encounter_id = line['id']
        patient_id = line['subject']['reference'].split('/')[1]
        random_row = practitionerdata.sample(n=1)
        practitioner_id = random_row['NPI']

       # Construct the MedicationAdministration Resource
        medication_administration_resource = {
            "resourceType": "MedicationAdministration",
            "id": uuid.uuid4(),
            "status": "completed",
            "medicationReference": {
                "reference": "Medication/f001",
                "display": "aspirin"
            },
            "context": {"reference": "Encounter/" + encounter_id},
            "subject": {
                "reference": "Patient/" + patient_id,
                "display": "John Doe"
            },
            "effectiveDateTime": "2023-07-03T14:42:00+00:00",
            "performer": [
                {
                    "actor": {
                        "reference": "Practitioner/" + practitioner_id,
                        "display": "Dr. Jones"
                    }
                }
            ],
            "dosage": {
                "text": "2 tablets",
                "route": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/route-of-administration",
                            "code": "PO",
                            "display": "Oral use"
                        }
                    ]
                }
            }
        }


         # Write the Practitioner to the file
        f.write(json.dumps(medication_administration_resource, separators=(',', ':')))
        f.write('\n')