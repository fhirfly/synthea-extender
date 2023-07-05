import ndjson
import json
import random
from faker import Faker

# Create a Faker instance
fake = Faker()

# Load the NDJSON file
with open('./input/Patient.ndjson', encoding='utf-8') as f:
    data = ndjson.load(f)

with open('./output/Group.ndjson', 'w') as f:
    # Extract patient ids
    patient_ids = [patient['id'] for patient in data]

    # Define the number of groups to create
    num_groups = 50000

    # Initialize an empty list for the groups

    # Generate the groups
    for i in range(num_groups):
        # Randomly select a subset of patient ids for this group
        group_patient_ids = random.sample(patient_ids, k=min(len(patient_ids), random.randint(1, 10)))
    
        # Build the group resource
        group = {
            "resourceType": "Group",
            "id": f"group{i+1}",
            "type": "person",
            "actual": True,
            "name": fake.word(),
            "member": [
                {
                    "entity": {
                        "reference": f"Patient/{patient_id}"
                    }
                }
                for patient_id in group_patient_ids
            ]
        }

        # Write the Group to the file
        f.write(json.dumps(group, separators=(',', ':')))
        f.write('\n')
