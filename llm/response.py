from config.db_config import DBConfig
from .schema import TextClassification
from .handler.item_handler import ItemHandler
from .handler.company_handler import CompanyHandler
from .handler.default_handler import DefaultHandler
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate

class ResponseHandler:
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
    
    def run(
        self,
        sys_cls_prompt: str = "You are a helpful assistant",
        sys_gen_prompt: str = "You are a helpful assistant",
        query: str = None,
        document_path: str = "data/resource.txt",
        vector_store_path: str = "data/faiss_index",
    ) -> str:
        if not query:
            raise ValueError("Query cannot be Empty")

        response = self.__classify(query, sys_cls_prompt)
        cls_response = response.classification
        print(response)

        if cls_response == "item":
            handler = ItemHandler(self.client_embed, self.db)
            handler_response = handler.handle(query)
            return self.__generate(
                sys_gen_prompt = sys_gen_prompt,
                information = handler_response,
                input = query, 
            ).content
        
        elif cls_response == "company":
            handler = CompanyHandler(self.client_embed, vector_store_path, document_path)
            handler_response = handler.handle(query)
            return self.__generate(
                sys_gen_prompt = sys_gen_prompt,
                information = handler_response,
                input = query, 
            ).content
        
        elif cls_response == "default":
            handler = DefaultHandler()
            return self.__generate(
                sys_gen_prompt = handler.get_sys_prompt(),
                information = handler.get_info(),
                input = query, 
            ).content

        else:
            raise ValueError(f"Invalid response: {response}")
    
    def __classify(self, query: str, sys_cls_prompt: str) -> str:
        cls_prompt = ChatPromptTemplate.from_messages([
            ("system", sys_cls_prompt),
            ("human", "{input}")
        ])
        chain = cls_prompt | self.client.with_structured_output(TextClassification)
        return chain.invoke({
            "input": query,
            "company_name": self.company_name
        })
        
    def __generate(self, information: str, input: str, sys_gen_prompt: str) -> str:
        gen_prompt = ChatPromptTemplate.from_messages([
            ("system", sys_gen_prompt),
            ("human", "Informasi: {information} \n\nPertanyaan: {input}"),
        ])
        chain = gen_prompt | self.client
        return chain.invoke({
            "company_name": self.company_name,
            "information": information,
            "input": input,
        })