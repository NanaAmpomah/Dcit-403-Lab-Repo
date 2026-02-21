from transitions import Machine

class RescueAgent:
    states = ['idle', 'alert', 'rescue']

    def __init__(self):
        self.machine = Machine(
            model=self,
            states=RescueAgent.states,
            initial='idle'
        )

        self.machine.add_transition(
            trigger='sensor_trigger',
            source='idle',
            dest='alert'
        )

        self.machine.add_transition(
            trigger='dispatch',
            source='alert',
            dest='rescue'
        )

        self.machine.add_transition(
            trigger='complete',
            source='rescue',
            dest='idle'
        )

if __name__ == "__main__":
    agent = RescueAgent()

    print("Initial State:", agent.state)

    agent.sensor_trigger()
    print("After sensor trigger:", agent.state)

    agent.dispatch()
    print("After dispatch:", agent.state)

    agent.complete()
    print("After completion:", agent.state)