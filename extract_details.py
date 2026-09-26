import urllib.request
import ssl
import json
import re
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'header', 'footer', 'nav'):
            self.skip = True

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'header', 'footer', 'nav'):
            self.skip = False

    def handle_data(self, data):
        if not self.skip:
            self.text.append(data)

    def get_text(self):
        return '\n'.join(self.text)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

candidates = [
    ('vibra-energia_analista-de-planejamento-supply-chain-pl', 'https://vibraenergia.gupy.io/job/eyJqb2JJZCI6MTI0ODkzNjUsInNvdXJjZSI6Imd1cHlfcG9ydGFsIn0=?jobBoardSource=gupy_portal'),
    ('lojas-renner-s-a_especialista-de-logistica-supply-chain-analytics', 'https://renner.gupy.io/job/eyJqb2JJZCI6MTI1MzIzNDIsInNvdXJjZSI6Imd1cHlfcG9ydGFsIn0=?jobBoardSource=gupy_portal'),
    ('gpa_especialista-supply-chain', 'https://gpa.gupy.io/job/eyJqb2JJZCI6MTI1MzA3ODcsInNvdXJjZSI6Imd1cHlfcG9ydGFsIn0=?jobBoardSource=gupy_portal'),
    ('azzas-2154-shoes-bags_analista-supply-chain-senior-sourcing', 'https://azzasshoesbags.gupy.io/job/eyJqb2JJZCI6MTI1OTU4MTMsInNvdXJjZSI6Imd1cHlfcG9ydGFsIn0=?jobBoardSource=gupy_portal'),
    ('ultragaz-biometano_especialista-de-supply-chain', 'https://ultragazbiometano.gupy.io/job/eyJqb2JJZCI6MTI0OTg2MjYsInNvdXJjZSI6Imd1cHlfcG9ydGFsIn0=?jobBoardSource=gupy_portal'),
    ('hirelatam_remote-operations-supply-chain-coordinator-food-cpg', 'https://recruiterflow.com/hirelatam/jobs/1727'),
    ('passport_logistics-analyst', 'https://dynamitejobs.com/company/passport/remote-job/logistics-analyst'),
    ('ting_supply-chain-manager', 'https://dynamitejobs.com/company/ting/remote-job/supply-chain-manager'),
    ('gruns_director-of-supply-chain', 'https://dynamitejobs.com/company/gruns/remote-job/director-of-supply-chain'),
    ('blueland_supply-chain-manager', 'https://jobs.lever.co/blueland/48b87f79-33d9-4ad7-aaee-3b2d2c63e970?utm_source=freehire.me')
]

for key, url in candidates:
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            json_lds = re.findall(r'<script[^>]*type=[\'"]application/ld\+json[\'"][^>]*>(.*?)</script>', html, re.DOTALL)
            loc_info = []
            for j in json_lds:
                try:
                    data = json.loads(j)
                    if isinstance(data, dict):
                        job_loc = data.get('jobLocation') or data.get('applicantLocationRequirements')
                        loc_type = data.get('jobLocationType')
                        loc_info.append(f'loc_type: {loc_type}, jobLocation: {job_loc}')
                except:
                    pass

            parser = TextExtractor()
            parser.feed(html)
            text = parser.get_text()
            lines = [l.strip() for l in text.splitlines() if l.strip()]
            full_text = '\n'.join(lines)
            with open(f'full_{key}.txt', 'w', encoding='utf-8') as out:
                out.write(f'URL: {url}\n\nJSON-LD LOC: ' + '; '.join(loc_info) + '\n\n' + full_text)
            print(f'Wrote full_{key}.txt ({len(full_text)} chars). Loc info: {loc_info}')
    except Exception as e:
        print(f'Error {key}: {e}')
