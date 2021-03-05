
class Player:
    def __init__(self, name):
        self.name = name
        self.bets = 1
        self.folded = False
        self.raised = False

    def __repr__(self):
        return self.name
        # return f"Name:{self.name} Bets: {self.bets} Folded: {self.folded}"

    def __eq__(self, other):
        return self.bets == other.bets

    def __gt__(self, other):
        return self.bets > other.bets

    def __add__(self, other):
        return self.bets + other.bets

    def __radd__(self, other):
        return self.bets + other

    def select_action(self, valid_actions, current_state):
        pass
