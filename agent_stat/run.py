import csv

from agent_stat.agent_model import AnswersModel


def run_report():
    pass


def generate_report1():
    agents_number = 15
    iteration_number = 50

    talkativeness = [0.1, 0.5, 0.9]
    agreeableness = [0.1, 0.5, 0.9]
    knowledge_sharing = [0.1, 0.5, 0.9]
    mimicry = [None, 0.5, 0.9]
    critical_thinking = [0.1, 0.5, 0.9]

    with open('res_with_percent5.csv', 'w', newline='') as csvfile:
        fieldnames = ['talkativeness', 'agreeableness', 'knowledge_sharing', 'mimicry', 'critical_thinking', 'equal',
                      'loop', 'timeout', "percent"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for agent in range(agents_number):
            for tl in talkativeness:
                for ag in agreeableness:
                    for ksh in knowledge_sharing:
                        for mm in mimicry:
                            for cth in critical_thinking:
                                agent_params = {
                                    "talkativeness": tl, "agreeableness": ag, "knowledge_sharing": ksh,
                                    "mimicry": mm, "critical_thinking": cth
                                }
                                agents = [agent_params for _ in range(agents_number)]
                                timeout = 0
                                done = 0
                                circle = 0
                                percent_list = []
                                for _ in range(50):
                                    model = AnswersModel(agents_number, agents)
                                    res_status = "timeout"
                                    for i in range(iteration_number):
                                        res, status = model.step()
                                        if res:
                                            res_status = status
                                            break
                                    if res_status == "timeout":
                                        timeout += 1
                                    elif res_status == "loop":
                                        circle += 1
                                    elif res_status == "equal":
                                        percent_list.append(str(model.schedule.agents[0].correct_answer_percent()))
                                        done += 1
                                res_dict = agent_params
                                res_dict["equal"] = done
                                res_dict["loop"] = circle
                                res_dict["timeout"] = timeout
                                res_dict["percent"] = ", ".join(percent_list)
                                print(res_dict)
                                writer.writerow(res_dict)


def generate_report2():
    agents_number = 15
    iteration_number = 100

    agent_class_1 = {"talkativeness": 0.9, "agreeableness": 0.9, "knowledge_sharing": 0.9,
                     "mimicry": None, "critical_thinking": 0.7}

    agent_class_2 = {"talkativeness": 0.1, "agreeableness": 0.1, "knowledge_sharing": 0.1,
                     "mimicry": None, "critical_thinking": 0.5}

    with open('report2_9.csv', 'w', newline='') as csvfile:
        fieldnames = ['first_type_num', 'second_type_num', 'equal', 'loop', 'timeout', "percent"]
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)

        for i in range(agents_number+1):
            agent_1_num = i
            agent_2_num = agents_number - i
            agents = []
            for k in range(agent_1_num):
                agents.append(agent_class_1)
            for k in range(agent_2_num):
                agents.append(agent_class_2)
            timeout = 0
            done = 0
            circle = 0
            percent_list = []
            for _ in range(100):
                model = AnswersModel(agents_number, agents)
                res_status = "timeout"
                for i in range(iteration_number):
                    res, status = model.step()
                    if res:
                        res_status = status
                        break
                if res_status == "timeout":
                    timeout += 1
                elif res_status == "loop":
                    circle += 1
                elif res_status == "equal":
                    percent_list.append(str(model.schedule.agents[0].correct_answer_percent()))
                    done += 1
            percent = ", ".join(percent_list)
            print([agent_1_num, agent_2_num, done, circle, timeout, percent])
            writer.writerow([agent_1_num, agent_2_num, done, circle, timeout, percent])

if __name__ == "__main__":
    generate_report2()
