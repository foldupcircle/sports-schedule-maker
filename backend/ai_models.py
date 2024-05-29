from langchain_openai import ChatOpenAI

GPT3 = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
)

GPT4 = ChatOpenAI(
        model="gpt-4-1106-preview",
        temperature=0,
)