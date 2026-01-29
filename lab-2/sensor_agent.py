import random
import asyncio
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour


class SensorBehaviour(PeriodicBehaviour):
    async def run(self):
        damage = random.randint(0, 100)

        if damage < 30:
            level = "LOW"
        elif damage < 70:
            level = "MODERATE"
        else:
            level = "SEVERE"

        print(f"[EVENT] Damage Level: {damage} → {level}")


class SensorAgent(Agent):
    async def setup(self):
        print("SensorAgent started...")
        behaviour = SensorBehaviour(period=5)
        self.add_behaviour(behaviour)


async def main():
    agent = SensorAgent(
        "sensor@localhost",
        "sensorpass"
    )

    await agent.start()
    print("Agent is running...")

    # Keep agent alive for logging
    await asyncio.sleep(30)

    await agent.stop()
    print("Agent stopped.")


if __name__ == "__main__":
    asyncio.run(main())
