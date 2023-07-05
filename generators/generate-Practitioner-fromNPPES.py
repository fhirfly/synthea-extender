import pandas as pd
import json
import datetime
# Read the CSV file
data = pd.read_csv('./input/npi_practitioner.csv')

with open('./output/Practitioner.ndjson', 'w') as f:
    for _, row in data.iterrows():
        # Create a new Practitioner
        if row['Provider Last Name (Legal Name)']!= 'NaN' and row['Provider First Name']!= 'NaN':
            practitioner = {
                "resourceType": "Practitioner",
                            "id": row['NPI'],
                "meta": {
                    "profile": [
                        "http://hl7.org/fhir/us/core/StructureDefinition/us-core-practitioner"
                    ]
                },
                "name": [{
                    "family": row['Provider Last Name (Legal Name)'],  # assuming the column name for last name in your CSV
                    "given": [row['Provider First Name']],  # assuming the column name for first name in your CSV
                }],
                "status": "active",
                "address": [{
                    "line": [row['Provider First Line Business Mailing Address']],  # assuming the column name for address in your CSV
                    "city": row['Provider Business Mailing Address City Name'],  # assuming the column name for city in your CSV
                    "state": row['Provider Business Mailing Address State Name'],  # assuming the column name for state in your CSV
                    "postalCode": row['Provider Business Mailing Address Postal Code'],  # assuming the column name for zip in your CSV
                    "country": "US"
                }],
                "telecom": [{
                    "system": "phone",  # assuming the contact is a phone
                    "value": row['Provider Business Mailing Address Telephone Number'],  # assuming the column name for phone in your CSV
                }],
                "identifier": [{
                    "system": "http://hl7.org/fhir/sid/us-npi",
                    "value": row['NPI'],  # assuming the column name for NPI in your CSV
                }]
            }

            # Write the Practitioner to the file
            f.write(json.dumps(practitioner, separators=(',', ':')))
            f.write('\n')
