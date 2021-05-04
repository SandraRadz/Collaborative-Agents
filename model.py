import mesa
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.time import RandomActivation, BaseScheduler
from scipy.stats import truncnorm
from agent import Agent

import logging

from utils import answers_is_equal, generate_answers

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


class AnswersModel(mesa.Model):

    def __init__(self, question_num, agents_param, controller):
        super().__init__()
        self.num_agents = len(agents_param)
        self.schedule = BaseScheduler(self)
        self.running = True
        self.questions_num = question_num
        self.pause = 0.25
        self.controller = controller
        # self.correct_answer = ["a", "b", "c", "b", "a", "b", "c", "a", "b", "c", "c", "b"]
        self.correct_answer = generate_answers(self.questions_num, ["a", "b", "c"])
        self.iter_num = 0
        self.last_change = 0

        self.datacollector = None

        for agent_param in agents_param:
            unique_id = len(self.schedule.agents)
            a = Agent(unique_id, self, agent_param["talkativeness"], agent_param["agreeableness"],
                      agent_param["critical_thinking"], agent_param["knowledge_sharing"])
            self.schedule.add(a)

    def step(self):
        self.iter_num += 1
        self.schedule.step()
        if self.all_agents_equal():
            return False, "ALL EQUAL!"
        diff = self.iter_num - self.last_change
        if diff > 2:
            return False, f"NO CHANGES LAST {diff} ROUND"
        return True, None

    def all_agents_equal(self):
        first_agent_answers = self.schedule.agents[0].answers
        for agent in self.schedule.agents[1:]:
            if not answers_is_equal(tuple(first_agent_answers), tuple(agent.answers)):
                return False
        return True

    def set_pause(self, pause):
        self.pause = pause

    def update_last_change(self):
        self.last_change = self.iter_num
