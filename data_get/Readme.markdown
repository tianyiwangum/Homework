### data structture of tree
the data structute is descibed in check_point.ipynb. and then it generates a tree.png in current dir. If you want to generate a json file, you can follow the folloing code.

code:

```python
from PIL import Image
import json

# Open the PNG image
image = Image.open("tree.png")

# Get the pixel data as a list of tuples
pixels = list(image.getdata())

# Convert the pixel data to a JSON-serializable format
json_data = {"pixels": pixels}

# Write the JSON data to a file
with open("tree.json", "w") as f:
    json.dump(json_data, f)

```
