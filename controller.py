from tkinter import Tk

from model import AnswersModel
from view import AgentGUI


class Controller:
    def __init__(self):
        self.agents_params = []
        self.model = None
        self.run = False
        self.equal = False

        root = Tk()
        self.gui = AgentGUI(root, self)
        root.mainloop()

    def delete_agent_prototype(self, item_index):
        self.agents_params.pop(item_index)

    def add_agent_prototype(self, agent):
        self.agents_params.append(agent)

    def run_model(self, iteration_num=None):
        if self.model:
            self.run = True
            while self.run and (not iteration_num or self.model.iter_num < iteration_num):
                self.run, message = self.model.step()
                self.gui.set_step(self.model.iter_num)
                if message:
                    self.gui.set_info_text(message)

    def setup_model(self, question_num=12):
        self.run = False
        self.model = AnswersModel(question_num=question_num, agents_param=self.agents_params, controller=self)

    def pause_model(self):
        self.run = False
