import spacy

# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")

# Process whole documents
text = ("When Sebastian Thrun started working on self-driving cars at "
        "Google in 2007, few people outside of the company took him "
        "seriously. “I can tell you very senior CEOs of major American "
        "car companies would shake my hand and turn away because I wasn’t "
        "worth talking to,” said Thrun, in an interview with Recode earlier "
        "this week.")

# doc = nlp('im crikcet player')

# # Analyze syntax
# print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
# print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])
# print(*doc.ents)

def getdata(text):
    
    entry = {}
    try:
        doc = nlp(text)
        for entity in doc.ents:
            # print(entity.text, entity.label_)
            entry[entity.label_] = entity.text
        print(entry)
        status = 'SUCCESS'
        return status, entry
    except Exception as e:
        print("got expetion", e)
    
    return 'FAILURE',{}

# status, entry = getdata('im crikcet player')
# res = {'data': entry, 'status': status}
# print(res)
print("reloadiang application")
        

# # Find named entities, phrases and concepts
# for entity in doc.ents:
#     print(entity.text, entity.label_)


