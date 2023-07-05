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

with open('./output/Goal.ndjson', 'w') as f:
# Process each line
    for line in data:
        # Get encounter id
        patient_id = line['id']
        random_row = practitionerdata.sample(n=1)
        practitioner_id = 1234

        goal = {
            "resourceType": "Goal",
            "id": uuid,
            "lifecycleStatus": "planned",
            "description": {
                "text": "Quit smoking"
            },
            "subject": {
                "reference": "Patient/" + patient_id,
                "display": "John Doe"
            },
            "target": [
                {
                    "measure": {
                        "coding": [
                            {
                                "system": "http://loinc.org",
                                "code": "72166-2",
                                "display": "Nicotine and metabolites panel - Urine"
                            }
                        ],
                        "text": "Nicotine level"
                    },
                    "detailQuantity": {
                        "value": 0.0,
                        "comparator": "<=",
                        "unit": "ng/mL",
                        "system": "http://unitsofmeasure.org",
                        "code": "ng/mL"
                    },
                    "dueDate": "2023-12-31"
                }
            ]
        }

        f.write(json.dumps(goal, separators=(',', ':')))
        f.write('\n')