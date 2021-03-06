#%%
# Standard plot
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

x = np.linspace(0, 20, 100)
plt.plot(x, np.sin(x))

#%%
# Interactive Plot using Bokeh
from bokeh.io import push_notebook, show, output_notebook
from bokeh.layouts import row, gridplot
from bokeh.plotting import figure, show, output_file
output_notebook()

import numpy as np

x = np.linspace(0, 4*np.pi, 100)
y = np.sin(x)
TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select"

p1 = figure(title="Legend Example", tools=TOOLS)
p1.circle(x,   y, legend="sin(x)")
p1.circle(x, 2*y, legend="2*sin(x)", color="orange")
p1.circle(x, 3*y, legend="3*sin(x)", color="green")
show(p1)

#%%
# LaTeX
from IPython.display import Latex
Latex(r'F(k) = \int_{-\infty}^{\infty} f(x) e^{2\pi i k} dx')

#%%
# Inline images
from IPython.display import Image
Image('http://jakevdp.github.com/figures/xkcd_version.png')

#%%
# IFrame
from IPython.display import IFrame
URL = "https://donjayamanne.github.io/pythonVSCodeDocs/docs/python-path"
IFrame(URL, width=800, height=500)