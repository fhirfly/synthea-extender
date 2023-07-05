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

with open('./output/Consent.ndjson', 'w') as f:
# Process each line
    for line in data:

        # Get encounter id
        patient_id = line['id']
        random_row = practitionerdata.sample(n=1)
        practitioner_id = random_row['NPI']

        # Define the base structure for a Consent resource
        consent = {
            "resourceType": "Consent",
            "id": str(uuid.uuid4()),  # Unique id
            "status": "active",
            "patient": {
                "reference": "Patient/" + patient_id  # ID of the patient
            },
            "dateTime": "2023-07-02 00:00:00",
            "performer": [
                {
                    "reference": "Practitioner/" + str(practitioner_id)  # ID of the practitioner
                }
            ],
            "organization": [
                {
                    "reference": "Organization/1234"  # ID of the organization
                }
            ],
            "policyRule": "http://hl7.org/fhir/ConsentPolicy/opt-in",
            "scope": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/consentscope",
                        "code": "patient-privacy"
                    }
                ]
            },
            "provision": {
                "type": "permit",
                "period": {
                    "start": "2023-07-02",
                    "end": "2024-07-02"
                }
            }
        }

         # Write the Consent to the file
        f.write(json.dumps(consent, separators=(',', ':')))
        f.write('\n')