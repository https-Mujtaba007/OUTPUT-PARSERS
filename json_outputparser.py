from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
# from langchain_classic.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    task="text generation"
)
model= ChatHuggingFace(llm=llm)

parser= JsonOutputParser()

template = PromptTemplate(
    template="give me name and city of most fictional person \n {format_instruction}",
    input_variables=[],
    partial_variables={'format_instruction':parser.get_format_instructions()}
)
prompt= template.format()
result= model.invoke(prompt)
final_result =parser.parse(result.content)
print(final_result)