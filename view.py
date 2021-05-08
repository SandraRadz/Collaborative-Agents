import random
from threading import Thread
from tkinter import Label, Button, Canvas, Listbox, END, NORMAL, DISABLED, Scrollbar, StringVar, OptionMenu, Entry, \
    Toplevel, Menu

from agent_types import AGENT_TYPES, AGENT1, AGENT2, AGENT3, AGENT4

from utils import get_truncated_normal, validate_value

iteration_number = 300


class AgentGUI:
    def __init__(self, master, controller):
        master.title("Collaborative Agent")
        self.controller = controller
        self.agent_types = AGENT_TYPES

        mainmenu = Menu(master)
        master.config(menu=mainmenu)
        mainmenu.add_command(label='Settings', command=self.setting_button)

        self.step_num = Label(text="round: 1", font="Verdana 10")
        self.step_num.grid(row=0, column=9, sticky="nw")

        AgentButton(master, AGENT1, 1, 1, command=lambda a=self.agent_types[AGENT1]: self.add_to_list(a))
        AgentButton(master, AGENT2, 1, 3, command=lambda a=self.agent_types[AGENT2]: self.add_to_list(a))
        AgentButton(master, AGENT3, 1, 5, command=lambda a=self.agent_types[AGENT3]: self.add_to_list(a))
        AgentButton(master, AGENT4, 1, 7, command=lambda a=self.agent_types[AGENT4]: self.add_to_list(a))
        AgentButton(master, "Random", 2, 1, self.add_random_to_list)

        self.agent_list = Listbox(master, width=55, height=10)
        self.agent_list.grid(row=3, column=1, columnspan=5, padx=7, sticky="news")

        Button(master, text="Delete", command=self.del_list).grid(row=3, column=7, sticky='new', padx=7)

        self.stop_button = Button(master, text="Set Up", command=self.setup)
        self.stop_button.grid(row=4, column=1, sticky='ew', padx=7, pady=1)

        self.start_button = Button(master, text="Run", state=DISABLED, command=self.start)
        self.start_button.grid(row=4, column=3, sticky='ew', padx=7, pady=1)

        self.pause_button = Button(master, text="Pause", state=DISABLED, command=self.pause)
        self.pause_button.grid(row=4, column=5, sticky='ew', padx=7, pady=1)

        Label(text="Question number:", font="Verdana 10").grid(row=5, column=1, padx=7, pady=1, sticky="nw")

        self.question_number = Entry(width=20)
        self.question_number.insert(END, '12')
        self.question_number.grid(row=5, column=3, sticky="new")

        self.info_label = Label(text="", font="Verdana 12", justify='left')
        self.info_label.grid(row=9, column=0, columnspan=6, sticky="new")

        self.canvas = Canvas(master, width=750, height=850, bg='white')
        self.canvas.grid(row=1, column=9, columnspan=10, rowspan=10)

        self.current_state = {}

    def start(self):
        self.start_button.configure(state=DISABLED)
        self.stop_button.configure(state=NORMAL)
        self.pause_button.configure(state=NORMAL)
        t1 = Thread(target=self.run_model)
        t1.start()

    def run_model(self):
        self.controller.run_model()

    def setup(self):
        self.start_button.configure(state=NORMAL)
        self.step_num.configure(text="round: 1")
        if self.controller.agents_params:
            question_num_str = self.question_number.get()
            try:
                question_num = int(question_num_str)
            except ValueError:
                question_num = 12
                self.question_number.delete(0, END)
                self.question_number.insert(0, 12)
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
        mimicry = None
        if agent_params['mimicry']:
            mimicry = round(agent_params['mimicry'], 2)

        # critical thinking not depends on character
        if not agent_params["critical_thinking"]:
            agent_params["critical_thinking"] = get_truncated_normal(mean=0.4, sd=0.2, low=0, upp=1).rvs()

        str_agent = f"{agent_params['name']} (tl={round(agent_params['talkativeness'], 2)}, " \
                    f"ag={round(agent_params['agreeableness'], 2)}, cr={round(agent_params['critical_thinking'], 2)}," \
                    f"ks={round(agent_params['knowledge_sharing'], 2)}, mm={mimicry})"
        self.agent_list.insert(END, str_agent)
        self.controller.add_agent_prototype(agent_params)

    def add_random_to_list(self):
        if random.random() > 0.5:
            mimicry = get_truncated_normal(mean=0.7, sd=0.3, low=0, upp=1).rvs()
        else:
            mimicry = None
        agent_params = {"talkativeness": get_truncated_normal(mean=0.5, sd=0.3, low=0, upp=1).rvs(),
                        "agreeableness": get_truncated_normal(mean=0.5, sd=0.3, low=0, upp=1).rvs(),
                        "knowledge_sharing": get_truncated_normal(mean=0.5, sd=0.3, low=0, upp=1).rvs(),
                        "critical_thinking": get_truncated_normal(mean=0.4, sd=0.2, low=0, upp=1).rvs(),
                        "mimicry": mimicry,
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
                item = self.canvas.create_text(x_pos, start_y_pos, text=agent.answers[i], font="Verdana 14",
                                               fill="green")
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
        self.step_num.configure(text=f"round: {step+1}")

    def set_info_text(self, text, color="black"):
        self.info_label.configure(text=text, fg=color)

    def setting_button(self):
        t1 = Thread(target=self.change_settings)
        t1.start()

    def change_settings(self):
        settings_window = Toplevel()
        settings_window.geometry('800x300')
        Label(settings_window, text="Agent type:", font="Verdana 12").grid(row=0, column=0, padx=7, pady=1, sticky="nw")
        Label(settings_window, text="talkativeness", font="Verdana 12").grid(row=0, column=1, padx=7, pady=1, sticky="nw")
        Label(settings_window, text="agreeableness", font="Verdana 12").grid(row=0, column=2, padx=7, pady=1, sticky="nw")
        Label(settings_window, text="knowledge_sharing", font="Verdana 12").grid(row=0, column=3, padx=7, pady=1, sticky="nw")
        Label(settings_window, text="critical_thinking", font="Verdana 12").grid(row=0, column=4, padx=7, pady=1,
                                                                                 sticky="nw")
        Label(settings_window, text="mimicry", font="Verdana 12").grid(row=0, column=5, padx=7, pady=1, sticky="nw")

        res = {}
        res[AGENT1] = self.__show_agent_setting(settings_window, AGENT1, 1)
        res[AGENT2] = self.__show_agent_setting(settings_window, AGENT2, 2)
        res[AGENT3] = self.__show_agent_setting(settings_window, AGENT3, 3)
        res[AGENT4] = self.__show_agent_setting(settings_window, AGENT4, 4)

        Button(settings_window, text="Save", command=lambda: self.save_changes(res, settings_window)).grid(row=5, column=0, sticky='new', padx=7, pady=1)

    def save_changes(self, el_list, settings_window):
        self.__update_value(AGENT1, el_list)
        self.__update_value(AGENT2, el_list)
        self.__update_value(AGENT3, el_list)
        self.__update_value(AGENT4, el_list)
        print(self.agent_types)
        settings_window.destroy()

    def __update_value(self, agent_id, value_dict):
        talk = value_dict[agent_id]["talkativeness"].get()
        if validate_value(talk):
            self.agent_types[agent_id]["talkativeness"] = float(talk)
        agr = value_dict[agent_id]["agreeableness"].get()
        if validate_value(agr):
            self.agent_types[agent_id]["agreeableness"] = float(agr)
        kn_sh = value_dict[agent_id]["knowledge_sharing"].get()
        if validate_value(kn_sh):
            self.agent_types[agent_id]["knowledge_sharing"] = float(kn_sh)

        cr_th = value_dict[agent_id]["critical_thinking"].get()
        if not cr_th:
            cr_th = None
        elif validate_value(cr_th):
            cr_th = float(cr_th)

        self.agent_types[agent_id]["critical_thinking"] = cr_th

        mim = value_dict[agent_id]["mimicry"].get()
        if not mim:
            mim = None
        elif validate_value(mim):
            mim = float(mim)
        self.agent_types[agent_id]["mimicry"] = mim

    def __show_agent_setting(self, root_element, agent_id, row):
        Label(root_element, text=AGENT_TYPES[agent_id]["name"], font="Verdana 12").grid(row=row, column=0, padx=7,
                                                                                        pady=1, sticky="nw")
        talk = Entry(root_element, width=5)
        talk.insert(END, self.agent_types[agent_id]["talkativeness"])
        talk.grid(row=row, column=1, padx=7, sticky="ew")
        agr = Entry(root_element, width=5)
        agr.insert(END, self.agent_types[agent_id]["agreeableness"])
        agr.grid(row=row, column=2, padx=7, sticky="ew")
        kn_sh = Entry(root_element, width=5)
        kn_sh.insert(END, self.agent_types[agent_id]["knowledge_sharing"])
        kn_sh.grid(row=row, column=3, padx=7, sticky="ew")


        critical = self.agent_types[agent_id]["critical_thinking"] or ""
        cr_th = Entry(root_element, width=5)
        cr_th.insert(END, critical)
        cr_th.grid(row=row, column=4, padx=7, sticky="ew")

        mimicry = self.agent_types[agent_id]["mimicry"] or ""
        mimi = Entry(root_element, width=5)
        mimi.insert(END, mimicry)
        mimi.grid(row=row, column=5, padx=7, sticky="ew")
        return {"talkativeness": talk, "agreeableness": agr, "knowledge_sharing": kn_sh, 'critical_thinking': cr_th,
                "mimicry": mimi}


class AgentButton(Button):

    def __init__(self, master, name, row, column, command=None):
        super().__init__(master=master, text=name, width=15, height=2, command=command)
        self.grid(row=row, column=column, padx=7, pady=1, sticky='nwe')
