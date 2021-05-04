import math
import random

from scipy.stats import truncnorm


def answers_is_equal(list1, list2):
    if len(list1) != len(list2):
        return False
    for i in range(len(list1)):
        if list1[i] != list2[i]:
            return False
    return True


def find_difference(list1, list2):
    if len(list1) != len(list2):
        raise IndexError
    res = []
    for i in range(len(list1)):
        if list1[i] != list2[i]:
            res.append(i)
    return res


def select_item_to_compare(agent1, agent2):
    # who will be tired first
    knowledge_sharing = min(agent1.knowledge_sharing, agent2.knowledge_sharing)
    diff = find_difference(agent1.answers, agent2.answers)
    random.shuffle(diff)
    num_of_comp = math.ceil(len(diff) * knowledge_sharing) - 1
    return diff[:num_of_comp]


def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)


def generate_correct_answers(questions_num, answer_options):
    answers = []
    for i in range(questions_num):
        answers.append(answer_options[int(random.random() * len(answer_options))])
    return answers


def generate_agent_answers(questions_num, answer_options, critical_thinking=None, correct_answer=None):
    answers = []
    if critical_thinking and correct_answer:
        correct_percent = random.uniform(max(0, critical_thinking-0.3), min(1, critical_thinking+0.3))
        correct_number = int(correct_percent * questions_num)
        index = list(range(0, questions_num))
        random.shuffle(index)
        correct_num = index[:correct_number]
        for i in range(questions_num):
            if i in correct_num:
                answers.append(correct_answer[i])
            else:
                incorrect_answer_options = list(filter(lambda x: x!= correct_answer[i], answer_options))
                answers.append(incorrect_answer_options[int(random.random() * len(incorrect_answer_options))])
    return answers