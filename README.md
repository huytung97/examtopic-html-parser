# examtopic-html-parser
Parser for examtopics html files

## Prerequisites
### Create a new directory for input files
```bash
mkdir input
```
Then put all .html files into this folder
### Create python environment and install python libraries
```bash
python -m venv .venv

# activate the environment
source .venv/bin/activate # linux
.venv\Scripts\activate # windows

pip install -r requirements.txt
```

## How to run
### Parse HTML files
```bash
# parse html to jsonline
python parse_html.py

# generate question pdf
python generate_pdf.py

# generate answer pdf
python generate_answer.py
```