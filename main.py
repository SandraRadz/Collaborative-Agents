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

# let's inspect the results:
# out = model.datacollector.get_agent_vars_dataframe().groupby('Step').sum()
# print(out)
from tkinter import Tk

from controller import Controller

if __name__ == "__main__":
    controller = Controller()
