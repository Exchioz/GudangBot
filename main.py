from config.settings import Settings
from llm.classifier import Classifier

def main(query: str):
    settings = Settings()
    llm = Classifier(
        openai_api_url=settings.OPENAI_API_URL,
        openai_api_key=settings.OPENAI_API_KEY,
        openai_llm_model=settings.OPENAI_LLM_MODEL,
        openai_embed_model=settings.OPENAI_EMBED_MODEL,
        company_name=settings.COMPANY_NAME,
    )

    response = llm.run(
        prompt=settings.SYSTEM_PROMPT,
        query=query
    )
    print(response)

if __name__ == '__main__':
    query = str(input("Masukan pertanyaan anda: "))
    main(query)