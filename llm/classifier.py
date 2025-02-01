from .schema import TextClassification
from .handler.item_handler import ItemHandler
from .handler.company_handler import CompanyHandler
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate

class Classifier:
    def __init__(
        self,
        openai_api_url: str,
        openai_api_key: str,
        openai_llm_model: str,
        openai_embed_model: str,
        company_name: str,
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
        
        if cls_response == "item":
            handler = ItemHandler(self.client_embed, response)
            handler_response = handler.handle()
        elif cls_response == "company":
            handler = CompanyHandler(self.client_embed, response)
            handler_response = handler.handle()
        elif cls_response == "default":
            handler_response = query
        else:
            raise ValueError(f"Invalid response: {response}")
        
        generate = self.__generate(handler_response)
        return generate
        
    
    def __generate(self, handler_response: str) -> str:
        messages = [
            ("system", "Bantu menjawab pertanyaan berikut dengan detail."),
            ("human", handler_response)
        ]
        return self.client.invoke(messages).content