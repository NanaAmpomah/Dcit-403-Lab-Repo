import asyncio
from spade import agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from datetime import datetime


# ----------------------------
# Responder Agent
# ----------------------------
class ResponderAgent(agent.Agent):

    class ReceiveRequest(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=5)
            if msg:
                print("\n[Responder] Message received")
                print("Performative:", msg.get_metadata("performative"))
                print("Content:", msg.body)

                if msg.get_metadata("performative") == "request":

                    # Trigger action
                    current_time = datetime.now().strftime("%H:%M:%S")

                    reply = msg.make_reply()
                    reply.set_metadata("performative", "inform")
                    reply.body = f"Current time is {current_time}"

                    await self.send(reply)
                    print("[Responder] INFORM sent")
            else:
                pass

    async def setup(self):
        print("Responder started")
        self.add_behaviour(self.ReceiveRequest())


# ----------------------------
# Requester Agent
# ----------------------------
class RequesterAgent(agent.Agent):

    class SendRequest(OneShotBehaviour):
        async def run(self):
            msg = Message(to="responder@localhost")
            msg.set_metadata("performative", "request")
            msg.body = "Send me the time"

            await self.send(msg)
            print("[Requester] REQUEST sent")

    class ReceiveInform(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=5)
            if msg:
                print("\n[Requester] Message received")
                print("Performative:", msg.get_metadata("performative"))
                print("Content:", msg.body)

    async def setup(self):
        print("Requester started")
        self.add_behaviour(self.SendRequest())
        self.add_behaviour(self.ReceiveInform())


async def main():
    responder = ResponderAgent("responder@localhost", "password")
    requester = RequesterAgent("requester@localhost", "password")

    await responder.start(auto_register=True)
    await requester.start(auto_register=True)

    await asyncio.sleep(10)

    await requester.stop()
    await responder.stop()


if __name__ == "__main__":
    asyncio.run(main())
