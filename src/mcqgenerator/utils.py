import os
import PyPDF2
import json
import traceback

def read_file(file):
    try:
        if file.name.endswith('.pdf'):
            text = ""
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
            return text

        elif file.name.endswith('.txt'):
            return file.read().decode('utf-8')

        else:
            raise Exception('Unsupported file format. Only PDF or TXT files are supported.')

    except Exception as e:
        traceback.print_exc()
        raise Exception(f" Error reading file: {str(e)}")

def get_table_data(quiz_str):
    try:
        quiz_dict = json.loads(quiz_str) 

        quiz_table_data = []
        for key, value in quiz_dict.items():
            mcq = value['mcq']
            options = " | ".join([f'{option}: {option_value}' for option, option_value in value['options'].items()])
            correct = value['correct option']
            quiz_table_data.append({'mcq': mcq, "choice": options, "correct": correct})

        return quiz_table_data

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False