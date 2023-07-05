import pandas as pd
import json
import datetime
# Read the CSV file
data = pd.read_csv('./input/npi_organization.csv')

with open('./output/Organization.ndjson', 'w') as f:
    for _, row in data.iterrows():
        # Create a new Practitioner
        organization = {
        'resourceType': 'Organization',
        'id': row['NPI'],
        'identifier': [
            {
                'system': 'http://hl7.org/fhir/sid/us-npi',
                'value': row['NPI'],
            },
        ],
        'name': row['Provider Organization Name (Legal Business Name)'],
        'address': [
            {
                'line': [row['Provider First Line Business Mailing Address']],
                'city': row['Provider Business Mailing Address City Name'],
                'state': row['Provider Business Mailing Address State Name'],
                'postalCode': row['Provider Business Mailing Address Postal Code'],
            },
        ],
        "telecom": [{
                    "system": "phone",  # assuming the contact is a phone
                    "value": row['Provider Business Mailing Address Telephone Number'],  # assuming the column name for phone in your CSV
                }],
        }
        
        # Write the Organization to the file
        f.write(json.dumps(organization, separators=(',', ':')))
        f.write('\n')
