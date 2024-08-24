import os
import json

def process_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    tokens = data['tokens']
    tokens_id = data['tokens-IDs']
    ner_tags = data['ner_tags']
    sentence_id = data['sentence-IDs']

    n = len(tokens)
    map = {}

    for i in range(n):
        map[(tokens_id[i], sentence_id[i])] = (ner_tags[i], tokens[i])

    complete_sentence = {}
    complete_sentence[sentence_id[0]] = map[(tokens_id[0], sentence_id[0])][1]
    for i in range(1, n):
        if sentence_id[i] == sentence_id[i - 1]:
            complete_sentence[sentence_id[i]] += " " + map[(tokens_id[i], sentence_id[i])][1]
        else:
            complete_sentence[sentence_id[i]] = map[(tokens_id[i], sentence_id[i])][1]

    types = {}
    bedict = {}

    s = ""
    idx = tokens_id[0]
    for i in range(n):
        tmp = ner_tags[i].split("-")
        if tmp[0] == "B":
            idx = tokens_id[i]
            s = tokens[i] + " "
            if i + 1 >= n or ner_tags[i + 1].split("-")[0] != "I":
                types[s.strip()] = tmp[1]
                bedict[(idx, sentence_id[i])] = s.strip()
        elif tmp[0] == "I":
            s += tokens[i] + " "
            if i + 1 >= n or ner_tags[i + 1].split("-")[0] != "I":
                types[s.strip()] = tmp[1]
                bedict[(idx, sentence_id[i])] = s.strip()

    source_sid = data["relations"]["source-head-sentence-ID"]
    source_wid = data["relations"]["source-head-word-ID"]
    relation_type = data["relations"]["relation-type"]
    target_sid = data["relations"]["target-head-sentence-ID"]
    target_wid = data["relations"]["target-head-word-ID"]

    answer = []
    for i in range(len(source_sid)):
        source_key = (source_wid[i], source_sid[i])
        target_key = (target_wid[i], target_sid[i])
        
        # Debug: Print keys and check if they exist in bedict
        print(f"Source Key: {source_key}, Target Key: {target_key}")
        print(f"bedict: {bedict}")

        source_entity = bedict.get(source_key, "Unknown Source")
        target_entity = bedict.get(target_key, "Unknown Target")

        if source_entity == "Unknown Source" or target_entity == "Unknown Target":
            print(f"Warning: Missing entity for source or target at index {i}")

        answer.append([source_entity, relation_type[i], target_entity])

    return {"types":types,"answer":answer,"dictionary":bedict.__str__()}

def process_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            file_path = os.path.join(input_folder, filename)
            result = process_file(file_path)
            
            output_file_path = os.path.join(output_folder, f"result_{filename}")
            with open(output_file_path, 'w') as out_file:
                json.dump(result, out_file, indent=4)

input_folder = '/home/ubuntu/fifthproj/dataset/resources/json_files'
output_folder = '/home/ubuntu/fifthproj/dataset/resources/extracted_files'
process_folder(input_folder, output_folder)