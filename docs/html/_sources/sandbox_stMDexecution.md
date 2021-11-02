---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---


# Test stMarkdown -  Execution

```{code-cell} ipython3
note = "Python syntax highlighting"
print(note)
```


```{code-cell} ipython3
from IPython.core.display import display, HTML
from plotly.offline import init_notebook_mode, plot
init_notebook_mode(connected=True)

import plotly.io as pio
import plotly.express as px
import plotly.offline as py

print("Plotly loaded")
df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species", size="sepal_length")
fig

plot(fig, filename = 'figure.html')
display(HTML('figure.html'))
```
