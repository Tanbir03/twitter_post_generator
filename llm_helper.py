from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()
llm = ChatGroq(groq_api_key=os.getenv("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"), model_name="llama-3.2-90b-text-preview")


if __name__ == "__main__":
    response = llm.invoke("Two most important ingradient in samosa are ")
    print(response.content)





