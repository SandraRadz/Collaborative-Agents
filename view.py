from msilib.schema import ListBox
from threading import Thread
from tkinter import Tk, Label, Button, Canvas, Frame, Listbox, LEFT, Scrollbar, Y, X, END, NORMAL, DISABLED

from agent_types import AGENT_TYPES, AGENT1, AGENT2, AGENT3
from model import AnswersModel

# agents_number = 15
from utils import get_truncated_normal

iteration_number = 300


class AgentGUI:
    def __init__(self, master, controller):
        master.title("Collaborative Agent")
        self.controller = controller

        self.agent_buttons = []

        AgentButton(master, "Agent1", 1, 1, command=lambda a=AGENT_TYPES[AGENT1]: self.add_to_list(a))
        AgentButton(master, "Agent2", 1, 3, command=lambda a=AGENT_TYPES[AGENT2]: self.add_to_list(a))
        AgentButton(master, "Agent3", 1, 5, command=lambda a=AGENT_TYPES[AGENT3]: self.add_to_list(a))
        AgentButton(master, "Random", 2, 1, self.add_random_to_list)

        self.agent_list = Listbox(master, width=45, height=10)
        self.agent_list.grid(row=3, column=1, columnspan=3, padx=7, sticky="news")
        # vsb = Scrollbar(self.agent_list, orient="vertical", command=self.agent_list.yview)
        # vsb.grid(row=3, column=4, sticky='ns')
        # self.agent_list.configure(yscrollcommand=vsb.set)

        Button(master, text="Delete", command=self.del_list).grid(row=3, column=5, sticky='n', padx=7)

        self.stop_button = Button(master, text="Set Up", command=self.setup)
        self.stop_button.grid(row=4, column=1, sticky='n', padx=7)

        self.start_button = Button(master, text="Run", command=self.start)
        self.start_button.grid(row=5, column=1, sticky='n', padx=7)

        self.pause_button = Button(master, text="Pause", state=DISABLED, command=self.pause)
        self.pause_button.grid(row=5, column=3, sticky='n', padx=7)

        # self.stop_button = Button(master, text="Stop", state=DISABLED, command=self.stop)
        # self.stop_button.grid(row=5, column=5, sticky='n', padx=7)

        self.canvas = Canvas(master, width=550, height=550, bg='white')
        self.canvas.grid(row=1, column=7, rowspan=10)

    def start(self):
        self.start_button.configure(state=DISABLED)
        self.stop_button.configure(state=NORMAL)
        self.pause_button.configure(state=NORMAL)
        # Call work function
        t1 = Thread(target=self.run_model)
        t1.start()

    def run_model(self):
        self.controller.run_model()

    def setup(self):
        self.canvas.delete("all")
        if self.controller.agents_params:
            question_num = 12
            self.controller.setup_model(question_num=question_num)
            self.show_agents()
        else:
            print("NO agents")

    def pause(self):
        self.controller.pause_model()
        self.start_button.configure(state=NORMAL)
        self.pause_button.configure(state=DISABLED)
        # self.stop_button.configure(state=NORMAL)

    # def stop(self):
    #     self.controller.stop_model()
    #     self.start_button.configure(state=NORMAL)
    #     self.pause_button.configure(state=DISABLED)
    #     self.stop_button.configure(state=DISABLED)

    def del_list(self):
        select = self.agent_list.curselection()
        if select:
            self.agent_list.delete(select)
            self.controller.delete_agent_prototype(select[0])

    def add_to_list(self, agent_params):
        str_agent = f"{agent_params['name']} Agent (tl={round(agent_params['talkativeness'], 2)}, " \
                    f"ag={round(agent_params['agreeableness'], 2)}, cr={round(agent_params['critical_thinking'], 2)}," \
                    f"ks={round(agent_params['knowledge_sharing'], 2)})"
        self.agent_list.insert(END, str_agent)
        self.controller.add_agent_prototype(agent_params)

    def add_random_to_list(self):
        agent_params = {"talkativeness": get_truncated_normal(mean=0.7, sd=0.4, low=0, upp=1).rvs(),
                        "agreeableness": get_truncated_normal(mean=0.7, sd=0.4, low=0, upp=1).rvs(),
                        "critical_thinking": get_truncated_normal(mean=0.7, sd=0.4, low=0, upp=1).rvs(),
                        "knowledge_sharing": get_truncated_normal(mean=0.7, sd=0.4, low=0, upp=1).rvs(),
                        "name": "random"}
        self.add_to_list(agent_params)

    def show_agents(self):
        agents = self.controller.model.schedule.agents
        correct_answer = self.controller.model.correct_answer
        start_x = 50
        start_y = 50
        for agent in agents:
            self.draw_agent(agent, correct_answer, start_x, start_y)
            start_y += 40

    def draw_agent(self, agent, correct_answer, start_x_pos, start_y_pos):
        x_pos = start_x_pos
        self.canvas.create_text(x_pos, start_y_pos, text=f"id: {agent.unique_id}", font="Verdana 14")
        x_pos += 55

        for i in range(len(agent.answers)):
            if agent.answers[i] == correct_answer[i]:
                self.canvas.create_text(x_pos, start_y_pos, text=agent.answers[i], font="Verdana 14", fill="green")
            else:
                self.canvas.create_text(x_pos, start_y_pos, text=agent.answers[i], font="Verdana 14", fill="red")
            x_pos += 10
        x_pos += 50
        percent = agent.correct_answer_percent()
        self.canvas.create_text(x_pos, start_y_pos, text=f"{percent}%", font="Verdana 14")



class AgentButton(Button):

    def __init__(self, master, name, row, column, command=None):
        super().__init__(master=master, text=name, width=17, height=2, command=command)
        self.grid(row=row, column=column, padx=7, pady=1, sticky='nwe')
