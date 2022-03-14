#
# from typing import Sequence
#
# import numpy as np
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
#
#
# data1 = np.array([[0.4, 0.4, 0.2], [0, 0.1, 0.9]])
# data2 = np.array([[0.4, 0.2, 0.4], [0.2, 0.1, 0.7]])
#
#
# def make_df(data: np.ndarray, column_names: Sequence[str], size_column: bool = True) -> pd.DataFrame:
#     """Return a dataframe from a numpy array with column names.
#
#     The dataframe also has a column ``iter`` to index the rows, and a column ``dummy_column_for_size`` so that Plotly can later specify the size.
#
#     Args:
#         data: A numpy array.
#         column_names: A sequence of column names.
#         size_column: If True, add a column ``dummy_column_for_size`` to the dataframe.
#     Returns:
#         A pandas dataframe.
#     """
#     df = pd.DataFrame(data, columns=column_names)
#     # rename the index column and make it into an extra column with name "iter"
#     df.index.name = "iter"
#     df.reset_index(inplace=True)
#
#     if size_column:
#         df["dummy_column_for_size"] = 1
#     return df
#
#
# names = ["Rock", "Paper", "Scissor"]
# df1 = make_df(data1, names)
# df2 = make_df(data2, names)
#
# # make a new df which with a combination of df1 and df2 with one extra column "player"
# # to distinguish between the two dataframes
# df = pd.concat([df1, df2], ignore_index=True)
# df['player'] = ['1'] * len(df1) + ['2'] * len(df2)
# print('df:')
# print(df)
#
#
# def plot_ternary(df, column_names):
#     return go.Scatterternary(
#         dict(
#             a=df[column_names[0]],
#             b=df[column_names[1]],
#             c=df[column_names[2]],
#             mode='markers',
#             marker=dict(
#                 size=14,
#                 color='#DB7365',
#             ),
#             text=df['iter'],
#             hoverinfo='text'
#         ))
#
#
# fig = make_subplots(rows=1, cols=2, specs=[
#     [{'type': 'ternary'}, {'type': 'ternary'}]])
#
# subfig1 = plot_ternary(df, names)
# fig.add_trace(subfig1, row=1, col=1)
# fig.add_trace(subfig1, row=1, col=2)
#
#
# def makeAxis(title, tickangle):
#     return {
#         'title': title,
#         'titlefont': {'size': 20},
#         'tickangle': tickangle,
#         'tickfont': {'size': 15},
#         'tickcolor': 'rgba(0,0,0,0)',
#         'ticklen': 5,
#         'showline': True,
#         'showgrid': True
#     }
#
#
# # label the axes
# # Update xaxis properties
# fig.update_aaxis(title_text="xaxis 1 title", row=1, col=1)
# fig.update_xaxes(title_text="xaxis 2 title", range=[10, 50], row=1, col=2)
# fig.update_xaxes(title_text="xaxis 3 title", showgrid=False, row=2, col=1)
# fig.update_xaxes(title_text="xaxis 4 title", type="log", row=2, col=2)
#
# # Update yaxis properties
# fig.update_yaxes(title_text="yaxis 1 title", row=1, col=1)
# fig.update_yaxes(title_text="yaxis 2 title", range=[40, 80], row=1, col=2)
# fig.update_yaxes(title_text="yaxis 3 title", showgrid=False, row=2, col=1)
# fig.update_yaxes(title_text="yaxis 4 title", row=2, col=2)
# # fig.update_layout(height=600, width=1500, title_text="Side By Side Subplots")
# fig.show()


import os
import webbrowser
#url = "http://docs.python.org/library/webbrowser.html"
filename = 'index.html'
url = 'file://' + os.path.realpath(filename)
webbrowser.open(url)
