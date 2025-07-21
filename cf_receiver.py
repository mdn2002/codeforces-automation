import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from flask import Flask, request
from flask_cors import CORS
from src.problem_creator import ProblemCreator
from src.utils.config_parser import ConfigParser
from src.html_parser import CodeforcesHTMLParser
import re

app = Flask(__name__)
CORS(app)

@app.route('/receive', methods=['POST'])
def receive():
    data = request.get_json()
    html = data.get('html', '')
    url = data.get('url', '')
    # Save the HTML for debugging and further processing
    with open('last_problem.html', 'w', encoding='utf-8') as f:
        f.write(html)
    # Parse the HTML
    parsed = CodeforcesHTMLParser.parse_problem(html)
    # Extract problem_id from URL (support gym, contest, and problemset)
    match = re.search(r'/problemset/problem/(\d+)/([A-Z])|/contest/(\d+)/problem/([A-Z])|/gym/(\d+)/problem/([A-Z])', url)
    if match:
        if match.group(1) and match.group(2):
            problem_id = f"{match.group(1)}{match.group(2)}"
        elif match.group(3) and match.group(4):
            problem_id = f"{match.group(3)}{match.group(4)}"
        elif match.group(5) and match.group(6):
            problem_id = f"{match.group(5)}{match.group(6)}"
        else:
            problem_id = parsed['problem_name'].replace(' ', '_')
    else:
        problem_id = parsed['problem_name'].replace(' ', '_')
    parsed['problem_id'] = problem_id
    parsed['url'] = url
    # Create the problem files
    config = ConfigParser()
    creator = ProblemCreator(config)
    creator.create_problem(problem_id, parsed)
    return 'OK'

if __name__ == '__main__':
    app.run(port=8765) 