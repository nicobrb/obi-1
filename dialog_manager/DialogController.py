import shelve
import random
from utils.enumerators import Turn, Response
from dialog_manager.DContextModel import DContextModel
from generation.NaturalLanguageGenerator import NaturalLanguageGenerator


class DialogController:
    def __init__(self, n_questions: int = 3):
        assert 3 <= n_questions <= 12, "invalid number of questions!"
        self.turn = Turn.INTRO
        self.last_response = Response.CORRECT
        self.retry = False
        self.done = False
        self.nlg = NaturalLanguageGenerator()
        self.context_model = DContextModel()
        self.n_questions_to_ask = n_questions
        self.questions_dictionary = {}
        with shelve.open("databases/questions_db/questions") as questions_db:
            chosen_questions_keys = random.sample(list(questions_db), self.n_questions_to_ask)  # n questions from db
            self.questions_dictionary = {key: questions_db[key] for key in chosen_questions_keys}

        self.qst_generator = self._generate_questions()
        self.current_qst = None

    def next_turn(self, idx=None):
        self.turn = Turn(self.turn.value + 1) if idx is None else Turn(idx)

    def _generate_questions(self):
        yield from self.questions_dictionary

    def _backup_strategy(self):
        pass

    def elaborate_initiative(self):
        if self.n_questions_to_ask == 0:
            self.next_turn()
        match self.turn:
            case Turn.INTRO:
                return self.nlg.initiative(self.turn)
            case Turn.OUTRO:
                self.done = True
                kwargs = {
                    "tot_qst": len(self.questions_dictionary),
                    "correct_qst": self.context_model.correct_answers,
                    "passed": (self.context_model.correct_answers / len(self.questions_dictionary) >= (1 / 2))
                }
                return self.nlg.initiative(turn=self.turn, **kwargs)
            case Turn.QUESTION:
                if self.last_response == Response.CORRECT:
                    key = next(self.qst_generator)
                    self.current_qst = (key, self.questions_dictionary[key])
                    return self.nlg.initiative(turn=self.turn,
                                               last_response=self.last_response, **{"question": self.current_qst[1]})
                else:
                    return self.nlg.initiative(turn=self.turn, last_response=self.last_response)

    def elaborate_user_input(self, user_input: str):
        match self.turn:
            case Turn.INTRO:
                self.context_model.find_name(user_input)
                response = self.nlg.response(turn=self.turn, **{"name": self.context_model.user_name})
                self.next_turn()
                return response
            case Turn.QUESTION:
                kwargs = {}
                resp, frame = self.context_model.decipher_response(user_input, self.current_qst[0])
                if resp == Response.INCOMPLETE and self.retry:
                    resp = Response.INCORRECT
                self.last_response = resp
                response = self.nlg.response(turn=self.turn, last_response=self.last_response, **kwargs)
                if self.last_response == Response.INCOMPLETE:
                    completed_slots = [key for key, value in frame.slots.items() if value is not None][2:]
                    response = response.replace(
                        self.nlg.SENTINEL,
                        " and ".join([", ".join(completed_slots[:-1]), completed_slots[-1]]) if
                        len(completed_slots) > 1 else completed_slots[0]
                    )
                if self.last_response == Response.CORRECT:
                    self.n_questions_to_ask -= 1
                    self.retry = False
                    self.context_model.correct_answers += 1
                elif not self.retry:
                    self.retry = True
                elif self.retry:
                    self.n_questions_to_ask -= 1
                    self.retry = False
                    self.last_response = Response.CORRECT
                return response
