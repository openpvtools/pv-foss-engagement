
import pandas as pd
import pathlib

datadir = pathlib.Path(__file__).parent.parent.parent / 'data'


def get_analytics_data(project):
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

