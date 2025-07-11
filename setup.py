from setuptools import find_packages, setup

setup(
    name="mcqgenerator",
    version='0.01',
    author='Brahmaiah',
    author_email='brahmaiahyegiati95@gmail.com',
    install_requires=[
        "openai",
        "langchain",
        "streamlit",
        "python-dotenv",
        "PyPDF2"
    ],
    packages=find_packages()
)
