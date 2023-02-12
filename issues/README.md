# Tools for generating issue statistics

The tools in this directory are meant to generate statistics from GitHub issues, e.g. calculating the lead times (depending on the definition this is the time between opening and closing an issue). For more fine-grained analytics the data from GitHub is augmented with additional data fetched from Zenhub.

For an optimal user experience, each calculation is split in a classical ETL manner into an "extract" and a "transform" phase.

## Prerequisites

- A GitHub token with permission to read issues for the target repository.
- A Zenhub token with permission to call the [REST API](https://github.com/ZenHubIO/API).
- Run `pip install -r requirements.txt` to install all the required dependencies.

## Extraction

The `fetch` tool fetches issue data from GitHub and Zenhub and stores the output in JSON format. See `fetch --help` for an explanation of how to use the tool.

## Transform

### Lead Times

The `leadtimes` tool calculates lead times of each issue in the input file from Zenhub event data. Lead time is defined as the time from when the issues has moved from the "In Progress" pipeline in Zenhub to the time the issues has been closed.

Run `leadtimes --help` for further information on the available flags.
