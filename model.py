import os

from dotenv import load_dotenv
from langchain_community.chat_models import ChatZhipuAI

load_dotenv()

model = ChatZhipuAI(
    zhipuai_api_key=os.getenv("ZHIPUAI_API_KEY"),
    model="glm-4.7"
)
