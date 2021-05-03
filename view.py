from msilib.schema import ListBox
from threading import Thread
from tkinter import Tk, Label, Button, Canvas, Frame, Listbox, LEFT, Scrollbar, Y, X, END

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

        # added agents
        self.agent_list = Listbox(master, width=45, height=10)
        self.agent_list.grid(row=3, column=1, columnspan=3, padx=7, sticky="news")
        # vsb = Scrollbar(self.agent_list, orient="vertical", command=self.agent_list.yview)
        # vsb.grid(row=3, column=4, sticky='ns')
        # self.agent_list.configure(yscrollcommand=vsb.set)

        # vsb = Scrollbar(master, orient="vertical", command=self.agent_list.yview)
        # vsb.grid(row=4, column=2, sticky='ns')
        # self.agent_list.configure(yscrollcommand=vsb.set)

        Button(master, text="Delete", command=self.del_list).grid(row=3, column=5, sticky='n', padx=7)

        self.canva = Canvas(master, width=550, height=550, bg='white')
        self.canva.grid(row=1, column=7, rowspan=10)

        # self.label = Label(master, text="This is our first GUI!")
        # self.label.pack()
        #
        # self.start_button = Button(master, text="Start", command=self.start)
        # self.start_button.pack()
        #
        # self.stop_button = Button(master, text="Stop", command=self.stop)
        # self.stop_button.pack()
        #
        # self.iteration_num = None
        # self.model = None
        # self.run = False
        # self.i = 0

        # self.close_button = Button(master, text="Close", command=master.quit)
        # self.close_button.pack()

    def start(self):
        # Call work function
        t1 = Thread(target=self.run_model)
        t1.start()

    def run_model(self):
        self.controller.run_model()

    def stop(self):
        if self.model:
            self.run = False
            print(f"Stop after {self.i} steps")

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


class AgentButton(Button):

    def __init__(self, master, name, row, column, command=None):
        super().__init__(master=master, text=name, width=17, height=2, command=command)
        self.grid(row=row, column=column, padx=7, pady=1, sticky='nwe')
