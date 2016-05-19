from flask import Blueprint, request, render_template
import tempfile

import numpy as np
import pandas as pd
import seaborn as sns  # For default styling
from . import app
from .config import TEMP_PLOT_DIR

@app.route('/')
def index():
    df = pd.DataFrame({
        'Date': pd.date_range('2010-01-01', '2015-01-01', freq='M'),
        'Budget': np.random.choice(np.arange(200000, 300000), 60),
        'Actual': np.random.choice(np.arange(200000, 300000), 60)
        })
    df.set_index('Date', inplace=True)
    ax = df.plot(legend=['Budget', 'Actual'], figsize=(12, 8))
    ax.set_xlabel('Date')

    temp_plt_file = tempfile.NamedTemporaryFile(
        dir=TEMP_PLOT_DIR, suffix='.png',delete=False)
    ax.get_figure().savefig(temp_plt_file)
    # get the file's name (rather than the whole path
    plot_png = temp_plt_file.name.split('/')[-1]

    table_html = (df.head(20)
                    .reset_index()
                    .to_html(classes=['u-full-width'], index=False)
                    .replace('border="1"','border="0"')
                )

    # custom_format = lambda x: '<span class="significant"><bold>%f</bold></span>' % x
    # table_html = df.head(20).reset_index().to_html(classes=['u-full-width'],
    #     formatters={'actual': custom_format}, index=False).replace('border="1"','border="0"')
    return render_template('index.html',
        data_table=table_html, plot_png=plot_png)

@app.route('/d3-var1/')
def d3_var1():
    df = pd.read_table("app/data/jobs.tsv")
    table_html = (df.head(20)
                    .to_html(classes=['u-full-width'], index=False)
                    .replace('border="1"','border="0"')
                )

    data_json = df.to_json(orient="records")
    return render_template('d3-var1.html', data_json=data_json, data_table=table_html)

