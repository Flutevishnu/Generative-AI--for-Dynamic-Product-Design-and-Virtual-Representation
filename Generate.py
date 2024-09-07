import websockets_api
import random
import json 
import websocket
import uuid



class ImageGen:

    def __init__(self) -> None:
        self.client_id = str(uuid.uuid4())
        self.server_address = "127.0.0.1:8188"
        with open("shoe_workflow_api.json", "r", encoding="utf-8") as f:
                self.prompt_text = f.read()

    def Genarate(self, Prompt: str):
         
        prompt = json.loads(self.prompt_text)
        seed = random.randint(99, 999999999999)
        print(Prompt)
        print(prompt["5"]["inputs"]["text"])
        prompt["5"]["inputs"]["text"] += Prompt
        print(prompt["5"]["inputs"]["text"])
        prompt["1"]["inputs"]["seed"] = seed
        prompt["18"]["inputs"]["seed"] = seed


        ws = websocket.WebSocket()
        ws.connect("ws://{}/ws?clientId={}".format(self.server_address, self.client_id))
        images = websockets_api.get_images(ws,self.client_id, prompt)

        return images

        