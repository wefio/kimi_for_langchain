# [在langchain中使用kimi](https://github.com/wefio/kimi_for_langchain/blob/main/moonshot_kimi.py)
## 起因
学习langchain，kimi里有50元，langchain貌似不能直接用kimi，示例又都是openai。于是尝试兼容。不保证维护，兼容到哪，得看以后还能不能用的到。<br>
由ai辅助完成<br>
## 导入kimi
简单的兼容了openai的调用方式<br>
如想要导入openai：<br>
```
import os
os.environ["OPENAI_API_KEY"] = 'your_OpenAI Key'
from langchain.chat_models import ChatOpenAI
chat = ChatOpenAI()
result = chat(prompt)
print(result.content)
```
现在可以：<br>
```
import os
from moonshot_kimi import moonshot
os.environ["MOONSHOT_API_KEY"] = "your_kimi_api" #如果在moonshot_kimi.py中填写好了可以删掉这一行
chat = moonshot()
result = chat.invoke(prompt)  #和原版略有不同
print(result.content)
```
## 导入kimi的llm
```
llm = moonshot().llm
```
## 使用指定模型
默认使用auto模型，但也可以指定<br>
例如使用视觉模型<br>
```
llm = moonshot(model="moonshot-v1-8k-vision-preview").llm
```
## 好像没什么用的额外功能
```
moonshot(verbose=True, chinese=True, no_md=True)
```
- 啰嗦模式、强制中文模式、无markdown模式<br>
注意，中文模式和无markdown模式都是用系统提示词实现的
## 需要注意的问题
如果需要真正的纯文本，如sql查询，需要使用langchain的PromptTemplate，不能用无markdown模式替代。如果sql成功了纯属意外，不使用无markdown模式也有可能成功。
