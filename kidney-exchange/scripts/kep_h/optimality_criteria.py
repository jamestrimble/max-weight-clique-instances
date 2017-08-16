from abc import ABCMeta, abstractmethod
from kep_h_pool_optimiser import OptimisationException

def get_criteria(s):
    names = s.split(":")
    if names == []:
        raise OptimisationException(
                "There must be at least one optimality criterion")
    return [get_criterion(name) for name in names]
    

def get_criterion(name):
    if name=="effective": return MaxEffectivePairwise()
    if name=="size":      return MaxTransplants()
    if name=="backarc":   return MaxBackarcs()
    if name=="weight":    return MaxWeight()
    if name=="intweight": return MaxIntWeight()
    if name=="3way":      return MinThreeWay()
    if name=="inverse3way":      return MaxInverseThreeWay()
    if name=="null":      return MaxNull()
    raise OptimisationException(
            "Unrecognised optimality criterion: {}".format(name))

class OptCriterion(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def chain_val(self, chain):
        pass

    @abstractmethod
    def cycle_val(self, cycle):
        pass

    @abstractmethod
    def altruist_val(self, altruist):
        pass

class MaxTransplants(OptCriterion):
    sense = 'MAX'

    def chain_val(self, chain):
        return chain.n_transplants()

    def cycle_val(self, cycle):
        return cycle.n_transplants()

    def altruist_val(self, altruist):
        return 1

class MaxEffectivePairwise(OptCriterion):
    sense = 'MAX'

    def chain_val(self, chain):
        return 1

    def cycle_val(self, cycle):
        for i in range(len(cycle.pd_pairs)):
            if cycle.pd_pairs[i].patient.has_backarc_to(cycle.pd_pairs[i-1].patient):
                return 1
        return 0

    def altruist_val(self, altruist):
        return 0

class MaxBackarcs(OptCriterion):
    sense = 'MAX'

    def chain_val(self, chain):
        return chain.n_backarcs()

    def cycle_val(self, cycle):
        return cycle.n_backarcs()

    def altruist_val(self, altruist):
        return 0

class MinThreeWay(OptCriterion):
    sense = 'MIN'

    def chain_val(self, chain):
        return chain.n_transplants() == 3

    def cycle_val(self, cycle):
        return cycle.n_transplants() == 3

    def altruist_val(self, altruist):
        return 0

class MaxInverseThreeWay(OptCriterion):
    # Maximise the number of unused NDDs plus twice the number of pairwise exchanges
    sense = 'MAX'

    def chain_val(self, chain):
        return (chain.n_transplants() == 2) * 2

    def cycle_val(self, cycle):
        return (cycle.n_transplants() == 2) * 2

    def altruist_val(self, altruist):
        return 1

class MaxWeight(OptCriterion):
    sense = 'MAX'

    def weight_fun(self, score, dage1, dage2):
        age_diff = abs(dage1 - dage2)
        small_age_diff_bonus = 3 if age_diff<=20 else 0
        max_age_minus_age_diff = 70 - age_diff
        tie_breaker = (max_age_minus_age_diff * 
                       max_age_minus_age_diff /
                       100000.0)
        age_diff_score = small_age_diff_bonus + tie_breaker
        return score + age_diff_score

    def chain_val(self, chain):
        return chain.weight(self.weight_fun)

    def cycle_val(self, cycle):
        return cycle.weight(self.weight_fun)

    def altruist_val(self, altruist):
        return 0

class MaxIntWeight(OptCriterion):
    sense = 'MAX'

    def weight_fun(self, score, dage1, dage2):
        age_diff = abs(dage1 - dage2)
        small_age_diff_bonus = 3 if age_diff<=20 else 0
        max_age_minus_age_diff = 70 - age_diff
        tie_breaker = (max_age_minus_age_diff * 
                       max_age_minus_age_diff /
                       100000.0)
        age_diff_score = small_age_diff_bonus + tie_breaker
        return int(round((score + age_diff_score)*100000)) / 100000

    def chain_val(self, chain):
        return chain.weight(self.weight_fun)

    def cycle_val(self, cycle):
        return cycle.weight(self.weight_fun)

    def altruist_val(self, altruist):
        return 0

class MaxNull(OptCriterion):
    sense = 'MAX'

    def chain_val(self, chain):
        return 0

    def cycle_val(self, cycle):
        return 0

    def altruist_val(self, altruist):
        return 0

