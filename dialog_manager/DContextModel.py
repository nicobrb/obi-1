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
        self._create_frames()

    # for future use
    def _add_frame_to_domain_ontology(self, new_frame: Frame):
        self.domain_ontology.append(new_frame)

    def _create_frames(self):
        self.domain_ontology.append(Frame(domain="info", intent="user", **{"name": None, "sex": None}))
        self.domain_ontology.append(Frame(domain="coruscant", intent="qst1"))
        self.domain_ontology.append(Frame(domain="children", intent="qst2"))
        self.domain_ontology.append(Frame(domain="pillars", intent="qst3"))
        self.domain_ontology.append(Frame(domain="kyber", intent="qst4"))
        self.domain_ontology.append(Frame(domain="order", intent="qst5"))
        self.domain_ontology.append(Frame(domain="yoda", intent="qst6"))
        self.domain_ontology.append(Frame(domain="color", intent="qst7"))
        self.domain_ontology.append(Frame(domain="dagobah", intent="qst8"))
        self.domain_ontology.append(Frame(domain="master", intent="qst9"))
        self.domain_ontology.append(Frame(domain="anakin", intent="qst10"))

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
        frame_list = [frame for frame in self.domain_ontology if frame.slot["domain"] == domain]
        pos, neg = resolve(user_response, frame_list)
        incomplete_frames = False
        if pos and not neg:
            incomplete_frames = len([frame.slot["domain"] for frame in self.domain_ontology if not frame.complete]) > 0

        match (pos, neg, incomplete_frames):
            case (True, False, False):
                return Response.CORRECT
            case (False, True, _):
                return Response.INCORRECT
            case (True, True, _) | (True, False, True):
                return Response.UNCERTAIN
            case (False, False, _), _:
                return Response.BACKUP
