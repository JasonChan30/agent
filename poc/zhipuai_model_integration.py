import os

from dotenv import load_dotenv
from langchain_community.chat_models import ChatZhipuAI
from langchain_core.messages import HumanMessage

load_dotenv()

model = ChatZhipuAI(
    zhipuai_api_key=os.getenv("ZHIPUAI_API_KEY"),
    model="glm-4.7"
)

messages = [HumanMessage(content="hello, 1+1等于几")]

res = model.invoke(messages)
print(res)