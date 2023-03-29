#Finite State Machine

class FSM:
    def __init__(self, cond_checker:callable, state_changer:callable, state_checker:callable):
        self.cond_checker = cond_checker
        self.state_changer = state_changer
        self.state_checker = state_checker
        self.cur_state = self.state_checker()
        self.prev_state = self.cur_state



