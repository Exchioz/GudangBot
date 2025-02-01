from config.db_config import DBConfig

from sklearn.metrics.pairwise import cosine_similarity
from langchain_openai import OpenAIEmbeddings
import numpy as np

class ItemHandler:
    def __init__(self, client_embed: OpenAIEmbeddings, db: DBConfig):
        self.client_embed = client_embed
        self.db = db

    def handle(self, name_item: str) -> str:
        try:
            self.db.connect()
            all_items = self.__get_all_items()
            if not all_items:
                return "Tidak ada item dalam database."

            item_embeddings = np.array(self.client_embed.embed_documents(all_items))
            query_embedding = np.array(self.client_embed.embed_query(name_item)).reshape(1, -1)

            similarities = cosine_similarity(query_embedding, item_embeddings)
            best_match_index = similarities.argmax()
            best_match_score = similarities[0][best_match_index]

            print("Nama item: ", name_item)
            print("Best match score:", best_match_score)
            if best_match_score > 0.6:
                item_name = all_items[best_match_index]
                item = self.__get_item_by_name(item_name)
                return f"Item ditemukan:\n- Nama: {item[0]}\n- Harga: Rp.{item[1]}\n- Stok: {item[2]} unit"
            else:
                return f"Item '{name_item}' tidak ada di toko kami."
        finally:
            self.db.disconnect()
    
    def __get_all_items(self):
        query = "SELECT name FROM items"
        result = self.db.execute_query(query)

        return [item[0] for item in result] if result else []

    def __get_item_by_name(self, name: str):
        query = "SELECT name, price, stock FROM items WHERE name = %s"
        result = self.db.execute_query(query, (name,))

        return result[0] if result else None