# AI-powered-PDF-Assistant-Use-Case

This is a minimal implementation of the RAG model for question answering.

## Requirements

- Python 3.9 or later

#### Install Python using anaConda

1) Download and install MiniConda from [here](https://docs.anaconda.com/anaconda/install/windows/)
2) Create a new environment using the following command:
```bash
$ conda create -n ai-assistant python=3.9
```
3) Activate the environment:
```bash
$ conda activate ai-assistant
```

### (Optional) Setup you command line interface for better readability

```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

## Installation

### Install the required packages

```bash
$ pip install -r requirements.txt
```

### Setup the environment variables

```bash
$ cp .env.example .env
```
Set your environment variables in the `.env` file. Like `Gimni_API_KEY` value.

### Run Streamlit Server

```bash
$ streamlit run src/app.py 
```
#### some versions of streamlit have error when upload file so you can use this commend
```bash
$ streamlit run src/app.py --server.enableXsrfProtection false
```


