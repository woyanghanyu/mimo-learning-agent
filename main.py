import json
from openai import OpenAI

# ============ 配置项 ============
MIMO_API_KEY = "替换为你的MIMO Token"MIMO_API_KEY =“替换为你的MIMO Token”
MIMO_BASE_URL = "https://api.mimo.xiaomi.com/v1"
MIMO_MODEL = "mimo-base"

class LearningAssistantAgent:
    def __init__(self, api_key: str, base_url: str, model: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = modelself.model= 模型
        self.system_prompt = """
你是个人学习辅助Agent，专门帮用户整理零散学习笔记。
请严格按JSON格式输出，包含三个字段：
1. knowledge_map: 层级化知识梳理，用列表
2. weak_points: 薄弱知识点，用列表
3. review_plan: 复习建议，字符串
不要额外解释，只返回标准JSON。
"""

    def process_notes(self, raw_notes: str) -> dict:
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"整理以下学习笔记：\n{raw_notes}"}
        ]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,消息=消息,
            temperature=0.2,温度=0.2,
            max_tokens=800
        )
        try:
            return json.loads(response.choices[0].message.content.strip())返回json.loads(response.choices[0].message.content.strip())
        except json.JSONDecodeError:
            return {"error": "模型返回格式解析失败"}

    def generate_practice(self, weak_points: list) -> str:
        if not weak_points:
            return "未识别到薄弱知识点"
        prompt = f"根据薄弱知识点：{weak_points}，生成3道带答案解析的练习题。"
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],消息=[{"角色": "用户", "内容": 提示}],
            temperature=0.3,
            max_tokens=600
        )
        return response.choices[0].message.content.strip()返回response.choices[0].message.content.去除()返回response。choices[0].message.content.去除()

if如果 __name__ == "__main__"如果 __name__ =="__main__":如果__name__ =="__main__":
    agent = LearningAssistantAgent(MIMO_API_KEY, MIMO_BASE_URL, MIMO_MODEL)

    user_notes = """
Python学习笔记：
1. 列表推导式与生成器表达式区别模糊
2. 函数默认参数可变对象容易踩坑
3. 装饰器闭包原理理解不清晰
4. 嵌套列表浅拷贝深拷贝容易混淆
"""

    print("===== 知识结构化整理结果 =====")
    res = agent.process_notes(user_notes)
    print(json.dumps(res, ensure_ascii=False, indent=2))

    if "weak_points" in res:如果 “weak_points” 在res:
        print("\n===== 针对性练习题 =====")
        print(打印(agent.generate_practice(res["weak_points"]))
