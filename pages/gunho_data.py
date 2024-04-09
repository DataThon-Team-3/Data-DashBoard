import plotly.express as px
import pandas as pd
import geopandas as gpd

india_gpd = gpd.read_file('../../../../india_gpd/India_gpd.shp')

india_gpd = india_gpd.drop(1)
india_gpd = india_gpd.set_index('ship_state')

india_gpd['center'] = india_gpd['geometry'].centroid
india_gpd['lon'] = india_gpd['center'].x
india_gpd['lat'] = india_gpd['center'].y

# 주별 인구대비 매출금액
india_gpd['Amount_population'] = india_gpd['Amount'] / india_gpd['Population'] * 100
# 주별 인구대비 시골인구
india_gpd['Rural_ratio'] = india_gpd['Rural'] / india_gpd['Population'] * 100
# 주별 인구대비 도시인구
india_gpd['Urban_ratio'] = india_gpd['Urban'] / india_gpd['Population'] * 100

india_gpd_table = india_gpd[['Qty', 'Amount', 'Population', 'Male', 'Female', 'Rural', 'Urban']].sort_values(by='Amount', ascending=False)


def create_choropleth_mapbox(color_col, title):
    fig = px.choropleth_mapbox(data_frame=india_gpd,
                               geojson=india_gpd.geometry,
                               locations=india_gpd.index,
                               color=color_col,
                               color_continuous_scale="BuGn",
                               range_color=(india_gpd[color_col].min(), india_gpd[color_col].max()),
                               mapbox_style="carto-positron",
                               zoom=3,
                               center={"lat": india_gpd['lat'].mean(), "lon": india_gpd['lon'].mean()},
                               opacity=0.5,
                               labels={color_col:'매출 금액'}
                              )

    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        title={
            'text': title,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 24}
        }
    )

    return fig
