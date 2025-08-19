import os
from langchain_community.chat_models.moonshot import MoonshotChat
from langchain.schema import HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate

class moonshot:
    def __init__(self, model="moonshot-v1-auto", verbose=False, chinese=False, no_md=False, **kwargs):
        """
        初始化Moonshot Kimi模型
        
        Args:
            model (str): 要使用的Kimi模型名称
                - moonshot-v1-auto: 可以根据当前上下文占用的 Tokens 数量来选择合适的模型，
                  可供选择的模型包括：moonshot-v1-8k/moonshot-v1-32k/moonshot-v1-128k                
                  参考：https://platform.moonshot.cn/docs/guide/choose-an-appropriate-kimi-model#moonshot-v1-auto-模型
                - 使用 Kimi 视觉模型（Vision）：moonshot-v1-8k-vision-preview/moonshot-v1-32k-vision-preview/moonshot-v1-128k-vision-preview 等
                  参考：https://platform.moonshot.cn/docs/guide/use-kimi-vision-model
            verbose (bool): 是否显示详细信息
            chinese (bool): 是否使用中文模式（添加"让我们说中文"提示）
            no_md (bool): 是否禁用Markdown格式输出
            **kwargs: 其他传递给MoonshotChat的参数
        """
        self.verbose = verbose
        self.chinese = chinese
        self.no_md = no_md
        
        # 构建额外的系统提示
        self.extra_prompt = self._build_extra_prompt()
        
        # 准备传递给模型的参数
        model_kwargs = {
            "model": model,
            "max_tokens": 1024,
            "moonshot_api_key": os.environ.get("MOONSHOT_API_KEY") or 'your_api',
            "verbose": verbose,
            **kwargs
        }

        if self.verbose:
            print(f"正在使用Moonshot模型: {model}")

        # 如果有额外提示，添加到模型的默认提示中
        if self.extra_prompt:
            # 将额外提示作为默认提示传递给模型
            model_kwargs["default_prompt"] = SystemMessage(content=self.extra_prompt)
        
        # 初始化MoonshotChat实例
        self.llm = MoonshotChat(**model_kwargs)

    def demo(self, system="你是一个很棒的智能助手", human="请给我写一句情人节红玫瑰的中文宣传语"):
        """
        使用MoonshotChat模型生成响应
        
        Args:
            system (str): 系统提示词
            human (str): 用户输入
            
        Returns:
            模型的响应或None（如果发生错误）
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

    def _build_extra_prompt(self):
        """
        构建额外的系统提示
        注意，只对内部invoke有效
        
        Returns:
            str: 额外的系统提示内容
        """
        prompts = []
        
        if self.chinese:
            prompts.append("让我们说中文")
            if self.verbose:
                print("已启用中文模式")
                
        if self.no_md:
            prompts.append("请不要使用任何Markdown格式，如代码块（```）、粗体、斜体等。只返回纯文本。")
            if self.verbose:
                print("已启用无Markdown模式")
                
        if self.verbose:
            print(f"额外的系统提示: {prompts}")
                
        return "\n".join(prompts) if prompts else ""

    def invoke(self, messages, *args, **kwargs):
        """
        调用模型生成响应
        
        Args:
            messages: 消息列表
            *args: 其他位置参数
            **kwargs: 其他关键字参数
            
        Returns:
            模型的响应
            
        Raises:
            Exception: 调用模型时发生的异常
        """
        if self.verbose:
            messages_display = messages if isinstance(messages, list) else [messages]
            print(f"发送的消息: {messages_display}")
                
        try:
            return self.llm.invoke(messages, *args, **kwargs)
        except Exception as e:
            if self.verbose:
                print(f"调用模型时出错: {e}")
            raise

if __name__ == '__main__':
    # 创建实例，启用中文模式和详细输出
    a = moonshot(verbose=True)
    messages = [
        SystemMessage(content="你是一个很棒的智能助手"),
        HumanMessage(content="请给我写一句情人节红玫瑰的中文宣传语")
    ]
    response = a.invoke(messages).content
    print(response)
    a.demo()
