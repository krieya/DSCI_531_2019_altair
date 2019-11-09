#!/usr/bin/env python
# coding: utf-8

# In[88]:


"""
Exploring Super Hero Movie Statistics Over Time
-----------------------------------------------
This is a case study of how the counts, ratings, gross and budget of super hero movies vary over time.

The Movies dataset contains information about super hero movies since 1978 to 2010. Before 2002, the count of super hero
films was always lower than 2, but since 2002, super hero films started to become popular as the count went up tp 6 per year.
Also, there are more movies with higher ratings in both websites since 2002. The highest rated movie in both websites, The Dark
Knight and The Incredibles, both released after 2002. 
In addition, the worldwide gross and production budget tend to grow higher since the year 2002 too.

"""

import pandas as pd
import altair as alt
from vega_datasets import data

sh_movies_df = (data.movies()
                .query('Creative_Type == "Super Hero"')
               )

sh_movies_df['Date'] = pd.to_datetime(sh_movies_df['Release_Date'])
sh_movies_df = sh_movies_df.set_index('Date')
sh_movies_df['Year'] = sh_movies_df.index.year
sh_movies_df['Rotten_Tomatoes_Rating'] = sh_movies_df['Rotten_Tomatoes_Rating'] / 100
sh_movies_df['IMDB_Rating'] = sh_movies_df['IMDB_Rating'] / 10

brush = alt.selection_interval(
    encodings = ['x']
)

years = alt.Chart(sh_movies_df).mark_bar().add_selection(
    brush
).encode(
    alt.X('Year:O', title = 'Release Year', axis = alt.Axis(labelAngle = 45)),
    alt.Y('count():Q', title='Counts')
).properties(
    width = 650,
    height = 80,
    title ='Super Hero Movie Counts')

ratings = alt.Chart(sh_movies_df).mark_circle().encode(
    alt.X('Rotten_Tomatoes_Rating:Q', title = 'Rotten Tomatoes Rating (Normalized)', scale = alt.Scale(domain = [0, 1])),
    alt.Y('IMDB_Rating:Q', title = 'IMDB Rating (Normalized)', scale = alt.Scale(domain = [0, 1])),
    alt.Tooltip(['Title:N', 'Rotten_Tomatoes_Rating:Q', 'IMDB_Rating:Q', 'Year:O']),
    opacity = alt.condition(brush, alt.value(0.75), alt.value(0.05))
).properties(
    width = 650,
    height = 400,
    title = 'Movie Ratings (Normalized) in IMDB and Rotten Tomatoes'
)

gross = alt.Chart(sh_movies_df).mark_circle().encode(
    alt.X('Production_Budget:Q', scale = alt.Scale(type='log',base = 10, zero = False),
         axis = alt.Axis(format = "~s"),
        title = 'Production Budget ($) (log_10 scale)'),
    alt.Y('Worldwide_Gross:Q', scale = alt.Scale(type='log',base = 10, zero = False),
         axis = alt.Axis(format = "~s"),
        title = 'Worldwide Gross ($) (log_10 scale)'),
    alt.Tooltip(['Title:N', 'Production_Budget:Q', 'Worldwide_Gross:Q', 'Year:O']),
    opacity = alt.condition(brush, alt.value(0.75), alt.value(0.05))
).properties(
    width = 650,
    height = 400,
    title = 'World Gross and Production Budget'
)

alt.vconcat(years, ratings, gross).properties(spacing = 10)

