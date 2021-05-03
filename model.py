import mesa
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.time import RandomActivation, BaseScheduler
from scipy.stats import truncnorm
from agent import Agent

import logging

from utils import answers_is_equal, get_truncated_normal, generate_answers

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


class AnswersModel(mesa.Model):

    def __init__(self, question_num, agents_param):
        super().__init__()
        self.num_agents = len(agents_param)
        self.schedule = BaseScheduler(self)
        self.running = True
        self.questions_num = question_num
        # self.correct_answer = ["a", "b", "c", "b", "a", "b", "c", "a", "b", "c", "c", "b"]
        self.correct_answer = generate_answers(self.questions_num, ["a", "b", "c"])
        print(f"correct_answers {self.correct_answer}")

        self.datacollector = DataCollector(
            model_reporters={"Tot informed": self.compute_correct_answer_percent},
            agent_reporters={"talkativeness": "talkativeness"})

        for agent_param in agents_param:
            unique_id = len(self.schedule.agents)
            a = Agent(unique_id, self, agent_param["talkativeness"], agent_param["agreeableness"],
                      agent_param["critical_thinking"], agent_param["knowledge_sharing"])
            self.schedule.add(a)

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

        if self.all_agents_equal():
            print("DONE!")
            self.running = False
            return True
        return False

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
