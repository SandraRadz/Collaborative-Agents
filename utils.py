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