import os
import json
import collections.abc

def extract_qa_from_json(json_data):
    """Extract question-answer pairs from the provided JSON data."""
    qa_pairs = []
    if json_data.get("Document", None) != None and json_data.get("Document").get('QAPairs')!= None:
        for i , qaps in enumerate(json_data.get("Document").get('QAPairs')):
            qap = json_data.get("Document").get('QAPairs').get('QAPair')
            pid = json_data.get("Document").get("@pid", None)
            if pid == None:
                pid = json_data.get("Document").get("@id", None)
            if pid == None:
                pid = json_data.get("Document").get("@fid", None)
                
            if isinstance(qap, collections.abc.Sequence) == True:
                question = qap[i].get('Question', None)
                if question!=None:
                    questiontext = question.get('#text')
                    answertext = qap[i].get('Answer', None)
            else:
                question = qap.get('Question', None)
                questiontext = question.get('#text')
                answertext = qap.get('Answer', None)
            # Append the QA pair to the list
            qa_pairs.append({
                    "linkId": pid,
                    "text": questiontext,
                    "type": "text",
                    "initial": [{"valueString": answertext}]
                })

    if json_data.get("doc", None) != None:
        for i , qaps in enumerate(json_data.get("doc").get('qaPairs')):
            qap = json_data.get("doc").get('qaPairs').get('pair')
            pid = json_data.get("doc").get("@pid", None)
            if pid == None:
                pid = json_data.get("doc").get("@id", None)
            if pid == None:
                pid = json_data.get("doc").get("@fid", None)
            if isinstance(qap, collections.abc.Sequence) == True:
                question = qap[i].get('question', None)
                if question!=None:
                    questiontext = question.get('#text')
                    answertext = qap[i].get('answer', None)
            else:
                question = qap.get('question', None)
                questiontext = question.get('#text')
                answertext = qap.get('answer', None)
            # Append the QA pair to the list
                qa_pairs.append({
                    "linkId": pid,
                    "text": questiontext,
                    "type": "text",
                    "initial": [{"valueString": answertext}]
                })
    if json_data.get("DiseaseFile", None) != None:
        for i , qaps in enumerate(json_data.get("DiseaseFile").get('QAPairs')):
            qap = json_data.get("DiseaseFile").get('QAPairs').get('QAPair')
            pid = json_data.get("DiseaseFile").get("@fid")
            if isinstance(qap, collections.abc.Sequence) == True:
                question = qap[i].get('question', None)
                if question!=None:
                    questiontext = question.get('#text')
                    answertext = qap[i].get('answer', None)
            else:
                question = qap.get('question', None)
                questiontext = question.get('#text')
                answertext = qap.get('answer', None)
            # Append the QA pair to the list
                qa_pairs.append({
                    "linkId": pid,
                    "text": questiontext,
                    "type": "text",
                    "initial": [{"valueString": answertext}]
                })
    return qa_pairs

def process_directory(dir_path, questionaire_output_file, response_output_file):
    """Process a directory and its subdirectories, extracting Q/A pairs from each JSON file."""
    i = 0
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.json'):
                with open(os.path.join(root, file), encoding='utf8', mode='r') as f:
                    data = json.load(f)
                    qa_pairs = extract_qa_from_json(data)
                    i=i+1
                    document = data.get('Document', None)
                    if document == None:
                        document = data.get('doc', None)
                        if document!=None:
                            documentId = document.get('@id', None)
                            if (documentId == None):
                                documentId = data.get('@fid', None)
                    else:
                        documentId = document.get('@id', None)
                        if (documentId == None):
                            documentId = document.get('@fid', None)
                    if document == None:
                        document = data.get('DiseaseFile', None)
                        documentId = document.get('@id', None)
                        if (documentId == None):
                            documentId = document.get('@fid', None)
                    
                    documentUrl = document.get('@url')
                     # Create the new Questionaire JSON file
                    with open('./output/' + questionaire_output_file + '.ndjson' , 'a', encoding='utf8') as f:
                        questionnaire = {
                            "resourceType": "Questionnaire",
                            "id": documentId,
                            "url": documentUrl,
                            "status": "active",
                            "subjectType": ["Patient"],
                            "date": "2023-07-02",
                            "item": qa_pairs
                        }
                        
                        json.dump(questionnaire, f, separators=(',', ':'))
                        f.write('\n')
                    # Create the new QuestionaireResponse JSON file
                    with open('./output/' + response_output_file + '.ndjson', 'a', encoding='utf8') as f:
                        questionnaire_response = {
                            "resourceType": "QuestionnaireResponse",
                            "id": documentId,
                            "status": "completed",
                            "subject": {
                                "reference": "Patient/Example"
                            },
                            "authored": "2023-07-02",
                            "item": qa_pairs
                        }
                        
                        json.dump(questionnaire_response, f, separators=(',', ':'))
                        f.write('\n')
    print('proccessed ' +str(i) + ' questions')
# Change this to the path of the directory you want to process
dir_path = 'C:/Users/richb/Projects/MedQuAD'
# This is the file where we'll store the extracted Q/A pairs
questionaire_output_file = 'Questionaire'
response_output_file = 'QuestionaireResponse'
process_directory(dir_path, questionaire_output_file, response_output_file)