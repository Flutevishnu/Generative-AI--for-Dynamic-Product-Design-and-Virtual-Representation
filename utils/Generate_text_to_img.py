import api.websockets_api as websockets_api
import random
import json 
import websocket
import uuid
import base64
from PIL import Image

class ImageGen:

    def __init__(self) -> None:
        self.client_id = str(uuid.uuid4())
        self.server_address = "127.0.0.1:8188"
        self.loras = {"Shoe": "shoes_xl.safetensors", "Tshirt":"t-shirt_design-sdxl.safetensors"}
        self.control_net_img = {"fullHand-Tshirt": "Control_net_images\\full_hand.jpeg", "Oversized-Tshirt":"Control_net_images\oversized-tshirt-fron.jpg", "Tshirt":"Control_net_images\\tshirt-half-front.jpg", "shirt":"Control_net_images\shirt_front.jpg", "Shoe":"Control_net_images\sneakers.jpeg"}
        
        with open("workflows/text-to-design.json", "r", encoding="utf-8") as f:
                self.prompt_text = f.read()

    def base64(self, img_path):
        print("img path", img_path)
        with open(img_path, "rb") as f:
            base64_string = base64.b64encode(f.read()).decode('utf-8')
        return base64_string

    def Generate(self, Prompt: str, product: str, base64_image=''):
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
                prompt["240"]["inputs"]["switch_1"] = "On"
                prompt["240"]["inputs"]["lora_name_1"] = self.loras[product_name]
            if base64_image == '':
                prompt["265"]["inputs"]["image"] = self.base64(self.control_net_img[product])
        else:
            if base64_image != "":
                prompt["265"]["inputs"]["image"] = base64_image
            
        prompt["269"]["inputs"]["prompt"] += Prompt
        prompt["266"]["inputs"]["seed"] = seed
        ws = websocket.WebSocket()
        ws.connect("ws://{}/ws?clientId={}".format(self.server_address, self.client_id))
        images = websockets_api.get_images(ws,self.client_id, prompt)
        return images
    

        