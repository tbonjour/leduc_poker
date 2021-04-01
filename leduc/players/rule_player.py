from leduc.players.player import Player
import numpy as np
from leduc.hand_eval import leduc_eval


class RulePlayer(Player):

    def select_action(self, valid_actions, current_state):
        is_pair = False
        raise_next = False
        # print('RANK', current_state['hole_card'].rank)
        # print(current_state['hole_card'], current_state['board_card'])
        if current_state['board_card']:
            if current_state['hole_card'] == current_state['board_card']:
                is_pair = True
        if current_state['hole_card'].rank > 12 or is_pair:
            raise_next = True
        if raise_next:
            if '2R' in valid_actions:
                return '2R'
            elif '4R' in valid_actions:
                return '4R'
            else:
                return np.random.choice(valid_actions)
        elif 'C' in valid_actions:
            return 'C'
        else:
            return np.random.choice(valid_actions)