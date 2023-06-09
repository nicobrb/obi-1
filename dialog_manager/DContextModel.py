import shelve
import string
from analysis.Frame import Frame
from analysis.regex import resolve
from utils.enumerators import Sex, Response


class DContextModel:
    def __init__(self):
        self.domain_ontology = []  # as a list of Frames
        self.user_name = None
        self.sex = None
        self.correct_answers = 0
        self._create_frames()

    # for future use
    def _add_frame_to_domain_ontology(self, new_frame: Frame):
        self.domain_ontology.append(new_frame)

    def _create_frames(self):
        self.domain_ontology.append(Frame(domain="info", intent="user", **{"name": None, "sex": None}))
        self.domain_ontology.append(Frame(domain="coruscant", intent="qst1", **{"coruscant": None}))
        self.domain_ontology.append(Frame(domain="children", intent="qst2", **{"children": None}))
        self.domain_ontology.append(
            Frame(domain="pillars", intent="qst3", **{"force": None, "knowledge": None, "self discipline": None}))
        self.domain_ontology.append(Frame(domain="kyber", intent="qst4", **{"kyber": None}))
        self.domain_ontology.append(Frame(domain="order", intent="qst5", **{"order": None}))
        self.domain_ontology.append(Frame(domain="yoda", intent="qst6", **{"yoda": None}))
        self.domain_ontology.append(Frame(domain="color", intent="qst7", **{"color": None}))
        self.domain_ontology.append(Frame(domain="master", intent="qst8", **{"master": None}))
        self.domain_ontology.append(Frame(domain="dagobah", intent="qst9", **{"dagobah": None}))
        self.domain_ontology.append(Frame(domain="anakin", intent="qst10", **{"anakin": None}))
        self.domain_ontology.append(Frame(domain="role", intent="qst11", **{"general": None, "commander": None}))
        self.domain_ontology.append(
            Frame(domain="orders", intent="qst12", **{"guardian": None, "sentinel": None, "consular": None}))

    def find_name(self, user_greetings):
        with shelve.open("databases/names_db/names") as names_db:
            males = names_db["males"]
            females = names_db["females"]
            for word in user_greetings.translate(str.maketrans('', '', string.punctuation)).split():
                if word.lower() in males:
                    self.user_name = word
                    self.sex = Sex.FEMALE
                    break
                elif word.lower() in females:
                    self.user_name = word
                    self.sex = Sex.FEMALE
                    break
        return self.user_name is not None

    def decipher_response(self, user_response: str, domain: str):
        frame = next(frm for frm in self.domain_ontology if frm.slots["domain"] == domain)
        pos, neg = resolve(user_response, frame)
        match (pos, neg, frame.is_complete):
            case (True, False, True):
                resp = Response.CORRECT
            case (False, True, _):
                resp = Response.INCORRECT
            case (True, False, False):
                resp = Response.INCOMPLETE
            case (True, True, _) | (False, False, _):
                resp = Response.UNCERTAIN
            case _:
                resp = Response.UNCERTAIN
        return resp, frame
