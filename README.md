:no_entry: :no_entry_sign: :warning: This package is **NO LONGER IN USE** since the _Lever Open_ company and project closed.

# leveropen
Lever Open API Python Wrapper

[![Build Status](https://travis-ci.com/n-n-s/leveropen.svg?branch=main)](https://travis-ci.com/n-n-s/leveropen)
[![Documentation Status](https://readthedocs.org/projects/leveropen/badge/?version=latest)](https://leveropen.readthedocs.io/en/latest/?badge=latest)

This project enables access to Lever Open data using Python.

[View the documentation](https://leveropen.readthedocs.io/en/latest/)

## Installation

```
pip install leveropen
```

## Usage Example

*Note: This example uses the additional python package matplotlib*

```python
import matplotlib.pyplot as plt
from tqdm import tqdm

from leveropen import Lever

lever = Lever(access_token="your-unique-access-token")
dataset = lever.get_datasets_by_collection("Gross Domestic Product (GDP)")[0]
fig, ax = plt.subplots()
for series in tqdm(dataset.get_series(), desc="Parsing series objects", unit="SeriesObjects"):
    data = series.get_data()["Value"]
    data.plot(
        title=f"Collection: {dataset.collection}\nTopic: {dataset.topic}",
        ax=ax,
        label=series.name,
    )
ax.legend()
plt.show()
```

*Console:*

```console
Parsing datasets: 100%|██████████| 1/1 [00:00<00:00, 321.95datasets/s]
✔ Loading datasets successful
✔ Loading series data successful
Parsing series: 100%|██████████| 5/5 [00:00<00:00, 19765.81series/s]
Parsing series objects: 100%|██████████| 5/5 [00:05<00:00,  1.16s/SeriesObjects]
```

![](https://leveropen.readthedocs.io/en/latest/_images/lever_example_plot.png)

## Links

- https://www.leveropen.com
