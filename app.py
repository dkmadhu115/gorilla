import openai
import streamlit as st
import subprocess
import sys

openai.api_key = "EMPTY"  # Key is ignored and does not matter
openai.api_base = "http://zanino.millennium.berkeley.edu:8000/v1"

# Query Gorilla Server
def get_gorilla_response(prompt, model):
    try:
        completion = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        print("Response: ", completion)
        return completion.choices[0].message.content 
    except Exception as e:
        print("Sorry, something went wrong!")

def extract_code_from_output(output):
    if output:
        code = output.split("code>>>:")[1]
        return code
    else:
        return ""

def run_generated_code(file_path):
    command = [sys.executable, file_path]

    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            st.success("Generated code executed successfully.")
            st.code(result.stdout, language="python")
        else:
            st.error("Generated code execution failed with the following error:")
            st.code(result.stderr, language="bash")
    except Exception as e:
        st.error(f"Error occurred while running the generated code: {str(e)}")

st.set_page_config(layout="wide")

def main():
    st.title("Gorilla LLM Demo App 🦍‍👤")

    input_prompt = st.text_area("Enter your prompt below:")

    option = st.selectbox('Select a model option from the list:', ('gorilla-7b-hf-v1', "gorilla-mpt-7b-hf-v0"))

    if st.button("Gorilla Search"):
        if len(input_prompt) > 0:
            col1, col2 = st.columns([1, 1])
            with col1:
                result = get_gorilla_response(prompt=input_prompt, model=option)
                st.write(result)

            with col2:
                if result:
                    code_result = extract_code_from_output(result)
                    st.subheader("Generated Output")
                    st.code(code_result, language='python')

                    file_path = f"generated_code_{option}.py"
                    with open(file_path, 'w') as file:
                        file.write(code_result)

                    run_generated_code(file_path)

if __name__ == "__main__":
    main()
