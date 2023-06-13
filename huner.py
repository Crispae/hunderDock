from flair.models import MultiTagger
from flair.data import Sentence
from flair.tokenization import SciSpacyTokenizer

import flask
from flask import Flask,request


### NOTE: Flair model causing problem in running server with multiple other models
## Need to seprate and load as standalone docker

class ModelLoader:
    """
    The code defines a Flask app that loads a pre-trained Flair model for named entity recognition and
    exposes an API endpoint for extracting entities from input text using the model.
    :return: The function "LstmModel" returns a JSON object containing the extracted entities and the
    input text.
    """
    def __init__(self):
        print("Loading model..")
        self.model = MultiTagger.load("hunflair") ### model is intialized
        print("Model Loaded")

    def EntityExtractor(self,input):
        
        ## Inferencing step
        sentence = Sentence(input) ### processing the text using Flair library
        self.model.predict(sentence) 
        
        ### Extraction step
        extracted_entities = []
        for keys in sentence.annotation_layers.keys():
            for sent in sentence.get_spans(keys):
                data_dict = {"word":sent.tokens[0].text,"start":sent.tokens[0].start_position,"end":sent.tokens[0].end_position,"entity":sent.tag.lower()}
                
                extracted_entities.append(data_dict)
        return extracted_entities

app = Flask(__name__)
LSTM_CRF_Model = ModelLoader() ## instansiating the LSTM model

@app.route("/extract",methods=["POST","GET"])
def LstmModel():
    print("Processing through LSTM-CRF model")

    if request.method == "POST":

        json_data = request.get_json() ## Fetching the text from post request
        input_text = str(json_data["text"])

        try:
            LSTM_extracted_entites = LSTM_CRF_Model.EntityExtractor(input=input_text)
            return [LSTM_extracted_entites,input_text] ## json output

        except:
            print("Error occur in processing the input text")
            return {"Result":"Error"}
    else:
        print("Get method called")
        return "Get method called,Use Post method to annotate the text"

if __name__ == "__main__":

    app.run(host="0.0.0.0",port=4031)



