class ItemHandler:
    def __init__(self, client_embed, response):
        self.client_embed = client_embed
        self.response = response
    
    def handle(self):
        return f"{self.response} Tersedia"