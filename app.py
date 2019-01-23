from flask import Flask, render_template, request, Markup
from hip_hop_graph import plot_gen, top_10_rappers_bar, top_10_rappers_line
import pandas as pd

app = Flask(__name__)

@app.route("/")
def intro():
    plot = Markup(plot_gen())
    plot2 = Markup(top_10_rappers_bar())
    plot3 = Markup(top_10_rappers_line())
    return render_template("index.html", plot=plot,plot2=plot2,plot3=plot3)

if __name__ == "__main__":
    app.run(debug=True,threaded=True)