from api import APIClient
import pandas as pd

class Classifier:
    def __init__(self):

# Optional param: method
# Default: Manyshot, delay seperate
# Options: 'manyshot_seperate_delay', 'manyshot', 'fewshot', 'fewshot_chain_of_thought', 'chain_of_thought'
        self.client = APIClient()
        
    def classify(self, claim):
        response, subclaim_list, valid_subclaims = self.client.run_pipeline(claim)
        return response, subclaim_list, valid_subclaims

class BackUpClassifier:
    def __init__(self):
        
# Optional param: method
# Default: Manyshot, delay seperate
# Options: 'manyshot_seperate_delay', 'manyshot', 'fewshot', 'fewshot_chain_of_thought', 'chain_of_thought'
        self.client = APIClient(temperature=1)
        
    def classify(self, claim):
        response, subclaim_list, valid_subclaims = self.client.run_pipeline(claim)
        return response, subclaim_list, valid_subclaims
        
classifier = Classifier()
classifier2 = BackUpClassifier()


# Classify congress Test set
validation_set = pd.read_csv("data/test.csv")

#clean
validation_set["ty_binary_label"] = validation_set["ty_binary_label"].apply(lambda x: int(x))
validation_set["will_binary_label"] = validation_set["will_binary_label"].apply(lambda x: int(x))
validation_set["clean_text"] = validation_set["clean_text"].apply(lambda x: x.replace("\n"," "))

validation_set_labeled = pd.DataFrame(columns=["text", "clean_text", "will_labels", "ty_labels", "will_binary_label", "ty_binary_label", "llm_label", "subclaim_list", "valid_subclaims"])

for counter, (_, row) in enumerate(validation_set.iterrows()):
    try:
        text = row["text"]
        clean_text = row["clean_text"]
        ty_label = row["ty_labels"]
        will_label = row["will_labels"]
        will_binary_label = row["will_binary_label"]
        ty_binary_label = row["ty_binary_label"]
        llm_label, subclaim_list, valid_subclaims = classifier.classify(clean_text)
    
    except Exception as e:
        try:    
            llm_label, intermediary_response, valid_subclaims = classifier2.classify(text)
        except Exception as e:
            print("ERROR: ", e)
            llm_label = 2
            subclaim_list = []
            valid_subclaims = []    
    
    new_row_df = pd.DataFrame([{
        "text": text, 
        "clean_text": clean_text,
        "ty_label": ty_label, 
        "will_label": will_label, 
        "will_binary_label": will_binary_label,
        "ty_binary_label": ty_binary_label,
        "llm_label": llm_label, 
        "subclaim_list": subclaim_list, 
        "valid_subclaims": valid_subclaims
    }])
    validation_set_labeled = pd.concat([validation_set_labeled, new_row_df], ignore_index=True)
        
    if counter % 5 == 0:
        print("Classified", counter, "/", len(validation_set), "paragraphs")

validation_set_labeled.to_csv("results/test_manyshot_gpt4o.csv", mode='a', index=False)