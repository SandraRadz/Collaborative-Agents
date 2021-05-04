import random
import time

import mesa

from utils import select_item_to_compare, find_difference, generate_answers, answers_is_equal


# todo leadership and mimicry

class Agent(mesa.Agent):
    """ An agent with fixed initial wealth."""

    def __init__(self, unique_id, model, talkativeness, agreeableness, critical_thinking, knowledge_sharing, name="Custom"):
        super().__init__(unique_id, model)
        self.talkativeness = talkativeness
        self.agreeableness = agreeableness
        self.critical_thinking = critical_thinking
        self.knowledge_sharing = knowledge_sharing
        self.answers = []
        self.answers = generate_answers(self.model.questions_num, ["a", "b", "c"])
        self.name = name

    def __str__(self):
        return f"{self.name} Agent (tl={self.talkativeness}, ag={self.agreeableness}, cr={self.critical_thinking}," \
               f"ks={self.knowledge_sharing})"

    def step(self):
        if self.talkativeness > random.random():
            self.model.controller.gui.change_agent_status(self.unique_id, "SHOWING", clean=True)
            # print(f"Agent {self.unique_id} is showing {self.answers} ({self.correct_answer_percent()} %)")
            for other_agent in self.model.schedule.agents:
                if other_agent.unique_id != self.unique_id and other_agent.agreeableness > random.random():
                    old_answers = tuple(other_agent.answers)
                    el_to_compare = select_item_to_compare(self, other_agent)
                    for el in el_to_compare:
                        other_agent.make_decision(el, self.answers[el])
                    if not answers_is_equal(old_answers, tuple(other_agent.answers)):
                        self.model.update_last_change()
                    new_correct_answers_percent = other_agent.correct_answer_percent()
                    self.model.controller.gui.change_agent_answers(other_agent, self.model.correct_answer,
                                                                   new_correct_answers_percent)
                    time.sleep(self.model.pause)
                    # print(f"Agent {other_agent.unique_id} changed his list from {old_answers} to {other_agent.answers} ({old_correct_answers_percent}% -> {new_correct_answers_percent} %)")

        else:
            self.model.controller.gui.change_agent_status(self.unique_id, "NOT SHOW", clean=True)
            # print(f"Agent {self.unique_id} does not want to show")
        time.sleep(self.model.pause)

    def correct_answer_percent(self):
        diff = find_difference(self.answers, self.model.correct_answer)
        correct_percent = 100 - len(diff) * 100 / len(self.model.correct_answer)
        return round(correct_percent, 2)

    def make_decision(self, question_id, new_answer):
        old_answer = self.answers[question_id]
        choose_better_answer = False
        if self.critical_thinking > random.random():
            choose_better_answer = True
        self.answers[question_id] = self.choose_answer(question_id, new_answer, choose_better_answer)

        # return if agent change his answer
        if old_answer != self.answers[question_id]:
            return True
        return False

    def choose_answer(self, question_id, variant2, choose_better):
        variant1 = self.answers[question_id]
        correct_answer = self.model.correct_answer[question_id]
        is_any_of_variant_correct = correct_answer == variant1 or correct_answer == variant2
        if choose_better and is_any_of_variant_correct:
            return correct_answer
        elif random.random() > 0.5:
            return variant1
        else:
            return variant2





