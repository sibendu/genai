import vertexai
from vertexai.generative_models import (
    FunctionDeclaration,
    GenerationConfig,
    GenerativeModel,
    Tool,
    HarmCategory,
    HarmBlockThreshold
)

import os
import shutil
from pathlib import Path
import requests
import git
import magika

repo_dir = "./repo/"

PROJECT_ID = os.environ.get("GOOGLE_PROJECT_ID") ## "rp-gcp-sma-itdisbx-01-np"  # @param {type:"string"}
LOCATION = os.environ.get("GOOGLE_LOCATION")  # "us-central1"  # @param {type:"string"}

vertexai.init(project=PROJECT_ID, location=LOCATION)

m = magika.Magika()

def clone_repo(repo_url, repo_dir):
    """Clone a GitHub repository."""

    if os.path.exists(repo_dir):
        shutil.rmtree(repo_dir)
    os.makedirs(repo_dir)
    git.Repo.clone_from(repo_url, repo_dir)


def extract_code(repo_dir):
    """Create an index, extract content of code/text files."""

    code_index = []
    code_text = ""
    for root, _, files in os.walk(repo_dir):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, repo_dir)
            code_index.append(relative_path)

            file_type = m.identify_path(Path(file_path))
            if file_type.output.group in ("text", "code"):
                try:
                    with open(file_path, "r") as f:
                        code_text += f"----- File: {relative_path} -----\n"
                        code_text += f.read()
                        code_text += "\n-------------------------\n"
                except Exception:
                    pass

    return code_index, code_text


def get_github_issue(owner: str, repo: str, issue_number: str) -> str:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }  # Set headers for GitHub API

    # Construct API URL
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"

    try:
        response_git = requests.get(url, headers=headers)
        response_git.raise_for_status()  # Check for HTTP errors
    except requests.exceptions.RequestException as error:
        print(f"Error fetching issue: {error}")  # Handle potential errors

    issue_data = response_git.json()
    if issue_data:
        return issue_data["body"]
    return ""

def get_code_prompt(question, code_index, code_text):
    """Generates a prompt to a code related question."""

    prompt = f"""
    Questions: {question}

    Context:
    - The entire codebase is provided below.
    - Here is an index of all of the files in the codebase:
      \n\n{code_index}\n\n.
    - Then each of the files is concatenated together. You will find all of the code you need:
      \n\n{code_text}\n\n

    Answer:
  """

    return prompt

def download_codebase(codebase):
    print('downloading codebase')
    if os.path.exists(repo_dir):
        shutil.rmtree(repo_dir)
    os.makedirs(repo_dir)
    git.Repo.clone_from(codebase, repo_dir)
    print('codebase downloaded')
    code_index, code_text = extract_code(repo_dir)
    print('code_index created')
    return code_index, code_text

def analyze(question, code_index, code_text):
    print(question)
    print(code_index[:50])
    print(code_text[:50])

    MODEL_ID = "gemini-1.5-pro-001"  # @param {type:"string"}

    model = GenerativeModel(
        MODEL_ID,
        system_instruction=[
            "You are a coding expert.",
            "Your mission is to answer all code related questions with given context and instructions.",
        ],
    )
    print(model)

    prompt = get_code_prompt(question, code_index, code_text)
    contents = [prompt]
    print('prompt generated')

    safety_settings = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    }

    # Generate text using non-streaming method
    responses = model.generate_content(contents, stream=True, safety_settings=safety_settings)

    output = "Answer:\n"
    for response in responses:
        output = output + "\n"+ response.text

    # Print generated text and usage metadata
    #print(output)
    print(f'\nUsage metadata:\n{response.to_dict().get("usage_metadata")}')
    print(f"\nFinish reason:\n{response.candidates[0].finish_reason}")
    print(f"\nSafety settings:\n{response.candidates[0].safety_ratings}")

    return output