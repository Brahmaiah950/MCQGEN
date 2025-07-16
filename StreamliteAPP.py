import os
import json
import traceback
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import ast

from src.mcqgenerator.logger import logging
from src.mcqgenerator.utils import read_file, get_table_data
from langchain_community.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generats_evalution_chain

# ✅ Load environment variables
load_dotenv()

# ✅ Load response schema
with open(r'C:\Users\HP\OneDrive\Desktop\MCQGEN\Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

# ✅ Streamlit app title
st.title("📘 MCQ Creator App using LangChain")

with st.form("user_inputs"):
    uploaded_file = st.file_uploader("📎 Upload PDF or TXT", type=["pdf", "txt"])
    mcq_count = st.number_input("🎯 Number of MCQs", min_value=3, max_value=50)
    subject = st.text_input("📚 Subject", max_chars=20)
    tone = st.text_input("🧠 Complexity/Tone", max_chars=20, placeholder="Simple")
    button = st.form_submit_button("🚀 Generate MCQs")

    if button and uploaded_file and mcq_count and subject and tone:
        with st.spinner("Generating MCQs..."):
            try:
                # ✅ Read input file
                text = read_file(uploaded_file)

                # ✅ Call LangChain generation pipeline
                with get_openai_callback() as cb:
                    response = generats_evalution_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject": subject,
                            "tone": tone,
                            "response_json": json.dumps(RESPONSE_JSON)
                        }
                    )
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("❌ Error occurred during MCQ generation.")
            else:
                st.success("✅ MCQs generated!")
                st.markdown(f"**Total tokens:** {cb.total_tokens}")
                st.markdown(f"**Prompt tokens:** {cb.prompt_tokens}")
                st.markdown(f"**Completion tokens:** {cb.completion_tokens}")
                st.markdown(f"**Estimated cost:** ${cb.total_cost:.5f}")

                # ✅ Extract and parse quiz
                quiz = response.get('quiz')
                if isinstance(quiz, str):
                    try:
                        quiz = ast.literal_eval(quiz)
                    except Exception as e:
                        st.error("Could not parse the quiz string.")
                        st.write("Raw quiz string:", quiz)
                        quiz = None

                if quiz:
                    st.subheader(" Raw Quiz Output")
                    st.json(quiz)

                    table_data = get_table_data(json.dumps(quiz))
                    if table_data:
                        df = pd.DataFrame(table_data)
                        df.index += 1
                        st.subheader("📊 MCQ Table")
                        st.table(df)
                        st.text_area("📋 Review", value=response.get("review", ""))
                    else:
                        st.error("⚠️ Could not format MCQ table.")
                else:
                    st.warning("⚠️ No valid 'quiz' found in the response.")
