import matplotlib.pyplot as plt
from tqdm import tqdm

from leveropen import Lever

lever = Lever()
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
