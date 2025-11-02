import json
import os
from typing import List

from bs4 import BeautifulSoup

html_path = 'input'
html_files: List[str] = os.listdir(html_path)

output_file = 'output.jsonl'

if os.path.exists(output_file):
    os.remove(output_file)

is_new_file = True

for fname in sorted(html_files):
    current_file_path: str = os.path.join(html_path, fname)
    
    with open(current_file_path, encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        question_containers = soup.select('.exam-question-card')

        questions = list()
        for question in question_containers:
            q = {"text": [], "img": []}
            
            q_body = question.select_one('.question-body')
            q_header = question.select_one('.card-header')

            q['question_no'] = q_header.text.strip().split('\n')[0]

            # select question
            p = q_body.select_one('p.card-text')
            for element in p.contents:
                if element.name == "br":
                    continue
                elif element.name == "img":
                    q["img"].append(element.get("src"))
                elif isinstance(element, str):
                    text = element.strip()
                    if text:
                        q["text"].append(text)

            # select choices
            choices = []
            correct_choices = []
            question_choices = q_body.select('.multi-choice-item')

            for choice in question_choices:
                if 'class' in choice.attrs and 'correct-hidden' in choice['class']:
                    correct_choices.append(choice.select_one('span')['data-choice-letter'])
                for unwanted in choice.select(".badge, .most-voted-answer-badge"):
                    unwanted.decompose()
                choices.append(choice.get_text(separator=" ", strip=True))

            q['choices'] = choices
            q['correct_choices'] = correct_choices
            questions.append(q)

        if is_new_file:
            mode = 'w'
            is_new_file = False
        else:
            mode = 'a'

        with open(output_file, mode, encoding="utf-8") as f:
            for q in questions:
                json.dump(q, f, ensure_ascii=False)
                f.write("\n")
