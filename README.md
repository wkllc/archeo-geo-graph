# Analyze historical trades using Graph theory

TODO: Consult Tsveta for better summary

## Dataset

* `coordinates.csv` contains the latitude and longitude coordinates of archeological sites
* `imports_detailed.csv` contains the following information for trade route specified by a `source` and `target` site:
    * % of imports for site per century - variable `percent_imports`
    * % of all pottery for site per century - variable `percent_all_pottery`
* `imports_combined.csv` combines regions with multiple sites into a single site/node - e.g. Italian sites

## Graph Theory analysis

Graph theory provides us with statistical methods that can shine new light on historical trades.

For this project 3 main scripts were developed:
* `graph_analysis.py`
    - computes degree of connectedness of a trade network
* `compare_networks.py`
    - compares the distance between two networks, offering insight into difference between e.g. 2 centuries
* `visualize.py`
    - creates a visualization of the trade network, using a world map
    * `visualize_abstract.py` creates the same visualization but wihtout the world map, for more abstract visualization

## Running the analaysis

1. setup python/conda environment
1. install requirements
1. from the root folder run the desired script, e.g.
```bash
python -m scripts.graph_analysis
```
or
```bash
python -m scripts.visualize -query 'Mytilini'
```
to produce figures like:

![Network of Mytilini's trade routes from imports data](figures/Mytilini_network.png)

