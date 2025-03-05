import requests
import json
import random
import sys

'''
Read user inputs from file.
Solr Connection details.
'''

def read_solr_inputs(filepath="inputs.txt"):
    inputs = {

    }

    try:
        with open(filepath, "r") as file:
            for line in file:
                key, value = line.strip().split('=')
                inputs[key.strip()] = value.strip()
    except Exception as e:
        print(f"error while reading file: {filepath}")
        exit(1)


    if not is_valid_input(inputs):
        raise Exception("Invalid inputs")

    return inputs


def is_valid_input(inputs):
    return ("hostname" in inputs and "portnumber" in inputs and "corename" in inputs)



# construct solr url with the given inputs
def get_solr_url(inputs):
    return f"http://{inputs['hostname']}:{inputs['portnumber']}/solr/{inputs['corename']}"
    

"""
Fetche core metadata including core name, index size, and document count.
"""
def get_core_metadata(inputs):

    solr_url = f"http://{inputs['hostname']}:{inputs['portnumber']}/solr/admin/cores?action=STATUS&wt=json" 

    try:
        response = requests.get(solr_url)
        response.raise_for_status()
        data = response.json()

        core_info = data["status"].get(inputs["corename"], {})   

        return {
            "core name": inputs["corename"],
            "index name": core_info.get("name"),
            "size of index": core_info.get("index", {}).get("sizeInBytes", 0),
            "# documents": core_info.get("index", {}).get("numDocs", 0),
        }  
    except requests.exceptions.RequestException as e:
        print(f"Eoor while fetching metadeta: {e}")
        exit(1)
    


"""
Retrieves 2 randomly selected documents from Solr, extracting first-level keys only.
"""
def get_random_documents(inputs):

    solr_url = f"{get_solr_url(inputs)}/select"
    params = {
        "q": "*:*",
        "rows": 2,  # Fetch 2 random documents
        "fl": "*",
        "wt": "json",
        "sort": f"random_{random.randint(1000, 9999)} asc"
    }

    try:
        response = requests.get(solr_url, params=params)
        response.raise_for_status()
        docs = response.json().get("response", {}).get("docs", [])

        sample_docs = []

        '''
        alter the response such that it matched the 
        expected solr_metadata.json
        
        '''
        for doc in docs:
            sample_doc = {
                "document_id": doc.get("id", "N/A"),
                "fieldTypes": []
            }

            for key, value in doc.items():
                if key == "id" or key == "_root_" or key == "_version_":   
                    continue  # Skip ID field, root and version. 
                
                field_entry = {"fieldName": key, "value": value}
                sample_doc["fieldTypes"].append(field_entry)

            sample_docs.append(sample_doc)

        return sample_docs
    except requests.exceptions.RequestException as e:
        print(f"Error fetching random documents: {e}")
        exit(1)

def main():

    if len(sys.argv) != 2:
        sys.exit("Usage: python solr_connector.py <inputfilename>.txt")


    filename = sys.argv[1] # get solr input file name

    inputs = read_solr_inputs(filepath=filename)

    metadata = get_core_metadata(inputs)

    print(metadata)
    random_documents = get_random_documents(inputs)


    # result = {
    #     "metadata": metadata,
    #     "documents" : random_documents
    # }

    result = {
        "type": "apache_solr",
        "data": {
            "CoreName": metadata["core name"],
            "SizeofIndex": metadata["size of index"],
            "NumberofDocuments": metadata["# documents"],
            "Index": [
                {
                    "IndexName": metadata["core name"],  # Assuming IndexName is the CoreName
                    "Documents": random_documents
                }
            ]
        }
    }

    with open("solr_metadata.json", "w") as file:
        json.dump(result, file, indent=4)
    
    print("solr metadata saved")


if __name__ == "__main__":
    main()