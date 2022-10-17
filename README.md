# PV FOSS Engagement

This repository fetches, archives, and summaries ReadTheDocs analytics data for several open-source software projects related to solar photovoltaics.

#### Fetching

Unfortunately there is currently no way to access analytics data through the RTD API.  Instead, we use a manual python scraper: [scrape_readthedocs.py](./scrape_readthedocs.py).  This script is automatically run by GitHub Actions.

#### Archiving

Data files are stored in the [/data](./data) directory.  These files contain page view statistics for each day, RTD version, and URL path.

#### Summarizing

Jupyter notebooks importing these data files are rerun with the latest data and assembled into a sphinx website hosted here: https://kanderso-nrel.github.io/pv-foss-engagement/

This process is automatically run any time the `main` branch is updated, meaning the website will update by itself whenever new data is added to the repo or the notebooks are updated.