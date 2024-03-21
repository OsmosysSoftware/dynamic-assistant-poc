# dynamic-assistant-poc
This is a POC to demonstrate how to dynamic pick assistant to route queries to related assistant.


## Prerequisites

Make sure you have python(3.11.7) and pip(24.0) installed

To check, use these command

```bash
python --version
pip --version
```

If Python or pip is not installed, please visit [Python's official website](https://www.python.org/downloads/) for installation instructions.

## Setup

Update the .env file with the OpenAI_Server_Key. You can obtain this key from your OpenAI account dashboard

Run the following command to run the application

```bash

python3 -m venv assistant

# If you are using the fish shell use this to activate virtual environment
source assistant/bin/activate.fish

# If you are using the bash shell use this to activate virtual environment
source assistant/bin/activate

pip install --upgrade openai python-dotenv

python app.py
```