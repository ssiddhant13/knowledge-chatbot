from langchain.llms import OpenAI

llm = OpenAI(openai_api_key="api-key", temperature=0.9)

result = llm._generate(prompts = ["What would be a good company name for a company that makes colorful socks?"])
print(result)