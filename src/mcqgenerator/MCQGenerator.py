import os
import json
import tracemalloc
import pandas as pd
from src.mcqgenerator.logger import logging
from src.mcqgenerator.utils import read_file, get_table_data

from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain , SequentialChain
import PyPDF2

load_dotenv()

key=os.getenv("OPENAI_API_KEY")

if key:
    print("Key loaded successfully")
else:
    print("Key not found")


llm=ChatOpenAI(openai_api_key=key,model_name='gpt-3.5-turbo', temperature=0.5)


#Prompt tamplate
TEMPLATE='''
        Text:{text}
        you are an expert in MCQ maker.Given the above text,it is your job to create a quiz of {number}/
        Multiple choice question for {subject} in tone {tone}.
        Make sure the questions are not repeated and check all questions to be conforming the text as well.
        Make sure to formate your response like RESPONSE_JSON and use it as guide.
        Ensure to make {number} of MCQs
        ### RESPONSE_JSON
        {response_json}

'''

quiz_generation_prompt=PromptTemplate(
    input_variables=['text','number','subject','tone','response_json'],
    template=TEMPLATE
)

#chain1
quiz_chain=LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)

#Prompt tamplate2
TEMPLATE2='''
            you are an expert english grammarian and writer.
            givean a multiple choice quiz for {subject} students.
            you need to evaluate the complexity of the question and given a complete analysis of the quiz. only use at max  word complexity,
            Update the quiz questions which needs to be changeed and chance the tone such that it prefectly fits students ability.
            Quiz_MCQs
            {quiz}
            check from an expert english writer of the above quiz
            '''
quiz_evaluation_prompt=PromptTemplate(
    input_variables=['subject','quiz'],
    template=TEMPLATE2
)

#chain2
review_chain=LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key='review',verbose=True)

#Overall chain where we are connecting the chains using SequentialChain
generats_evalution_chain=SequentialChain(
    chains=[quiz_chain,review_chain],input_variables=['text','number','subject','tone','response_json'],
    output_variables=['quiz','review'],verbose=True
)

