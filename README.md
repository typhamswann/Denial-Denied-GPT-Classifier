# Denial Delay Classifier

This project is a classifier for detecting climate denial and delay.

## Installation guide

Clone the repository
```console
git clone https://github.com/willkattrup/denial-delay-classifier.git
```

Setup the virtual environment to install dependencies
```console
python -m venv venv
```

Activate environment
```console
source venv/bin/activate 
```

Install the project
```console
pip install .
```

Set up your API Key
```console
export OPENAI_API_KEY="your api key here"
```

Run the classifier script
## Usage guide

Run classifier.py to classify a list of claims (csv). This will output a results file (csv). To check how the classifier performs against coders, run intercoder_reliability.py. Follow formats in all the folders to get similar outputs.

To change the classification method, change the initialization of the Classifier in classifier.py. There is an optional method parameter. The methods are listed. By default, manyshot classification with denial aggregated is the classifier used. This is the best classification method for our datasets, attaining human-level intercoder reliability if treated as a coder. Optionally, one can also change the language model (currently supporting OpenAI models) and the temperature (level of output randomness).


The methods are as follows:

'manyshot_seperate_delay' (default) - Manyshot classification with seperated delay - This method involves showing the LLM a statement, and having it pass an initial filter of all claims that may be relevant. A loop is then run so that for each of those claims, the LLM is shown the statement and many examples of statements made and the correct label. The samples given are a few hand selected samples and selected from failures of the LLM in the training set. Denial claims are assessed at the second level of the taxonomy than mapped to Denial or no claim. Delay claims are only shown once with many examples of statements and whether they classify as delay or not. This method is done to reduce delay false positives, which the LLMs is inclined to do if shown specific aspects of the second level of the delay taxonomy. If there are formatting failures in the LLM output, the process is re-ran with a different temperature, and model in the case of a formatting failure in the initial screen. 

'manyshot' - Manyshot classification - This method involves showing the LLM a statement, and having it pass an initial filter of all claims that may be relevant. A loop is then run so that for each of those claims, the LLM is shown the statement and many examples of statements made and the correct label. The samples given are a few hand selected samples and selected from failures of the LLM in the training set. Denial and delay claims are assessed at the second level of the taxonomy than mapped to Denial, Delay, or no claim. If there are formatting failures in the LLM output, the process is re-ran with a different temperature, and model in the case of a formatting failure in the initial screen. 

'fewshot' - Fewshot classification - This method involves showing the LLM a statement, and having it pass an initial filter of all claims that may be relevant. A loop is then run so that for each of those claims, the LLM is shown the statement and many examples of statements made and the correct label. The samples given are hand selected instances of the subclaim and common errors. Denial claims are assessed at the second level of the taxonomy than flattened to Denial, Delay, or no claim. Delay claims are only shown once with many examples of statements and whether they classify as delay or not. If there are formatting failures in the LLM output, the process is re-ran with a different temperature, and model in the case of a formatting failure in the initial screen. 

'fewshot_chain_of_thought' - Fewshot chain of thought - This method involves showing the LLM a statement, and having it pass an initial filter of all claims that may be relevant. A loop is then run so that for each of those claims, the LLM is shown the statement and many examples of statements made and the correct label. The samples given are hand selected instances of the subclaim and common errors. The model is then prompted to think step by step and output a final true or false. Claims are assessed at the second level of the taxonomy than flattened to Denial, Delay, or no claim. If there are formatting failures in the LLM output, the process is re-ran with a different temperature, and model in the case of a formatting failure in the initial screen. 

'chain_of_thought' - Chain of thought - This method involves showing the LLM a statement, the taxonomy to the second level, and prompting it to think step by step. After thinking, it will produce an output which will be extracted and mapped to delay, denial, or no claim. If there are formatting failures in the LLM output, the process is re-ran with a different temperature, and model in the case of a formatting failure in the initial screen. 