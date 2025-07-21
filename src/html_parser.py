from bs4 import BeautifulSoup
from typing import Dict, Any
from datetime import datetime
import re

class CodeforcesHTMLParser:
    @staticmethod
    def parse_problem(html: str) -> Dict[str, Any]:
        soup = BeautifulSoup(html, 'lxml')
        data = {}
        # Problem name
        title = soup.find('div', class_='title')
        data['problem_name'] = title.get_text(strip=True) if title else 'Unknown Problem'
        # Time limit
        time_limit = soup.find('div', class_='time-limit')
        if time_limit:
            text = time_limit.get_text(" ", strip=True)
            match = re.search(r'(\d+\.?\d*)\s*(second|seconds)', text)
            data['time_limit'] = f"{match.group(1)} {match.group(2)}" if match else 'Unknown'
        else:
            data['time_limit'] = 'Unknown'
        # Memory limit
        memory_limit = soup.find('div', class_='memory-limit')
        if memory_limit:
            text = memory_limit.get_text(" ", strip=True)
            match = re.search(r'(\d+)\s*(megabyte|megabytes)', text)
            data['memory_limit'] = f"{match.group(1)} {match.group(2)}" if match else 'Unknown'
        else:
            data['memory_limit'] = 'Unknown'
        # Test cases
        inputs = soup.find_all('div', class_='input')
        outputs = soup.find_all('div', class_='output')
        test_cases = []
        for inp, out in zip(inputs, outputs):
            in_pre = inp.find('pre')
            out_pre = out.find('pre')
            test_cases.append({
                'input': in_pre.get_text('\n', strip=True) if in_pre else '',
                'output': out_pre.get_text('\n', strip=True) if out_pre else ''
            })
        data['test_cases'] = test_cases
        # Created date with hour, minute, and second
        data['created_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return data 