from bs4 import BeautifulSoup
from datetime import datetime, UTC
from dateutil.parser import isoparse
import json
import requests
import sys

url = 'https://www.towerbridge.org.uk/lift-times'
selector = '.view-bridge-opening-times tbody > tr > td:first-child > time'


r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')
now = datetime.now(UTC)
for t in soup.select(selector):
    dt = isoparse(t['datetime'])
    if dt > now:
        break
else:
    sys.exit(1)

data = {
    'next_lift': dt.isoformat()
}
print(json.dumps(data))

