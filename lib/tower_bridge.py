from bs4 import BeautifulSoup
from datetime import datetime, UTC
from dateutil.parser import parse
from dateutil.tz import gettz
from dateutil.utils import default_tzinfo
import json
import requests

url = 'https://www.towerbridge.org.uk/bridge-lifts'
selector = '''.time-table-container h3.time-table__heading,
              .time-table-container .bridge-lift-row__content > p:first-child > strong'''

tz = gettz("Europe/London")


def next_lift():
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    now = datetime.now(UTC)
    day = None
    for tag in soup.select(selector):
        if tag.name == 'h3':
            day = tag.text
        elif day is None:
            raise ValueError("No day heading found")
        else:
            dtstr = f"{day} {tag.text}"
            #print(dtstr)
            dt = default_tzinfo(parse(dtstr), tz)
            #print(dt)
            if dt > now:
                break
    else:
        return None

    data = {
        'next_lift': dt.isoformat()
    }
    return data

if __name__ == '__main__':
    print(json.dumps(next_lift()))

