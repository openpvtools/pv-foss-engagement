"""
Scraper for ReadTheDocs traffic analytics.

It would be nice if analytics were exposed through their API, but that's not the case:
https://github.com/readthedocs/readthedocs.org/issues/8891

So we do this silly login/scraping business instead.
"""

import requests
import bs4
import pandas as pd
import os
import io
import datetime
import logging
import sys

project_names = [
    'bifacial-radiance',
    'bifacialvf',
    'openpvtools',
    'panel-segmentation',
    'pv-ice',
    'pvanalytics',
    'pvcaptest',
    'pvlib-python',
    'py-smarts',
    'rdtools',
    'solarfactors',
    'twoaxistracking',
]

logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s | %(levelname)s | %(message)s'
)

username = os.getenv('RTD_USERNAME')
password = os.getenv('RTD_PASSWORD')

if username is None:
    logging.error('RTD_USERNAME environment variable not set')
    sys.exit(1)

if password is None:
    logging.error('RTD_PASSWORD environment variable not set')
    sys.exit(1)

session = requests.Session()

# first, load the login page and get this mysterious csrf token
logging.debug('requesting login page')
response = session.get("https://app.readthedocs.org/accounts/login/")
response.raise_for_status()

soup = bs4.BeautifulSoup(response.content, features='html.parser')
token = soup.find(attrs={'name': 'csrfmiddlewaretoken'}).attrs['value']

# now send in our credentials
logging.debug('posting credentials')
data = {'csrfmiddlewaretoken': token, 'login': username, 'password': password, 'next': '/dashboard/'}
response = session.post("https://app.readthedocs.org/accounts/login/",
                        data=data,
                        headers={"referer": "https://app.readthedocs.org/accounts/login/?next=/dashboard/"})
response.raise_for_status()
logging.debug('login successful')

# finally, fetch the analytics data
today = datetime.date.today().strftime('%Y-%m-%d')
for project_name in project_names:
    logging.debug(f'fetching analytics for {project_name=}')
    url = f"https://readthedocs.org/dashboard/{project_name}/traffic-analytics/?download=true"
    response = session.get(url)
    df = pd.read_csv(io.StringIO(response.content.decode()))

    fn = f"data/{project_name}_{today}.csv"
    logging.debug(f'writing file: {fn=}')
    df.to_csv(fn)

