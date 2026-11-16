from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
from langchain_classic.output_parsers import StructuredOutputParser,ResponseSchema
from langchain_core.prompts import PromptTemplate

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    task="text generation"
)
model= ChatHuggingFace(llm=llm)

schema = [
    ResponseSchema(name='fact_1',description='fact_1 abou the topic'),
    ResponseSchema(name='fact_2',description='fact_2 abou the topic'),
    ResponseSchema(name='fact_3',description='fact_3 abou the topic')
    
]

parser = StructuredOutputParser.from_response_schemas(schema)

template = PromptTemplate(
    template= 'give 3 facts about {topic} \n {format_instruction}',
    input_variables=['topic'],
    partial_variables={'format_instruction':parser.get_format_instructions()}
)

prompt = templite.invoke({'topic':'black hole'})
result = model.invoke(prompt)
final_result= parser.parse(result.content)
print(final_result)
