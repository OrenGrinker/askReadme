import requests
import anthropic


def fetch_readme_content(github_link):
    """Fetch the README content from the GitHub repository."""
    api_url = github_link.replace("github.com", "api.github.com/repos") + "/readme"
    headers = {'Accept': 'application/vnd.github.v3.raw'}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        return None


def analyze_readme_content(readme_content, api_key, temperature, max_tokens, chat_history):
    """Analyze the README content using Anthropic's Claude model."""
    client = anthropic.Anthropic(api_key=api_key)
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"I need help understanding the content of a README file from a GitHub project. The README file contains information about the project's purpose, installation instructions, usage guidelines, and contribution guidelines.\n\nHere is the content of the README file:\n\n{readme_content}"
                }
            ]
        }
    ]
    messages.extend(chat_history)  # Include previous chat history
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=max_tokens,
        temperature=temperature,
        messages=messages
    )
    return message.content
