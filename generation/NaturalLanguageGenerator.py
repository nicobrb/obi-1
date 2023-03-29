from simplenlg.framework import *
from simplenlg.lexicon import *
from simplenlg.realiser.english import *
from simplenlg.phrasespec import *
from simplenlg.features import *
import random

class NaturalLanguageGenerator: 
    
    def __init__(self):
        lexicon = Lexicon.getDefaultLexicon()
        self.nlg_factory = NLGFactory(lexicon)
        self.realiser = Realiser(lexicon)
        self.affirmative_answers = dict()
        self.negative_answers = dict()
        self.generate_affirmative_answers()
        self.generate_negative_answers()

    def greetings(self) -> str:
        # Create a sentence with the form "Hello, I'm Obi1 and I will question you about Jedi culture. We can start the interview now. What is your name?"
        s_0 = self.nlg_factory.createClause("Hello")
        
        # Create a sentence with the form "I am Obi1"
        subj_1 = self.nlg_factory.createNounPhrase("I")
        verb_1 = self.nlg_factory.createVerbPhrase("be")
        obj_1 = self.nlg_factory.createNounPhrase("Obi1")
        s_1 = self.nlg_factory.createClause(subj_1, verb_1, obj_1)

        # Create a sentence with the form "I will question you"
        subj_2 = self.nlg_factory.createNounPhrase("I")
        verb_2 = self.nlg_factory.createVerbPhrase("question")
        verb_2.setFeature(Feature.TENSE, Tense.FUTURE)
        obj_2 = self.nlg_factory.createNounPhrase("you")
        s_2 = self.nlg_factory.createClause(subj_2, verb_2, obj_2)

        # Create a preposition phrase with the form "about Jedi culture"
        p_1 = self.nlg_factory.createPrepositionPhrase("about")
        p_1.addComplement("Jedi culture")

        # I add the preposition phrase to the sentence
        s_2.addComplement(p_1)

        # I tie the sentence 0 and sentence 1 together with a comma
        c_1 = self.nlg_factory.createCoordinatedPhrase()
        c_1.setConjunction(",")
        c_1.addCoordinate(s_0)
        c_1.addCoordinate(s_1)

        # I tie the sentence generated in the previous step and sentence 2 together with the word "and"
        c_2 = self.nlg_factory.createCoordinatedPhrase()
        c_2.setConjunction("and")
        c_2.addCoordinate(c_1)
        c_2.addCoordinate(s_2)

        # Create a sentence with the form "We can start the interview now"
        subj_3 = self.nlg_factory.createNounPhrase("we")
        verb_3 = self.nlg_factory.createVerbPhrase("start")
        adv_3 = self.nlg_factory.createAdverbPhrase("now")
        verb_3.setPostModifier(adv_3)
        obj_3 = self.nlg_factory.createNounPhrase("the", "interview")
        s_3 = self.nlg_factory.createClause(subj_3, verb_3, obj_3)
        s_3.setFeature(Feature.MODAL, "can")
        
        # Create a sentence with the form "What is your name?"
        subj_4 = self.nlg_factory.createNounPhrase("name")
        verb_4 = self.nlg_factory.createVerbPhrase("be")
        pron_4 = self.nlg_factory.createWord("you", LexicalCategory.PRONOUN)
        pron_4.setFeature(Feature.POSSESSIVE, True)
        subj_4.setDeterminer(pron_4)
        s_4 = self.nlg_factory.createClause(subj_4, verb_4)
        s_4.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHAT_OBJECT)

        # I tie the three sentences together with a new line
        return self.realiser.realiseSentence(c_2) + '\n' + self.realiser.realiseSentence(s_3) + '\n' + self.realiser.realiseSentence(s_4)

    def greets_user(self, name: str = None) -> str:
        # Create a sentence with the form "Hello, name!" if the name is not None, otherwise "Hello, aspiring Padawan!"
        s_0 = self.nlg_factory.createClause("Hello")
        if name:
            subj_1 = self.nlg_factory.createNounPhrase(name + "!")
            s_1 = self.nlg_factory.createClause(subj_1)
            c_1 = self.nlg_factory.createCoordinatedPhrase()
            c_1.setConjunction(",")
            c_1.addCoordinate(s_0)
            c_1.addCoordinate(s_1)
            return self.realiser.realiseSentence(c_1)
        subj_1 = self.nlg_factory.createNounPhrase("Padawan!")
        subj_1.setDeterminer("aspiring")
        s_1 = self.nlg_factory.createClause(subj_1)
        c_1 = self.nlg_factory.createCoordinatedPhrase()
        c_1.setConjunction(",")
        c_1.addCoordinate(s_0)
        c_1.addCoordinate(s_1)

        # Create a sentence with the form "Let's start"
        verb_1 = self.nlg_factory.createVerbPhrase("let's start")
        verb_1.setFeature(Feature.PERSON, Person.FIRST)
        s_2 = self.nlg_factory.createClause(verb=verb_1)

        # Create a preposition phrase with the form "with the first question"
        prep_1 = self.nlg_factory.createPrepositionPhrase("with")
        subj_1 = self.nlg_factory.createNounPhrase("the", "question")
        subj_1.addModifier("first")
        prep_1.addComplement(subj_1)
        s_2.addPostModifier(prep_1)
        return self.realiser.realiseSentence(c_1)[:-1] + '\n' + self.realiser.realiseSentence(s_2)

    def ask_nth_question(self, question) -> str:
        # Create a sentence with for the question extracted from a PD
        s_1 = self.nlg_factory.createSentence(question)
        return self.realiser.realiseSentence(s_1)
    
    def generate_affirmative_answers(self):
        # 1. Create a sentence with the form "Yes, that's correct."
        s_0 = self.nlg_factory.createClause("Yes")
        verb_1 = self.nlg_factory.createVerbPhrase("that's")
        verb_1.setFeature(Feature.PERSON, Person.FIRST)
        obj_1 = self.nlg_factory.createNounPhrase("correct")
        s_1 = self.nlg_factory.createClause(verb_1, obj_1)

        # I tie the two sentences together with a comma
        c_1 = self.nlg_factory.createCoordinatedPhrase()
        c_1.setConjunction(",")
        c_1.addCoordinate(s_0)
        c_1.addCoordinate(s_1)
        rs_c1 = self.realiser.realiseSentence(c_1)
        self.affirmative_answers.update({rs_c1 : 1})

        # 2. Create a sentence with the form "That's exactly right!"
        verb_2 = self.nlg_factory.createVerbPhrase("that's")
        verb_2.setFeature(Feature.PERSON, Person.FIRST)
        obj_2 = self.nlg_factory.createNounPhrase("right")
        adv_2 = self.nlg_factory.createWord("exactly", LexicalCategory.ADVERB)
        obj_2.addPreModifier(adv_2)
        s_2 = self.nlg_factory.createClause(verb_2, obj_2)
        rs_s2 = self.realiser.realiseSentence(s_2)
        self.affirmative_answers.update({rs_s2 : 0})

        # 3. Create a sentence with the form "You are absolutely correct! You have a great understanding of the topic at hand."
        # Create a sentence with the form "You are absolutely correct!"
        subj_3 = self.nlg_factory.createNounPhrase("you")
        verb_3 = self.nlg_factory.createVerbPhrase("be")
        obj_3 = self.nlg_factory.createNounPhrase("correct!")
        adv_1 = self.nlg_factory.createWord("absolutely", LexicalCategory.ADVERB)
        obj_3.addPreModifier(adv_1)
        s_3 = self.nlg_factory.createClause(subj_3, verb_3, obj_3)

        # Create a sentence with the form "You have a great understanding"
        subj_4 = self.nlg_factory.createNounPhrase("you")
        verb_4 = self.nlg_factory.createVerbPhrase("have")
        obj_4 = self.nlg_factory.createNounPhrase("understanding")
        adj_4 = self.nlg_factory.createWord("a great", LexicalCategory.ADJECTIVE)
        obj_4.addModifier(adj_4)
        s_4 = self.nlg_factory.createClause(subj_4, verb_4, obj_4)

        # Create a preposition phrase with the form "of the topic at hand"
        prep_5 = self.nlg_factory.createPrepositionPhrase("of")
        subj_5 = self.nlg_factory.createNounPhrase("the", "topic")
        subj_5.addModifier("at hand")

        # I tie the preposition phrase to the previous sentence
        prep_5.addComplement(subj_5)
        s_4.addPostModifier(prep_5)

        # I tie the two sentences together with a space
        self.affirmative_answers.update({self.realiser.realiseSentence(s_3)[:-1] + " " + self.realiser.realiseSentence(s_4) : 0})

        # 4. Create a sentence with the form "You are spot on! Your answer perfectly aligns with the correct solution."
        # Create a sentence with the form "You are spot on!"
        subj_6 = self.nlg_factory.createNounPhrase("you")
        verb_6 = self.nlg_factory.createVerbPhrase("be")
        obj_6 = self.nlg_factory.createNounPhrase("spot")
        obj_6.addPostModifier("on!")
        s_6 = self.nlg_factory.createClause(subj_6, verb_6, obj_6)

        # Create a sentence with the form "Your answer perfectly aligns with the correct solution."
        # Create a sentence with the form "Your answer perfectly aligns"
        subj_7 = self.nlg_factory.createNounPhrase("answer")
        pron_7 = self.nlg_factory.createWord("you", LexicalCategory.PRONOUN)
        pron_7.setFeature(Feature.POSSESSIVE, True)
        subj_7.setSpecifier(pron_7)
        verb_7 = self.nlg_factory.createVerbPhrase("align")
        adv_7 = self.nlg_factory.createWord("perfectly", LexicalCategory.ADVERB)
        verb_7.addModifier(adv_7)
        s_7 = self.nlg_factory.createClause(subj_7, verb_7)
        
        # Create a preposition phrase with the form "with the correct solution"
        prep_2 = self.nlg_factory.createPrepositionPhrase("with")
        subj_8 = self.nlg_factory.createNounPhrase("the", "solution")
        subj_8.addModifier("correct")
        prep_2.addComplement(subj_8)
        s_7.addPostModifier(prep_2)

        # I tie the two sentences together with a space
        self.affirmative_answers.update({self.realiser.realiseSentence(s_6)[:-1] + " " + self.realiser.realiseSentence(s_7) : 0})

        # 5. Create a sentence with the form "Bingo! You got it right. Your response is completely accurate."
        # Create a sentence with the form "Bingo!"
        s_8 = self.nlg_factory.createClause("Bingo!")

        # Create a sentence with the form "You got it right."
        subj_9 = self.nlg_factory.createNounPhrase("you")
        verb_9 = self.nlg_factory.createVerbPhrase("get")
        verb_9.setFeature(Feature.TENSE, Tense.PAST)
        obj_9 = self.nlg_factory.createNounPhrase("right")
        pron_9 = self.nlg_factory.createWord("it", LexicalCategory.PRONOUN)
        obj_9.addPreModifier(pron_9)
        s_9 = self.nlg_factory.createClause(subj_9, verb_9, obj_9)

        # Create a sentence with the form "Your response is completely accurate."
        subj_10 = self.nlg_factory.createNounPhrase("response")
        pron_10 = self.nlg_factory.createWord("you", LexicalCategory.PRONOUN)
        pron_10.setFeature(Feature.POSSESSIVE, True)
        subj_10.setSpecifier(pron_10)
        verb_10 = self.nlg_factory.createVerbPhrase("be")
        obj_10 = self.nlg_factory.createNounPhrase("accurate")
        adv_10 = self.nlg_factory.createWord("completely", LexicalCategory.ADVERB)
        obj_10.addPreModifier(adv_10)
        s_10 = self.nlg_factory.createClause(subj_10, verb_10, obj_10)
        self.affirmative_answers.update({self.realiser.realiseSentence(s_8)[:-1] + " " + self.realiser.realiseSentence(s_9) + " " + self.realiser.realiseSentence(s_10) : 0})

    def affirmative_answer(self) -> str:
        # Extract the affirmative sentences that have not been used yet
        returnable_sentences = [key for key, value in self.affirmative_answers.items() if value == 1]

        # I randomly select one of the sentences
        affirmative_sentence = random.choice(returnable_sentences)

        # I update the dictionary to mark the sentence as used
        self.affirmative_answers.update({affirmative_sentence : 0})

        # I reset the dictionary if all the sentences have been used
        if (len(returnable_sentences) == 1):
            self.affirmative_answers = self.affirmative_answers.fromkeys(self.affirmative_answers, 1)

        return affirmative_sentence
    
    def generate_negative_answers(self):
        # 1. Create a sentence with the form "I'm sorry, but that's false."
        # Create a sentence with the form "I'm sorry."
        subj_1 = self.nlg_factory.createNounPhrase("I")
        verb_1 = self.nlg_factory.createVerbPhrase("be")
        obj_1 = self.nlg_factory.createNounPhrase("sorry")
        s_1 = self.nlg_factory.createClause(subj_1, verb_1, obj_1)

        # Create a sentence with the form "but that's false."
        prep_2 = self.nlg_factory.createPrepositionPhrase("but")
        subj_2 = self.nlg_factory.createNounPhrase("that")
        verb_2 = self.nlg_factory.createVerbPhrase("be")
        obj_2 = self.nlg_factory.createNounPhrase("false")
        subj_2.addPreModifier(prep_2)
        s_2 = self.nlg_factory.createClause(subj_2, verb_2, obj_2)

        # I tie the two sentences together with a comma
        c_1 = self.nlg_factory.createCoordinatedPhrase()
        c_1.setConjunction(",")
        c_1.addCoordinate(s_1)
        c_1.addCoordinate(s_2)
        
        # I add the sentence to the dictionary
        self.negative_answers.update({self.realiser.realiseSentence(c_1) : 1})

        # 2. Create a sentence with the form "It doesn't match with my prior knowledge."
        # Create a sentence with the form "It doesn't match"
        pron_3 = self.nlg_factory.createWord("it", LexicalCategory.PRONOUN)
        verb_3 = self.nlg_factory.createVerbPhrase("do match")
        verb_3.setFeature(Feature.NEGATED, True)
        s_3 = self.nlg_factory.createClause(pron_3, verb_3)
        
        # Create a sentence with the form "with my prior knowledge."
        prep_4 = self.nlg_factory.createPrepositionPhrase("with")
        subj_4 = self.nlg_factory.createNounPhrase("knowledge")
        adj_4 = self.nlg_factory.createAdjectivePhrase("prior")
        subj_4.addModifier(adj_4)
        pron_4 = self.nlg_factory.createWord("I", LexicalCategory.PRONOUN)
        pron_4.setFeature(Feature.POSSESSIVE, True)
        subj_4.setDeterminer(pron_4)
        prep_4.addComplement(subj_4)
        s_4 = self.nlg_factory.createClause(prep_4)

        # I tie the two sentences together without conjunction
        c_1 = self.nlg_factory.createCoordinatedPhrase()
        c_1.setConjunction("")
        c_1.addCoordinate(s_3)
        c_1.addCoordinate(s_4)

        # I add the sentence to the dictionary
        self.negative_answers.update({self.realiser.realiseSentence(c_1) : 0})

        # 3. Create a sentence with the form "That's not the answer that i expected."
        # Create a sentence with the form "That's not the answer"
        subj_5 = self.nlg_factory.createNounPhrase("that")
        verb_5 = self.nlg_factory.createVerbPhrase("be")
        verb_5.setFeature(Feature.NEGATED, True)
        obj_5 = self.nlg_factory.createNounPhrase("the", "answer")
        s_5 = self.nlg_factory.createClause(subj_5, verb_5, obj_5)

        # Create a sentence with the form "that i expected."
        subj_6 = self.nlg_factory.createNounPhrase("I")
        verb_6 = self.nlg_factory.createVerbPhrase("expect")
        verb_6.setFeature(Feature.TENSE, Tense.PAST)
        s_6 = self.nlg_factory.createClause(subj_6, verb_6)
        s_5.addComplement(s_6)
        
        # I add the sentence to the dictionary
        self.negative_answers.update({self.realiser.realiseSentence(s_5) : 0})

        # 4. Create a sentence with the form "I don't really think so."
        subj_7 = self.nlg_factory.createNounPhrase("I")
        verb_7 = self.nlg_factory.createVerbPhrase("think")
        verb_7.setFeature(Feature.NEGATED, True)
        adv_7 = self.nlg_factory.createAdverbPhrase("really")
        verb_7.addComplement(adv_7)
        adv_8 = self.nlg_factory.createAdverbPhrase("so")
        verb_7.addComplement(adv_8)
        s_7 = self.nlg_factory.createClause(subj_7, verb_7)
        
        # I add the sentence to the dictionary
        self.negative_answers.update({self.realiser.realiseSentence(s_7) : 0})

        # 5. Create a sentence with the form "I'm sorry, I doubt that's the correct answer."
        # Create a sentence with the form "I'm sorry"
        subj_8 = self.nlg_factory.createNounPhrase("I")
        verb_8 = self.nlg_factory.createVerbPhrase("be")
        obj_8 = self.nlg_factory.createNounPhrase("sorry")
        s_8 = self.nlg_factory.createClause(subj_8, verb_8, obj_8)
        
        # Create a sentence with the form "I doubt that's the correct answer."
        subj_9 = self.nlg_factory.createNounPhrase("I")
        verb_9 = self.nlg_factory.createVerbPhrase("doubt")
        s_9 = self.nlg_factory.createClause(subj_9, verb_9)

        # I tie the two sentences together with a comma
        c_9 = self.nlg_factory.createCoordinatedPhrase()
        c_9.setConjunction(",")
        c_9.addCoordinate(s_8)
        c_9.addCoordinate(s_9)

        
        # Create a sentence with the form "that's the correct answer."
        subj_10 = self.nlg_factory.createNounPhrase("that")
        verb_10 = self.nlg_factory.createVerbPhrase("be")
        obj_10 = self.nlg_factory.createNounPhrase("the", "answer")
        adj_10 = self.nlg_factory.createAdjectivePhrase("correct")
        obj_10.addModifier(adj_10)
        s_10 = self.nlg_factory.createClause(subj_10, verb_10, obj_10)

        c_10 = self.nlg_factory.createCoordinatedPhrase()
        c_10.setConjunction("")
        c_10.addCoordinate(c_9)
        c_10.addCoordinate(s_10)
        
        # I add the sentence to the dictionary
        self.negative_answers.update({self.realiser.realiseSentence(c_10) : 0})

    def generate_answer(self, affirmative: bool) -> str:
        # Extract the negative sentences that have not been used yet
        sentences = self.affirmative_answers if affirmative else self.negative_answers
        returnable_sentences = [key for key, value in sentences.items() if value == 1]

        # I randomly select one of the sentences
        extracted_sentence = random.choice(returnable_sentences)

        # I update the dictionary to mark the sentence as used
        sentences[extracted_sentence] = 0

        # I reset the dictionary if all the sentences have been used
        if (len(returnable_sentences) == 1):
            if (affirmative):
                self.affirmative_answers = self.affirmative_answers.fromkeys(self.affirmative_answers, 1)
            else:
                self.negative_answers = self.negative_answers.fromkeys(self.negative_answers, 1)

        return extracted_sentence
    
if __name__ == "__main__":
    nlg = NaturalLanguageGenerator()
    nlg.greetings()
    nlg.greets_user()
    nlg.ask_nth_question("How many children can a Jedi have?")
    nlg.generate_answer(True)
    nlg.generate_answer(False)