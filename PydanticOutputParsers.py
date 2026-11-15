from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
from langchain_classic.output_parsers import PydanticOutputParser
from pydantic import BaseModel,Field
from langchain_core.prompts import PromptTemplate

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    task="text generation"
)
model= ChatHuggingFace(llm=llm)

class Person(BaseModel):
  
    name:str = Field(description='name of the person'),
    age : int =Field(gt=18,description='age of the person')
    city : str = Field(description='city of the person where to belong')

parser =PydanticOutputParser(pydantic_object=Person)

template = PromptTemplate(
  template = 'give name,age ,city of famous {place}person \n {format_instruction}',
  input_variables=['place'],
  partial_variables={'format_instruction':parser.get_format_instructions()}
 )
prompt = template.invoke({'place':'pakistani'})
result = model.invoke(prompt)
final_result= parser.parse(result)
print(final_result)
