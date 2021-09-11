import pandas as pd
import numpy as np
import json
from flask import jsonify


def calculatingDistance(latitude, longitude, limit):
    df = pd.read_csv('venues.csv')
    df['latitude_x'] = float(latitude)
    df['longitude_y'] = float(longitude)
    df['distance'] = np.linalg.norm(
        df[["latitude", "longitude"]].values - df[["latitude_x", "longitude_y"]].values, axis=1)

    # setting response limits and sorting by venue distance
    df.sort_values(["distance"], ascending=(True), inplace=True)

    return df.head(int(limit))


def splitCategories(df):

    # splitting multiple categories into single ones
    df['categories'] = df.categories.apply(
        lambda x: "".join(x for x in str(x)))
    categories_split = pd.concat([pd.Series(row['name'], row['categories'].split(','))
                                  for _, row in df.iterrows()]).reset_index()

    categories_split.columns = ['categories', 'name']

    # replacing old categories column with the split categories
    df.drop(columns=['categories'], inplace=True)
    categorized_venues_df = pd.merge(df, categories_split, on='name')

    # calculating no of venues in each category for soring
    g = categorized_venues_df.groupby(
        ['categories']).size().reset_index(name='counts')
    categorized_venues_df = pd.merge(g, categorized_venues_df, on='categories')
    return categorized_venues_df


def toJson(df):

    # formatting df
    df = (df.groupby(['categories', 'counts'], as_index=True)
          .apply(lambda x: x[['name', 'address']].to_dict('r'))
          .reset_index()
          .rename(columns={0: 'Venues'}))

    # sorting df
    df.sort_values(["counts"], ascending=(False), inplace=True)
    df.drop(columns='counts', inplace=True)

    # df => json
    j = df.to_json(orient='records')

    return (json.dumps(json.loads(j), indent=2, sort_keys=False))
