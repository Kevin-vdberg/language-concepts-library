import spacy

class TextAnalyser:
    """
    Initialize a TextAnalyzer with a specified language

    Args:
        language (str): The language code for the model to use (e.g. "EN").
    """

    #Constants

    #Supported languages. 
    #Models can be added here to create a class instance with different models
    #Make sure the spaCy models are installed when using them
    SPACY_NLP_DICTIONARY = {
        "EN":"en_core_web_md",
    }
   
    #The word type constant is used to lookup spaCy word classes and can be customized here
    WORD_TYPES = {
        "noun":("NOUN"),
        "verb":("VERB"),
        "helper":("ADP")
    }
    
    #Constructor 
    def __init__(self, language, NLP_MODELS=SPACY_NLP_DICTIONARY):
        try:
            language_model = self.SPACY_NLP_DICTIONARY[language]
        except:
            supported_languages = self.SPACY_NLP_DICTIONARY.keys()
            raise ValueError(f"Language '{language}' is not supported. The currently supported languages are: {', '.join(supported_languages)}")
        
        try:
            self.nlp = spacy.load(language_model)
        except Exception as e:
            raise Exception((f"An error occurred when initializing the spaCy language model: {str(e)}"))
        
        self.doc = self.nlp("")   

    #Private methods    
    def _get_doc_from_file(self,file_location):
        try:
            with open(file_location, "r") as file:
                content = file.read()
                doc = self.nlp(content)
            return doc
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_location}")
        except Exception as e:
            raise Exception(f"An error occurred while processing the file: {str(e)}")
    
    def _set_doc(self,doc):
        self.doc = doc
    
    def _evaluate_word_types(self,type,types):
        type_present = False

        for t in types:    
            if type == t:
                type_present = True
                break
        return type_present

    def _get_words(self,type):
        words = []

        try:
            NEEDED_TYPES = self.WORD_TYPES[type]
        except:
            supported_types = ', '.join(self.WORD_TYPES.keys())
            raise ValueError(f"The type {type} is not supported or not defined. You can define the lookup type by updating WORD_TYPES. Currently defined types are: {supported_types}")

        for token in self.doc:
            pos = token.pos_
            if self._evaluate_word_types(pos,NEEDED_TYPES):
                words.append(token.lemma_)
        
        UNIQUE_WORDS = list(set(words))
        return UNIQUE_WORDS
                
    #Public methods
    def set_doc_from_file(self,file_location):
        doc = self._get_doc_from_file(file_location)
        self._set_doc(doc)
    
    def get_nouns(self):
        return  self._get_words("noun")
    
    def get_verbs(self):
        return  self._get_words("verb")
    
    def get_helpers(self):
        return  self._get_words("helper")

    def get_word_concepts(self,type):
        word_concepts = []

        try:
            NEEDED_TYPES = self.WORD_TYPES[type]
        except:
            supported_types = ', '.join(self.WORD_TYPES.keys())
            raise ValueError(f"The type {type} is not supported or not defined. You can define the lookup type by updating WORD_TYPES. Currently defined types are: {supported_types}")

        for token in self.doc:
            concept_dictionary={}
            pos = token.pos_

            if self._evaluate_word_types(pos,NEEDED_TYPES):
                vector = token.vector
                lemma = token.lemma_

                concept_dictionary["Vector"]=vector
                concept_dictionary["Type"]=type
                concept_dictionary["EnLemma"]=lemma
                
                word_concepts.append(concept_dictionary)

        return word_concepts