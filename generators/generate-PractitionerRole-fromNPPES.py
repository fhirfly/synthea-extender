import pandas as pd
import json
import datetime
# Read the CSV file
data = pd.read_csv('./input/npi_practitioner.csv')

with open('./output/PractitionerRole.ndjson', 'w') as f:
    for _, row in data.iterrows():
        # Create a new Practitioner
        if row['Provider Last Name (Legal Name)']!= 'NaN' and row['Provider First Name']!= 'NaN':
            practitioner_role = {
            "resourceType": "PractitionerRole",
            "id": "pracrole001",
            "active": True,
            "practitioner": {
                "reference": "Practitioner/prac001",
                "display": "Dr. Smith"
            },
            "organization": {
                "reference": "Organization/org001",
                "display": "ABC Hospital"
            },
            "code": [
                {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/practitioner-role",
                            "code": "doctor",
                            "display": "Doctor"
                        }
                    ],
                    "text": "Doctor"
                }
            ],
            "specialty": [
                {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "394814009",
                            "display": "General Practitioner"
                        }
                    ],
                    "text": "General Practitioner"
                }
            ],
            "location": [
                {
                    "reference": "Location/loc001",
                    "display": "Main Hospital Campus"
                }
            ]
        }

        # Write the Practitioner to the file
        f.write(json.dumps(practitioner_role, separators=(',', ':')))
        f.write('\n')
