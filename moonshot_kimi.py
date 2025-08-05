import os
from langchain_community.chat_models.moonshot import MoonshotChat
from langchain.schema import HumanMessage, SystemMessage

class moonshot:
    def __init__(self, model="moonshot-v1-auto"):
        """
        初始化Moonshot Kimi模型
        
        Args:
            model (str): 要使用的Kimi模型名称
        """
        print(f"正在使用Moonshot模型: {model}")
        # 从环境变量获取API密钥，避免硬编码
        api_key = os.environ.get("MOONSHOT_API_KEY") or 'your_api'
        self.llm = MoonshotChat(
            model=model,
            max_tokens=1024,
            moonshot_api_key=api_key
        )

    def demo(self, system="你是一个很棒的智能助手", human="请给我写一句情人节红玫瑰的中文宣传语"):
        """
        使用MoonshotChat模型生成响应
        
        Args:
            system (str): 系统提示词
            human (str): 用户输入
        """
        messages = [
            SystemMessage(content=system),
            HumanMessage(content=human)
        ]
        try:
            response = self.llm.invoke(messages)
            print(f"模型响应: {response.content}")
            return response
        except Exception as e:
            print(f"调用Kimi API时出错: {e}")
            return None

    def invoke(self, messages, *args, **kwargs):
        """
        调用模型生成响应
        
        Args:
            messages: 消息列表
            *args: 其他位置参数
            **kwargs: 其他关键字参数
            
        Returns:
            模型的响应
        """
        return self.llm.invoke(messages, *args, **kwargs)

if __name__ == '__main__':
    a = moonshot()
    messages = [
        SystemMessage(content="你是一个很棒的智能助手"),
        HumanMessage(content="请给我写一句情人节红玫瑰的中文宣传语")
    ]
    response = a.invoke(messages).content
    print(response)
    a.demo()
