git# News Manager

Simple news manager provided by VNExpress RSS

## Description

An in-depth paragraph about your project and overview of use.

## Getting Started

### Dependencies

* Ubuntu 18.04
* Python 3.10
* Poetry 1.3.1

### Installing

* Install from poetry
```
cd ./opt
cp .env.example .env
poetry install
```

### Executing program

* Run admin API
```
poetry run python main.py
```

* Run public API
```
poetry run python main_2.py
```

* Run cronjob
```
poetry run python cron_run.py
```

## Help

Any advice for common problems or issues.
```
command to run if program contains helper info
```

## Acknowledgments

Inspiration, code snippets, etc.
* [VNExpress RSS](https://vnexpress.net/rss)
