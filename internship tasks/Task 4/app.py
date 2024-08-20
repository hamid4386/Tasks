# Author Details:

### **Name: Muhammad Hamid**
### **linkedin** :https://www.linkedin.com/in/muhammad-hamid-87242a312/

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import warnings
import plotly.figure_factory as ff
warnings.filterwarnings("ignore")
import os
import datetime as dt
import seaborn



# setting up page

st.set_page_config(" Supermarket", page_icon=":bar_chart:", layout="wide")

st.title(":bar_chart: Supermarket Sales Dashboard")
st.markdown("<style>div.block-container{padding-top:2.5rem;}</style>", unsafe_allow_html=True)


# uploading file
fl = st.file_uploader(":file_folder: Upload a file", type=["csv", "xlsx", "txt", "xls"])

if fl is not None: 
    filename = fl.name
    st.write(f"File uploaded: {filename}")
    df = pd.read_csv(filename)

else:
    df = pd.read_csv("superstore.csv")


# createing date picker

col1, col2 = st.columns((2))

df["Order Date"] = pd.to_datetime(df["Order Date"])

# geting min and max date

start_date = pd.to_datetime(df["Order Date"].min())
end_date = pd.to_datetime(df["Order Date"].max())

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", start_date))

with col2:
    Date2 = pd.to_datetime(st.date_input("End Date", end_date))


df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= Date2)].copy()


# creating sidebar
st.sidebar.header("Filter data:")

region = st.sidebar.multiselect("Select your Region", df["Region"].unique())

if not region:
    df2 = df.copy()
else:
    df2 = df[df["Region"].isin(region)]

# create for state

state = st.sidebar.multiselect("Select your State", df2["State"].unique())

if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2["State"].isin(state)]

# create for city

city = st.sidebar.multiselect("Select your City", df3["City"].unique())

# filter teh data based on region, state and city

if not region and not state and not city:
    filtered_df = df
elif not state and not city:
    filtered_df = df[df['Region'].isin(region)]
elif not region and not city:
    filtered_df = df[df['State'].isin(state)]
elif state and city:
    filtered_df = df3[df['State'].isin(state) & df3["City"].isin(city)]
elif region and city:
    filtered_df = df3[df['Region'].isin(region) & df3["City"].isin(city)]
elif region and state:
    filtered_df = df3[df['Region'].isin(region) & df3["State"].isin(state)]
elif city:
    filtered_df = df3[df3["City"].isin(city)]
else:
    filtered_df = df3[df3['Region'].isin(region) & df3['State'].isin(state) & df3["City"].isin(city)]


# create a column chart for category and region

category_df = filtered_df.groupby(by =["Category"], as_index = False)["Sales"].sum()

with col1:
    st.subheader("Category wise Sales")
    fig = px.bar(category_df, x="Category", y="Sales", text=["${:,.2f}".format(x) for x in category_df["Sales"]], template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)


with col2:
    st.subheader("Region wise Sales")
    fig=  px.pie(filtered_df, values="Sales", names="Region", hole=0.5, template="seaborn")
    fig.update_traces(text=filtered_df["Region"], textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True)



cl1 , cl2 = st.columns((2))

with cl1:
    with st.expander("View Data based on category"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv = category_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download data", data=csv, file_name="category_data.csv", mime="text/csv",
                        help="click here to download the data") 
    

with cl2:
    with st.expander("View Data based on Region"):
        region = filtered_df.groupby(by=["Region"], as_index=False)["Sales"].sum()
        st.write(category_df.style.background_gradient(cmap="Oranges"))
        csv = category_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download data", data=csv, file_name="region_data.csv", mime="text/csv",
                        help="click here to download the data") 
        
filtered_df['month_year'] = filtered_df['Order Date'].dt.to_period('M')
st.subheader("Time series analysis")

line_chart = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y : %b"))['Sales'].sum()).reset_index()
fig2 = px.line(line_chart, x="month_year", y="Sales", labels={"Sales" : "Amount"}, height=500, width=1000, template="gridon")

st.plotly_chart(fig2, use_container_width=True)

with st.expander("View Data based on Time series"):
    st.write(line_chart.T.style.background_gradient(cmap="Greens"))
    csv = line_chart.to_csv(index=False).encode('utf-8')
    st.download_button("Download data", data=csv, file_name="time_series_data.csv", mime="text/csv",
                        help="click here to download the data")
    


# lets create treamap for based on region,category and sub-category

st.subheader("Treemap Analysis")

fig3 = px.treemap(filtered_df, path=["Region", "Category", "Sub-Category"], values="Sales", hover_data=["Sales"], color="Sub-Category")

fig3.update_layout(width=850, height=650)

st.plotly_chart(fig3, use_container_width=True)

with st.expander("View Data based on Treemap"):

    treemap = filtered_df.groupby(["Region", "Category", "Sub-Category"], as_index=False)["Sales"].sum()
    st.write(treemap.T.style.background_gradient(cmap="Reds"))
    csv = treemap.to_csv(index=False).encode('utf-8')
    st.download_button("Download data", data=csv, file_name="treemap_data.csv", mime="text/csv",
                        help="click here to download the data")
    

chart1, chart2 = st.columns((2))

with chart1:
    st.subheader("Segment wise Sales")
    fig = px.pie(filtered_df, names="Segment", values="Sales", hole=0.5, template="plotly_dark")
    fig.update_traces(text= filtered_df["Segment"], textposition="inside")
    st.plotly_chart(fig, use_container_width=True)

with chart2:
    st.subheader("Category wise Sales")
    fig = px.pie(filtered_df, names="Category", values="Sales", hole=0.5, template= "gridon")
    fig.update_traces(text= filtered_df["Category"], textposition="inside")
    st.plotly_chart(fig, use_container_width=True)

st.subheader(":point_right: month wise sub-category sales summary")

with st.expander("Summary table"):
    df_sample = df[0:5][["Region", "Category", "Sub-Category", "Sales", "Quantity", "Discount", "Profit"]]

    fig = ff.create_table(df_sample, colorscale="cividis")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("month wise sub category sales summary")
    filtered_df["month"] = filtered_df["Order Date"].dt.month_name()
    sub_category_Year = pd.pivot_table(data = filtered_df, values="Sales", index="Sub-Category", columns="month")

    st.write(sub_category_Year.style.background_gradient(cmap="Blues"))


# create a scatter plot

data1 = px.scatter(filtered_df, x = "Sales", y = "Profit", size="Quantity")
data1['layout'].update(title="Relation between Sales and Profit",
                       titlefont=dict(size=20),xaxis=dict(title="Sales",titlefont=dict(size=19)),yaxis=dict(title="Profit",titlefont=dict(size=19)))

st.plotly_chart(data1, use_container_width=True)

with st.expander("View Data"):
    st.write(filtered_df.iloc[:500,1:20:2].style.background_gradient(cmap="Oranges"))

# donload original dataSet

csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Download data", data=csv, file_name="data.csv", mime="text/csv")