
import mesa
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.time import RandomActivation, BaseScheduler
from scipy.stats import truncnorm
from agent import Agent

import logging

from utils import answers_is_equal, get_truncated_normal

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


class AnswersModel(mesa.Model):

    def __init__(self, correct_answer, agents):
        super().__init__()
        self.num_agents = len(agents)
        self.schedule = BaseScheduler(self)
        self.running = True
        self.correct_answer = correct_answer
        self.questions_num = len(correct_answer)

        self.datacollector = DataCollector(
            model_reporters={"Tot informed": self.compute_correct_answer_percent},
            agent_reporters={"talkativeness": "talkativeness"})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

        if self.all_agents_equal():
            self.running = False

    # todo remove
    def compute_correct_answer_percent(self):
        # for i in self.schedule.agents:
        #     compute_answer_percent(i)
        return 50

    def agent_percent(self):
        return [agent.correct_answer_percent() for agent in self.schedule.agents]

    def max_model_percent(self):
        return max(self.agent_percent())

    def all_agents_equal(self):
        first_agent = self.schedule.agents[0]
        for agent in self.schedule.agents[1:]:
            if not answers_is_equal(first_agent.answers, agent.answers):
                return False
        return True

