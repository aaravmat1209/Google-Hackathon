import streamlit as st
import os
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")  # Store API key securely
genai.configure(api_key=API_KEY)


model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])


def get_gemini_response(question, student_solution):
    prompt = f"""
    The student provided solution: {student_solution}.  
    Your task is to determine if the student's solution \
    is correct or not.
    To solve the problem do the following:
    - First, work out your own solution to the problem. 
    - Then compare your solution to the student's solution \
    and evaluate if the student's solution is correct or not. 
    Don't decide if the student's solution is correct until 
    you have done the problem yourself. 
    Use the following format: 
    Question:
    \n
    Student's solution:
    \n
    Actual solution:
    steps to work out the solution and your solution here
    \n
    Is the student's solution the same as actual solution just calculated:
    yes or no
    \n
    Student grade:
    correct or incorrect
"""
    question = question + "\n" + prompt
    response = chat.send_message(question, stream=True)
    return response


st.set_page_config(page_title="Automate Grading with Gemini")

st.header("Automate Grading with Gemini")

input = st.text_input("Ask a Question: ")
student_solution = st.text_input("Student Solution: ")
submit = st.button("Submit")

if submit and input:
    response = get_gemini_response(input, student_solution)
    st.subheader("The response is")
    correct = False
    for chunk in response:
        text = chunk.text
        st.write(text)
