import os
import json
import collections.abc

def extract_qa_from_json(json_data):
    """Extract question-answer pairs from the provided JSON data."""
    qa_pairs = []
    if json_data.get("Document", None) != None and json_data.get("Document").get('QAPairs')!= None:
        for i , qaps in enumerate(json_data.get("Document").get('QAPairs')):
            qap = json_data.get("Document").get('QAPairs').get('QAPair')
            if isinstance(qap, collections.abc.Sequence) == True:
                question = qap[i].get('Question', None)
                if question!=None:
                    questiontext = question.get('#text')
                    answertext = qap[i].get('Answer', None)
            else:
                question = qap.get('Question', None)
                questiontext = question.get('#text')
                answertext = qap.get('Answer', None)
            qa_pairs.append({'question': questiontext, 'answer': answertext})

    if json_data.get("doc", None) != None:
        for i , qaps in enumerate(json_data.get("doc").get('qaPairs')):
            qap = json_data.get("doc").get('qaPairs').get('pair')
            if isinstance(qap, collections.abc.Sequence) == True:
                question = qap[i].get('question', None)
                if question!=None:
                    questiontext = question.get('#text')
                    answertext = qap[i].get('answer', None)
            else:
                question = qap.get('question', None)
                questiontext = question.get('#text')
                answertext = qap.get('answer', None)
            qa_pairs.append({'question': questiontext, 'answer': answertext})
    return qa_pairs

def process_directory(dir_path, output_file, all_pairs):
    """Process a directory and its subdirectories, extracting Q/A pairs from each JSON file."""
    all_pairs = [{"question": None, "answer": None}]
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.json'):
                with open(os.path.join(root, file), encoding='utf8', mode='r') as f:
                    data = json.load(f)
                    qa_pairs = extract_qa_from_json(data)
                    all_pairs.update(qa_pairs)
    with open(output_file, 'a', encoding='utf8') as outfile:
        json.dump(all_pairs, outfile)

# Change this to the path of the directory you want to process
dir_path = 'C:/Users/richb/Projects/MedQuAD'
# This is the file where we'll store the extracted Q/A pairs
output_file = 'extracted_qa_pairs.json'
all_pairs = []
process_directory(dir_path, output_file, all_pairs)