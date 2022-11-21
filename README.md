# PV FOSS Engagement

This repository tracks and summarizes engagement statistics for several
open-source software projects related to solar photovoltaics.
See https://kanderso-nrel.github.io/pv-foss-engagement/

Currently this project tracks statistics for:

- [pvlib-python](https://github.com/pvlib/pvlib-python)
- [RdTools](https://github.com/NREL/rdtools)
- [pvanalytics](https://github.com/pvlib/pvanalytics)
- [twoaxistracking](https://github.com/pvlib/twoaxistracking)
- [Panel-Segmentation](https://github.com/NREL/Panel-Segmentation)

The summaries are computed in jupyter notebooks stored in this repository.
The notebooks in this repo may be out of date, but they are automatically
re-run when building the website, so the website itself will usually
reflect more recent data.
The website is automatically rebuilt any time the `main` branch is updated, meaning
the website will update by itself whenever new data is added to the repo or
the notebooks are updated.

Currently, this project uses two sources of data:

## GitHub stars

GitHub stars over time are retrieved from GitHub's "stargazers" API.  For now,
this project only summarizes the current dataset returned from that API.
That means that it only summarizes the users currently starring the project;
it has no concept of users that previously starred the project but later
unstarred it.

## ReadTheDocs page views

ReadTheDocs only reports data for roughly the last three months, so part of
this project is to periodically fetch and archive the latest data so it doesn't
get lost.  Unfortunately the older data from before this project started is
probably permanently gone.

#### Fetching

Unfortunately there is currently no way to access analytics data through the RTD API.
Instead, we use a manual python scraper: [scrape_readthedocs.py](./scrape_readthedocs.py).
This script is automatically run by GitHub Actions.

#### Archiving

Data files are stored in the [/data](./data) directory.
These files contain page view statistics for each day, RTD version, and URL path.
