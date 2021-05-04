from threading import Thread
from tkinter import Label, Button, Canvas, Listbox, END, NORMAL, DISABLED

from agent_types import AGENT_TYPES, AGENT1, AGENT2, AGENT3

from utils import get_truncated_normal

iteration_number = 300


class AgentGUI:
    def __init__(self, master, controller):
        master.title("Collaborative Agent")
        self.controller = controller

        self.step_num = Label(text="round: 0", font="Verdana 10")
        self.step_num.grid(row=0, column=7, sticky="nw")

        AgentButton(master, "Agent1", 1, 1, command=lambda a=AGENT_TYPES[AGENT1]: self.add_to_list(a))
        AgentButton(master, "Agent2", 1, 3, command=lambda a=AGENT_TYPES[AGENT2]: self.add_to_list(a))
        AgentButton(master, "Agent3", 1, 5, command=lambda a=AGENT_TYPES[AGENT3]: self.add_to_list(a))
        AgentButton(master, "Random", 2, 1, self.add_random_to_list)

        self.agent_list = Listbox(master, width=45, height=10)
        self.agent_list.grid(row=3, column=1, columnspan=3, padx=7, sticky="news")
        # vsb = Scrollbar(self.agent_list, orient="vertical", command=self.agent_list.yview)
        # vsb.grid(row=3, column=4, sticky='ns')
        # self.agent_list.configure(yscrollcommand=vsb.set)

        Button(master, text="Delete", command=self.del_list).grid(row=3, column=5, sticky='new', padx=7)

        self.stop_button = Button(master, text="Set Up", command=self.setup)
        self.stop_button.grid(row=4, column=1, sticky='ew', padx=7, pady=1)

        self.start_button = Button(master, text="Run", state=DISABLED, command=self.start)
        self.start_button.grid(row=4, column=3, sticky='ew', padx=7, pady=1)

        self.pause_button = Button(master, text="Pause", state=DISABLED, command=self.pause)
        self.pause_button.grid(row=4, column=5, sticky='ew', padx=7, pady=1)

        self.info_label = Label(text="", font="Verdana 12", justify='left')
        self.info_label.grid(row=7, column=0, columnspan=6, sticky="ew")

        self.canvas = Canvas(master, width=550, height=550, bg='white')
        self.canvas.grid(row=1, column=7, columnspan=10, rowspan=10)

        self.current_state = {}

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
        self.start_button.configure(state=NORMAL)
        self.step_num.configure(text="round: 0")
        if self.controller.agents_params:
            question_num = 12
            self.controller.setup_model(question_num=question_num)
            self.show_agents()
        else:
            self.set_info_text("PLEASE, ADD AGENTS", "red")

    def pause(self):
        self.controller.pause_model()
        self.start_button.configure(state=NORMAL)
        self.pause_button.configure(state=DISABLED)

    def del_list(self):
        select = self.agent_list.curselection()
        if select:
            self.agent_list.delete(select)
            self.controller.delete_agent_prototype(select[0])

    def add_to_list(self, agent_params):
        self.set_info_text("")
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
        self.canvas.delete("all")
        agents = self.controller.model.schedule.agents
        correct_answer = self.controller.model.correct_answer
        start_x = 50
        start_y = 50
        # {id: {'list': [a, b, c, f], 'percent': 90, 'status': "SHOWING"}}
        self.current_state = {}
        for i in range(len(agents)):
            agent = agents[i]
            res = self.draw_agent(agent, correct_answer, start_x, start_y)
            self.current_state[i] = res
            start_y += 40

    def draw_agent(self, agent, correct_answer, start_x_pos, start_y_pos):
        x_pos = start_x_pos
        self.canvas.create_text(x_pos, start_y_pos, text=f"id: {agent.unique_id}", font="Verdana 14")
        x_pos += 55
        res = {'list': []}
        for i in range(len(agent.answers)):
            if agent.answers[i] == correct_answer[i]:
                item = self.canvas.create_text(x_pos, start_y_pos, text=agent.answers[i], font="Verdana 14", fill="green")
            else:
                item = self.canvas.create_text(x_pos, start_y_pos, text=agent.answers[i], font="Verdana 14", fill="red")
            res['list'].append(item)
            x_pos += 10
        x_pos += 50
        percent = agent.correct_answer_percent()
        percent_el = self.canvas.create_text(x_pos, start_y_pos, text=f"{percent}%", font="Verdana 14")
        res["percent"] = percent_el
        x_pos += 100
        status = self.canvas.create_text(x_pos, start_y_pos, text=f"", font="Verdana 14")
        res["status"] = status
        return res

    def change_agent_answers(self, agent, correct_answer, percent):
        line_id = agent.unique_id
        for i in range(len(agent.answers)):
            el = self.current_state[line_id]["list"][i]
            if agent.answers[i] == correct_answer[i]:
                self.canvas.itemconfig(el, text=agent.answers[i], fill="green")
            else:
                self.canvas.itemconfig(el, text=agent.answers[i], fill="red")
            el_percent = self.current_state[line_id]["percent"]
            self.canvas.itemconfig(el_percent, text=f"{percent}%")

    def change_agent_status(self, agent_id, status, clean=True):
        if clean:
            for key, value in self.current_state.items():
                self.canvas.itemconfig(value["status"], text="")
        self.canvas.itemconfig(self.current_state[agent_id]["status"], text=status)

    def set_step(self, step):
        self.step_num.configure(text=f"round: {step}")

    def set_info_text(self, text, color="black"):
        self.info_label.configure(text=text, fg=color)


class AgentButton(Button):

    def __init__(self, master, name, row, column, command=None):
        super().__init__(master=master, text=name, width=17, height=2, command=command)
        self.grid(row=row, column=column, padx=7, pady=1, sticky='nwe')
