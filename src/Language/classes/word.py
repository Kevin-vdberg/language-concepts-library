import json
from ..Types.enums import WordType

class Word:
    """
    A class that contains all information regarding a word concept variation in a certain language. Words are classified as nouns, verbs or modifiers

    Attributes:
        simple (str): The grammatical simple version of the word: this is almost always the lemma.
        meaning (str): A description of the word's meaning.
        ipa (str): The phonetic transcription of the simple/lemma.
        sound (str): A reference to a sound file.
        variations (dictionary): A dictionary containing all variations of a word and it's classifying attributes
    """

 # Attributes for word varriations
    _COMMON_ATTRIBUTES =    {   "ipa":"",
                                "sound": ""
                            }   
    _GENERAL_ATTRIBUTES =   {  "gender": ("male","female","neuter"),
                                "number": ("singular","plural"),
                                "case": ("nominative","genitive","dative","accusative","vocative","ablative","organic","local","instrumental","prepositional")
                            }
    
    _NOUN_ATTRIBUTES =       {  "gender": _GENERAL_ATTRIBUTES["gender"],
                                "number": _GENERAL_ATTRIBUTES["number"],
                                "case": _GENERAL_ATTRIBUTES["case"],
                                "unique": ("proper","common"),
                                "diminuative":(True,False)                         
                            }
    
    _VERB_ATTRIBUTES =       {  "mood":("indicative","imperative","conditional","interrogative","subjunctive"),
                                "tense":("present","past","future","absolute"),
                                "aspect":("simple","perfective","imperfective"),
                                "person":(1,2,3),
                                "gender":_GENERAL_ATTRIBUTES["gender"],
                                "number":_GENERAL_ATTRIBUTES["number"],
                                "direct_object":(),
                                "indirect_object":()
                            }
    
    _MODIFIER_ATTRIBUTES =   {  "type":(),
                                "gender": _GENERAL_ATTRIBUTES["gender"],
                                "number": _GENERAL_ATTRIBUTES["number"],
                                "case": _GENERAL_ATTRIBUTES["case"],
                            }
    
    @staticmethod
    def _validate_type(type):
        try:
            type_enum = WordType[type]
            return type_enum
        except KeyError:
            return None
    

    def __init__(self,type):
        """
        Initializes the word object

        Parameters:
            type (Enum): This defines the kind of object that's made and uses an LanguageWordConceptType Enum.
        """ 
        self.simple = ""
        self.meaning = ""
        self.type = type.name
        self.ipa = ""
        self.sound = ""

        if type == WordType.NOUN:
            base_variation = Word._NOUN_ATTRIBUTES
        elif type == WordType.VERB:
            self.valency= -1
            base_variation = Word._VERB_ATTRIBUTES
        elif type == WordType.MODIFIER:
            base_variation = Word._MODIFIER_ATTRIBUTES
        else:
            raise NotImplementedError("This type dictionary has not been implemented")
        
        variation_dictionary = dict(base_variation)

        for key, value in Word._COMMON_ATTRIBUTES.items():
            variation_dictionary[key] = value

        self.variations = {"_doc": variation_dictionary}
            

    def set_variation_attribute(self,variation,key,value):
        self.variations[variation][key] = value
    
    def get_all_variations(self):
        filtered_variations = [key for key in self.variations.keys() if not key.startswith("_")]
        return filtered_variations


    def get_as_json(self):
        """
        Create a JSON object for the LanguageWordConcept object

        Parameters:
            None
        
        Returns:
            str:  JSON object describing the object
        """

        word_dictionary =   {
                            "simple": self.simple,
                            "meaning":self.meaning,
                            "ipa":self.ipa,
                            "sound":self.sound,
                            "type": self.type,
                            "variations":self.variations
                            }
                
        if hasattr(self, "valency"):
            word_dictionary["valency"] = self.valency      
        
        json_data = json.dumps(word_dictionary)
        return json_data
    
    def add_variation(self, variation):

        type_enum = WordType[self.type]

        if type_enum == WordType.NOUN:
            base_keys = set(Word._NOUN_ATTRIBUTES.keys())
        elif type_enum == WordType.VERB:
            base_keys = set(Word._VERB_ATTRIBUTES.keys())
        elif type_enum == WordType.MODIFIER:
            base_keys = set(Word._MODIFIER_ATTRIBUTES.keys())
        else:
            raise NotImplementedError("This type dictionary has not been implemented")
        
        common_keys = set(Word._COMMON_ATTRIBUTES.keys())
        variation_keys = base_keys.union(common_keys)

        self.variations[variation] = {key: None for key in variation_keys}
        

    def change_type(self,type):
        Word._validate_type(type)
