import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
import geopandas as gpd
from matplotlib import rc
import seaborn as sns
from utils.path_utils import get_root_repo_path


JUNGMIN_DATA_DIR = get_root_repo_path().joinpath("data", "jungmin")

plt.rcParams["font.family"] = "AppleGothic"

st.title("아마존 인디아 웨어하우스 위치제안")
### sh_sel = Amazon sales data
sh_sel = pd.read_csv(JUNGMIN_DATA_DIR.joinpath("state_amazon_processed.csv"))
# st.dataframe(sh_sel, use_container_width = True)

### sidebar
option = st.sidebar.selectbox(
    "Select",
    [
        "2022 아마존 웨어하우스 현황",
        "주문량에 따른 웨어하우스 위치 제안",
        "풀필먼트에 따른 취소율",
    ],
)

# order_qtt = order quantity per state
order_qtt = pd.read_csv(JUNGMIN_DATA_DIR.joinpath("state_order_qtt.csv"))
# st.dataframe(order_qtt, use_container_width = True)

if option == "2022 아마존 웨어하우스 현황":
    st.write("2022 아마존 인디아 주 별 총 주문의 합 및 주 별 인구")
    # order_population = order quantity and state populations
    order_population = pd.read_csv(
        JUNGMIN_DATA_DIR.joinpath("Order_qtt_population.csv")
    )
    wh = pd.read_csv(JUNGMIN_DATA_DIR.joinpath("aws_warehouse.csv"))

    # st.dataframe(order_population, use_container_width = True)
    tab1, tab2 = st.tabs(["주 별 주문량 및 인구 수", "웨어하우스 위치"])
    with tab1:
        st.dataframe(order_population, use_container_width=True)
    with tab2:
        st.dataframe(wh, use_container_width=True)
    ##scatter plot
    # plot = sns.scatterplot(data=order_population, x="Total_Population", y="order_quantity")
    # plt.title('주 별 인구 및 총 주문횟수')
    # st.pyplot(plot.get_figure())

    geojson_path = JUNGMIN_DATA_DIR.joinpath("states_india.geojson")
    map_df = gpd.read_file(geojson_path)
    merged_map_df = map_df.assign(st_nm=lambda df: df["st_nm"].str.lower()).merge(
        order_population, how="left", left_on="st_nm", right_on="state"
    )
    fig, ax = plt.subplots(figsize=(16, 12))
    india_zipcode_to_geo = (
        pd.read_csv(
            JUNGMIN_DATA_DIR.joinpath("india_zipcode_geo.txt"), sep="\t", header=None
        )[[1, 9, 10]]
        .rename(columns={1: "zipcode", 9: "lat", 10: "long"})
        .drop_duplicates(subset=["zipcode"])
        .reset_index(drop=True)
    )
    # merged_map_df.plot(ax=plt.gca())
    merged_map_df.fillna({"order_quantity": 0}).plot(
        ax=ax,
        column="order_quantity",
        cmap="Blues",
        linewidth=0.8,
        edgecolor="0.8",
        legend=True,
    )
    ax.set_title("주문량 top15 주", fontsize=20)

    st.pyplot(fig)


elif option == "주문량에 따른 웨어하우스 위치 제안":
    st.write(
        "주문량 top 15 주 중 웨어하우가 없는 6개 지역에 아마존 웨어하우스 위치 제안 "
    )
    with st.expander("suggested states"):
        st.markdown(
            """
            - Kerala
            - Andhra Pradesh
            - Rajasthan
            - Bihar
            - Odisha
            - Madhya Pradesh
        """
        )
    geojson_path = JUNGMIN_DATA_DIR.joinpath("states_india.geojson")
    map_df = gpd.read_file(geojson_path)
    order_population = pd.read_csv(
        JUNGMIN_DATA_DIR.joinpath("Order_qtt_population.csv")
    )
    merged_map_df = map_df.assign(st_nm=lambda df: df["st_nm"].str.lower()).merge(
        order_population, how="left", left_on="st_nm", right_on="state"
    )

    wh = pd.read_csv(JUNGMIN_DATA_DIR.joinpath("aws_warehouse.csv"))
    india_zipcode_to_geo = (
        pd.read_csv(
            JUNGMIN_DATA_DIR.joinpath("india_zipcode_geo.txt"), sep="\t", header=None
        )[[1, 9, 10]]
        .rename(columns={1: "zipcode", 9: "lat", 10: "long"})
        .drop_duplicates(subset=["zipcode"])
        .reset_index(drop=True)
    )

    # map stating order quantity(color),location of warehouses(red dots), population (hover over)
    import plotly.express as px
    import json

    with open(geojson_path) as fd:
        india_geojson = json.load(fd)
    # Plot for Option 3
    plt.title("Graph for Option 3")
    # st.pyplot(plot_option_3.get_figure())
    fig = px.choropleth_mapbox(
        merged_map_df,
        geojson=india_geojson,
        color="order_quantity",
        color_continuous_scale="Blues",
        featureidkey="properties.cartodb_id",
        locations="cartodb_id",
        mapbox_style="carto-positron",
        zoom=3,
        center={"lat": 18.15, "lon": 79.09},
        hover_data=["state", "Total_Population"],
        opacity=0.8,
    )
    wh_geo = wh.merge(india_zipcode_to_geo, left_on="postal_code", right_on="zipcode")[
        ["code", "lat", "long"]
    ]
    wh_new_geo = pd.read_csv(JUNGMIN_DATA_DIR.joinpath("rec_location.csv"))
    wh_new_geo = wh_new_geo.merge(india_zipcode_to_geo, on="zipcode")[
        ["lat", "long", "state"]
    ]
    fig.add_scattermapbox(
        lat=wh_geo["lat"],
        lon=wh_geo["long"],
        mode="markers+text",
        text=wh_geo["code"],
        marker_size=6,
        marker_color="rgb(235, 0, 100)",
        name="Current Warehouse Location",
    )
    fig.add_scattermapbox(
        lat=wh_new_geo["lat"],
        lon=wh_new_geo["long"],
        mode="markers",
        marker_size=12,
        marker_color="rgb(0, 235, 100)",
        name="Suggested Warehouse Location",
    )
    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    st.plotly_chart(fig)


elif option == "풀필먼트에 따른 취소율":
    st.write(
        "웨어하우스가 늘어나서 풀필먼트가 아마존으로 변경되면 배송 취소율을 줄일 수 있음 "
    )
    sh = pd.read_csv(JUNGMIN_DATA_DIR.joinpath("full_cancel.csv"))
    # st.dataframe(sh,use_container_width = True )
    amazon_data = sh[sh["fullfilment"] == "Amazon"]
    amazon_cancelled_rate = (amazon_data["ship_status"] == "Cancelled").mean()

    merchant_data = sh[sh["fullfilment"] == "Merchant"]
    merchant_cancelled_rate = (merchant_data["ship_status"] == "Cancelled").mean()

    fig, ax = plt.subplots()
    bars = ax.bar(
        ["Amazon", "Merchant"],
        [amazon_cancelled_rate, merchant_cancelled_rate],
        color=["yellow", "green"],
    )
    ax.set_xlabel("Fulfillment")
    ax.set_ylabel("Cancellation Rate")
    ax.set_title("풀필먼트 타입(아마존/판매자)에 따른 배송 취소율")

    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{height:.2%}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
        )

    # Display the plot using st.pyplot()
    st.pyplot(fig)
