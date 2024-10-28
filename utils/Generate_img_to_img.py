import api.websockets_api as websockets_api
import random
import json 
import websocket
import uuid


class ImageGen:

    def __init__(self) -> None:
        self.client_id = str(uuid.uuid4())
        self.server_address = "127.0.0.1:8188"
        self.loras = {"Shoe": "shoes_xl.safetensors", "Tshirt":"t-shirt_design-sdxl.safetensors"}
        
        with open("workflows/sketch_to_design.json", "r", encoding="utf-8") as f:
                self.prompt_text = f.read()

    def Generate(self, Prompt: str, product: str, base64_image):
        prompt = json.loads(self.prompt_text)
        seed = random.randint(99, 999999999999)

        if product != "Other":
            product_name = product.split('-') 
            if len(product_name) > 1:
                product_name = product_name[1]
            else:
                product_name = product_name[0]
            print(product_name)
            if product_name != "shirt":
                prompt["264"]["inputs"]["switch_1"] = "On"
                prompt["264"]["inputs"]["lora_name_1"] = self.loras[product_name]
            if base64_image != '':
                prompt["275"]["inputs"]["image"] = base64_image
    
        else:
            if base64_image != "":
                prompt["275"]["inputs"]["image"] = base64_image
        prompt["277"]["inputs"]["text_b"] += Prompt
        prompt["256"]["inputs"]["seed"] = seed

        ws = websocket.WebSocket()
        ws.connect("ws://{}/ws?clientId={}".format(self.server_address, self.client_id))
        images = websockets_api.get_images(ws,self.client_id, prompt)
        return images
    

        