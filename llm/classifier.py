from .schema import TextClassification
from .handler.item_handler import ItemHandler
from .handler.company_handler import CompanyHandler
from config.db_config import DBConfig
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate

class Classifier:
    def __init__(
        self,
        company_name: str,
        openai_api_url: str,
        openai_api_key: str,
        openai_llm_model: str,
        openai_embed_model: str,
        db_host: str,
        db_port: int,
        db_user: str,
        db_password: str,
        db_name: str,
    ):
        self.company_name = company_name
        self.client = ChatOpenAI(
            base_url=openai_api_url,
            api_key=openai_api_key,
            model=openai_llm_model,
        )
        self.client_embed = OpenAIEmbeddings(
            base_url=openai_api_url,
            api_key=openai_api_key,
            model=openai_embed_model,
        )
        self.db = DBConfig(
            db_host=db_host,
            db_port=db_port,
            db_user=db_user,
            db_password=db_password,
            db_name=db_name,
        )
    
    def run(self, prompt: str, query: str) -> str:
        cls_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", prompt),
                ("human", "{input}")
            ]
        )
        chain = cls_prompt | self.client.with_structured_output(TextClassification)
        response = chain.invoke({"input": query, "company_name": self.company_name})
        
        cls_response = response.classification
        print(response)
        
        if cls_response == "item":
            handler = ItemHandler(self.client_embed, self.db)
            handler_response = handler.handle(query)
        elif cls_response == "company":
            handler = CompanyHandler(self.client_embed)
            handler_response = handler.handle(query)
        elif cls_response == "default":
            handler_response = query
        else:
            raise ValueError(f"Invalid response: {response}")
        
        generate = self.__generate(handler_response)
        return generate
        
    def __generate(self, handler_response: str) -> str:
        messages = [
            ("system", 
                "Anda adalah asisten AI untuk PT.XYZ, sebuah perusahaan jual beli barang. "
                "Tugas Anda adalah memberikan jawaban yang ramah dan informatif kepada pelanggan "
                "berdasarkan pertanyaan yang diajukan."),
            ("human", 
                f"Informasi: {handler_response}")
        ]
        return self.client.invoke(messages).content