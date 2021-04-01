
class Player:
    def __init__(self, name, init_amount=100):
        self.name = name
        self.amount = init_amount
        self.bets = 1
        self.folded = False
        self.raised = False

    def __repr__(self):
        # return self.name
        return f"Name:{self.name} Amount: {self.amount}"

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
