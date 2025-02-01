from config.settings import Settings
from llm.classifier import Classifier

def main(query: str):
    settings = Settings()

    llm = Classifier(
        company_name=settings.COMPANY_NAME,
        openai_api_url=settings.OPENAI_API_URL,
        openai_api_key=settings.OPENAI_API_KEY,
        openai_llm_model=settings.OPENAI_LLM_MODEL,
        openai_embed_model=settings.OPENAI_EMBED_MODEL,
        db_host=settings.DB_HOST,
        db_port=settings.DB_PORT,
        db_name=settings.DB_NAME,
        db_password=settings.DB_PASSWORD,
        db_user=settings.DB_USER,
    )

    response = llm.run(
        prompt=settings.SYSTEM_PROMPT,
        query=query
    )
    print(response)

if __name__ == '__main__':
    query = str(input("Masukan pertanyaan anda: "))
    main(query)