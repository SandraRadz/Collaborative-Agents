# from model import Answers_Model
#
# agents_number = 15
# iteration_number = 3
# correct_answer = ["a", "b", "c", "b", "a", "b", "c", "a", "b", "c", "c", "b"]
#
# model = Answers_Model(agents_number, correct_answer=correct_answer)
# for i in range(iteration_number):
#     print(f"{i} -----------------------------------------------------------")
#     print(f"max {model.max_model_percent()} %")
#     print(f"all {model.agent_percent()}")
#     model.step()

#let's inspect the results:
# out = model.datacollector.get_agent_vars_dataframe().groupby('Step').sum()
# print(out)
from tkinter import Tk

from model import AnswersModel
from view import AgentGUI


class Controller:
    def __init__(self):
        self.agents = []
        self.correct_answer = ["a", "b", "c", "b", "a", "b", "c", "a", "b", "c", "c", "b"]
        self.model = None
        self.run = False
        self.iter_num = 0

    def delete_agent_prototype(self, item_index):
        self.agents.pop(item_index)

    def add_agent_prototype(self, agent):
        self.agents.append(agent)

    def run_model(self, iteration_num=None):
        if not self.run:
            self.model = AnswersModel(correct_answer=self.correct_answer, agents=self.agents)
            self.run = True
            self.iter_num = 0

            while self.run and (not iteration_num or self.iter_num < iteration_num):
                self.model.step()
                self.iter_num += 1


if __name__ == "__main__":
    root = Tk()
    controller = Controller()
    my_gui = AgentGUI(root, controller)
    root.mainloop()
