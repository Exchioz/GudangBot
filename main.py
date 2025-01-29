from agents.settings import Settings
from agents.react_agent import ReActAgent

def main():
    settings = Settings()
    agent = ReActAgent(
        openai_base_url=settings.OPENAI_BASE_URL,
        openai_llm_model=settings.OPENAI_LLM_MODEL,
        openai_api_key=settings.OPENAI_API_KEY
    )
    query = str(input("Masukan pertanyaan anda: "))
    output = agent.run(
        sys_prompt=settings.SYSTEM_PROMPT,
        query=query
    )
    return output


if __name__ == '__main__':
    main()