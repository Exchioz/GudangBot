from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from .tools import AgentTools

class ReActAgent:
    def __init__(
        self,
        openai_base_url: str = "https://api.openai.com/v1/",
        openai_api_key: str = "",
        openai_llm_model: str = "gpt-3.5-turbo",
        ):
        self.client = ChatOpenAI(
            base_url=openai_base_url,
            model=openai_llm_model,
            api_key=openai_api_key
        )
        
    def run(self, sys_prompt: str, query: str) -> str:
        tools = AgentTools()
        tools_list = tools.get_tools()

        graph = create_react_agent(self.client, tools=tools_list)
        inputs = {"messages": [
            ("system", sys_prompt),
            ("user", query)
            ]}
        ai_response =  self.__print_stream(graph.stream(inputs, stream_mode="values"))
        
        return ai_response

    @staticmethod
    def __print_stream(stream):
        for message in stream:
            print(message)
            ai_messages = [msg for msg in message['messages'] if 'AIMessage' in str(type(msg))]
            for msg in ai_messages:
                if msg.content:
                    print(msg.content)