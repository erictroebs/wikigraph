# WikiGraph
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-3c80ba.svg)](https://www.python.org/)

This project is the exam of a basic Python programming course at my university.
I release this mainly for educational purpose.


## Dependencies
- `Python 3.8+` (older versions might work but remain untested)
- `requests` (http interaction with Wikipedia)
- `igraph` (save graph representations to images and documents)


## Project Goals
##### From Exam Task
- breadth-first-search starting from any given Wikipedia article to every
  linked article
  - This must be implemented without any libraries except `requests`!
- command line parameters (see [Command Line Parameters](#command-line-parameters)):
  - maximum node limit `K` (see [-K](#command-line-parameters))
  - maximum depth limit `D` (see [-D](#command-line-parameters))
- output as adjacency matrix (see [-m](#command-line-parameters))
- basic graph operations:
  - get all neighbours / edges
  - search for the node with highest / lowest degree (see [-p](#command-line-parameters))
  - calculate graph density (see [-p](#command-line-parameters))
- export as image (see [--png](#command-line-parameters))
- highlight keywords (see [-h](#command-line-parameters))

##### Additional Self Defined
- simple http cache (see [--cache](#command-line-parameters))
  - This is a directory specified via command line parameters to save every
    requested articles HTML code to. There is only very simple checks to ensure
    cache validity and no expiry at all.
- maximum references per article limit (see [-R](#command-line-parameters))
- exclude articles from parsing (see [-e](#command-line-parameters))
  - It is possible to define an exclude function instead of a keyword list
    when using the `GraphBuilder` object from your own code to allow for
    fine-grained filtering.
- export as PDF (see [--pdf](#command-line-parameters))


## Getting Started
create and activate a virtual python environment
```bash
python -m venv env
source env/bin/activate
```

install python dependencies
```bash
pip install requests python-igraph
```

run main.py
```bash
python main.py https://en.wikipedia.org/wiki/Elon_Musk
```


## Command Line Parameters
parameter                | expects    | default | description
------------------------ | ---------- | ------- | --------------------------------------------
--help                   |            |         | show help
--help-md                |            |         | show help formatted as markdown
-v, --verbose            |            |         | set log level to info
-D, --maximum-depth      | number     | 10      | maximum distance from start article
-K, --maximum-nodes      | number     | 500     | maximum nodes in graph
-R, --maximum-references | number     |         | maximum references used per article
-e, --exclude            | identifier |         | exclude article from result graph
--png                    | path       |         | save graph to given png file
--pdf                    | path       |         | save graph to given pdf file
-h, --highlight          | keyword    |         | highlight articles containing a given phrase
--cache                  | directory  |         | directory to store downloaded HTML files in
-p, --properties         |            |         | print graph properties to stdout
-m, --matrix             |            |         | print adjacency matrix to stdout


## Further Examples
print properties and adjacency matrix:
```bash
python main.py -pm https://en.wikipedia.org/wiki/Elon_Musk
```

save graph to `musk.pdf`, highlight `Tesla` and `Bitcoin`, skip `SpaceX`:
```bash
python main.py -e SpaceX -h Tesla -h BitCoin --pdf musk.pdf https://en.wikipedia.org/wiki/Elon_Musk
```
