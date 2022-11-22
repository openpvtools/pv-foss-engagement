
import pandas as pd
import pathlib
import requests
import re
import os
import numpy as np
import datetime

from bokeh.plotting import figure
from bokeh.models import HoverTool

datadir = pathlib.Path(__file__).parent.parent.parent.parent / 'data'


def get_rtd_analytics_data(project):
    filenames = sorted(datadir.glob(project + "*"))
    dfs = [pd.read_csv(fn, parse_dates=True) for fn in filenames]
    df = pd.concat(dfs)
    df['Date'] = pd.to_datetime(df['Date'])
    # the last day in a file can be incomplete, so in the overlap range we
    # prefer newer records (indicated by occurring later in `filenames`)
    df = df.drop_duplicates(['Date', 'Version', 'Path'], keep='last')
    df = df.drop(columns=['Unnamed: 0'])
    df = df.sort_values(['Version', 'Date', 'Path'])
    # prefix X.Y.Z with "v"
    is_bare_version = df['Version'].str.contains('.', regex=False) & ~df['Version'].str.startswith('v')
    df.loc[is_bare_version, 'Version'] = 'v' + df.loc[is_bare_version, 'Version']
    # remove PR builds and such
    keep = (
        df['Version'].str.startswith('v') |
        df['Version'].isin(['stable', 'latest']) |
        (df['Version'] == '0.1')
    )
    df = df.loc[keep, :]
    df = df.reset_index(drop=True)
    return df


user = os.getenv('GH_USERNAME')
token = os.getenv('GH_TOKEN')
auth = (user, token)


def _fetch_gh_api(repo, page=None):
    '''return API json response, plus the max page count'''
    url = f'https://api.github.com/repos/{repo}/stargazers'
    if page is not None:
        url += f"?page={page}"
    #print(url)
    # necessary to get starred_at data:
    headers = {'Accept': 'application/vnd.github.v3.star+json'}
    response = requests.get(url, headers=headers, auth=auth)

    data = response.json()
    try:
        link_text = response.headers['link']
        matches = re.findall(r'page=(\d*)', link_text)
        page_numbers = map(lambda s: int(s.split("=")[-1]), matches)
        N = max(page_numbers)
    except KeyError:
        N = 1
    return data, N


def get_github_stars(repo):
    data, N = _fetch_gh_api(repo)
    for i in range(2, N+1):
        data.extend(_fetch_gh_api(repo, i)[0])

    star_date = [d['starred_at'] for d in data]
    user_name = [d['user']['login'] for d in data]
    df = pd.DataFrame({'star_date': star_date, 'user_name': user_name})
    df['star_date'] = pd.to_datetime(df['star_date'])
    df = df.sort_values('star_date')
    return df


def plot_github_stars_timeseries(gh):
    star_curve = gh.set_index('star_date').assign(x=1).x.cumsum().resample('d').max()
    # project out to present:
    star_curve = pd.concat([star_curve, pd.Series({datetime.datetime.utcnow(): np.nan})])
    star_curve = star_curve.ffill()

    p = figure(height=350, x_axis_type="datetime")
    hover_tool = HoverTool(tooltips=[('Date', '@x{%Y-%m-%d}'), ('Total Stars', '@y')],
                           formatters={'@x': 'datetime'})
    hover_tool.point_policy = 'snap_to_data'
    p.add_tools(hover_tool)

    p.line(star_curve.index, star_curve)
    p.yaxis.axis_label = 'Total Stars'
    p.xaxis.axis_label = 'Date'
    return p
