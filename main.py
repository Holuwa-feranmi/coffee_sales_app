import pandas as pd 
import streamlit as st 


def load_data():
    df = pd.read_excel("Coffe_sales.xlsx")
    # replace the NaN with "None" / "Non-Card"
    df.loc[:, "card"] = df.card.fillna("Non-card")

    return df
try:
    df = load_data()

    st.title("COFFEE SALES APP")

    # filters
    filters = {
        "coffee_name": df["coffee_name"].unique(),
        "Time_of_Day": df["Time_of_Day"].unique(),
        "Month_namee": df["Month_name"].unique(),
        "cash_type": df["cash_type"].unique(),
        "Weekday": df["Weekday"].unique(),
    }
    # store user selection
    selected_filters = {}

    # generate multi-select widgets dynamically
    for key, options in filters.items():
        selected_filters[key] = st.sidebar.multiselect(key,options)

    # take a copy of the data 
    filtered_df = df.copy()

    # apply filter selection to the data
    for key, selected_values in selected_filters.items():
        if selected_values:
            filtered_df = filtered_df[filtered_df[key].isin(selected_values)]

    # display the data
           
    st.dataframe(filtered_df)

    # section 2 : Calculations
    no_of_cups = len(filtered_df)
    total_revenue = filtered_df["money"].sum()
    avg_sale = filtered_df["money"].mean()
    perct_sales_contrib = f"{(total_revenue / df["money"].sum()) * 100:,.2f}%"

    # display a quick overview using metrics

    st.write("### Quick Overview")

    # streamlit column components
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Cups Sold: ", no_of_cups)

    with col2:
        st.metric("Revenue: ", f"{total_revenue:,.2f}")

    with col3:
        st.metric("Avg_Sale: ", f"{avg_sale:,.2f}")

    with col4:
        st.metric("percent Contribution to Sales: ", perct_sales_contrib)

    # Analysis Findings Based on Research Question
    st.write("### Analysis Findings")

    temp_1 = df["Time_of_Day"].value_counts().reset_index()
    temp_1.columns = ["Time of Day", "Cups sold"]

    st.dataframe(temp_1)

    # simple chart
    import altair as alt

    chart_1 = alt.Chart(temp_1).mark_bar().encode(
        x=alt.X("Cups sold:Q"),
        y=alt.Y("Time of Day:N"),
        color=alt.Color("Time of Day:N", legend=None)

    ).properties(height = 250)

    # display the chart
    st.altair_chart(chart_1, use_container_width=True)

    # Top coffee Types
    st.write("### Revenue by Coffee Types")
    temp_2 = filtered_df.groupby("coffee_name")["money"] .sum().reset_index().sort_values(by = "money",ascending=False)
    # temp_2.columns = []

    st.dataframe(temp_2)

    chart_2 = alt.Chart(temp_2).mark_bar().encode(
        x=alt.X("coffee_name", sort='-y'),
        y="money"
    ).properties(
        title=f"Top 5 Coffee Sales by  Revenue"
    )
    chart_2

    # Average Revenue by Coffee Sold
    st.write("### Avg Revenue of Coffee Sold ")
    temp_3 = filtered_df.groupby("coffee_name")["money"].mean().reset_index()

    st.dataframe(temp_3)

    chart_3 = alt.Chart(temp_3).mark_line(point=True).encode(
        x="coffee_name",
        y="money"
    ).properties(
        title="Average Revenue of Coffee Sold"
    )
    chart_3

    # Monthly Sales Trend
    st.write("### Monthly Sales Trend")
    temp_4 = filtered_df.groupby(["Month_name"])["money"].sum().reset_index()

    st.dataframe(temp_4)

    chart_4 = alt.Chart(temp_4).mark_area().encode(
        x=alt.X("Month_name", sort=temp_4),
        y= "money"
    ).properties(
        title= "Monthly Sales Trend"
    )
    chart_4


except Exception as e:
    st.error("Error: check error details")

    with st.expander("Error Details"):
        
        st.code(str(e))
    # st.code(traceback.format_exc())
