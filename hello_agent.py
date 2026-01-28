from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
import asyncio

class HelloBehaviour(CyclicBehaviour):
    async def run(self):
        print("Hello, I am running...")
        await asyncio.sleep(5)

class HelloAgent(Agent):
    async def setup(self):
        print("Agent starting...")
        self.add_behaviour(HelloBehaviour())

async def main():
    # These are the credentials you "picked"
    agent = HelloAgent("agent1@localhost", "1234")
    await agent.start()
    await asyncio.sleep(20)
    await agent.stop()

asyncio.run(main())
