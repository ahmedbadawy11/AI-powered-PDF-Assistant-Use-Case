# AI-powered-PDF-Assistant-Use-Case

This is a minimal implementation of the RAG model for question answering.

## Requirements

- Python 3.9 or later

#### Install Python using Anaconda

1) Download and install Anaconda from [here](https://docs.anaconda.com/anaconda/install/windows/)
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
### Install Tesseract
1) Install Poppler from [here](https://github.com/oschwartz10612/poppler-windows)
2) Copy Poppler and paste it this directory `src/controls`
3) Download and install Tesseract from [here](https://github.com/UB-Mannheim/tesseract/wiki)
4) Add Tesseract to your system PATH
5) Open the Control Panel and go to `System and Security` > `System` > `Advanced system settings` then Click on the `Environment Variables` button.
6) In the `System variables` section, find the `Path` variable and click `Edit`. Add the path to the Tesseract installation directory (e.g., `C:\Program Files\Tesseract-OCR`) and click OK.


2) Create a new environment using the following command:
### Setup the environment variables

```bash
$ cp .env.example .env
```
Set your environment variables in the `.env` file. Like `Gimni_API_KEY` value.

### Run Streamlit Server

```bash
$ streamlit run src/app.py 
```
#### some versions of streamlit have error when upload file so you can use this command
```bash
$ streamlit run src/app.py --server.enableXsrfProtection false
```


