import time

from agent import Agent
from model import AnswersModel


class Controller:
    def __init__(self):
        self.agents_params = []
        self.model = None
        self.run = False
        self.iter_num = 0
        self.equal = False

    def delete_agent_prototype(self, item_index):
        self.agents_params.pop(item_index)

    def add_agent_prototype(self, agent):
        self.agents_params.append(agent)

    def run_model(self, iteration_num=None):
        pause = 1
        while self.run and (not iteration_num or self.iter_num < iteration_num) and not self.equal:
            print(self.iter_num)
            self.equal = self.model.step()
            self.iter_num += 1
            time.sleep(pause)

    def setup_model(self, question_num=12):
        self.run = False
        self.model = AnswersModel(question_num=question_num, agents_param=self.agents_params)
        self.iter_num = 0
        self.equal = False

    def pause_model(self):
        self.run = False
        print("-------------------------------------------------------")
        print(self.iter_num)

    # def stop_model(self):
    #     self.run = False
    #     self.model = None
    #     print("-------------------------------------------------------")
    #     print(self.iter_num)
