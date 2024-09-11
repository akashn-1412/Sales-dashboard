import streamlit as st
import pandas as pd
import plotly.express as px

# Function to plot visualizations
def plot_visualizations(df):
    st.write("## Visualization Dashboard")

    # Get numerical and categorical columns
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()

    # Bar Chart
    st.write("### Bar Chart")
    if categorical_columns:
        x_bar = st.selectbox("Select X-axis for Bar Chart", categorical_columns)
        y_bar = st.selectbox("Select Y-axis for Bar Chart", categorical_columns)
        if x_bar:
            fig_bar = px.bar(df, x=x_bar, y=y_bar, title=f"Bar Chart for {x_bar} vs {y_bar}")
            st.plotly_chart(fig_bar)

    # Line Chart
    st.write("### Line Chart")
    if numeric_columns:
        x_line = st.selectbox("Select X-axis for Line Chart", numeric_columns)
        y_line = st.selectbox("Select Y-axis for Line Chart", numeric_columns)
        if x_line:
            fig_line = px.line(df, x=x_line, y=y_line, title=f"Line Chart for {x_line} vs {y_line}")
            st.plotly_chart(fig_line)

    # Pie Chart
    st.write("### Pie Chart")
    if categorical_columns:
        pie_column = st.selectbox("Select a column for Pie Chart", categorical_columns)
        if pie_column:
            fig_pie = px.pie(df, names=pie_column, title=f"Pie Chart for {pie_column}")
            st.plotly_chart(fig_pie)

    # Area Chart
    st.write("### Area Chart")
    if numeric_columns:
        x_area = st.selectbox("Select X-axis for Area Chart", numeric_columns)
        y_area = st.selectbox("Select Y-axis for Area Chart", numeric_columns)
        if x_area:
            fig_area = px.area(df, x=x_area, y=y_area, title=f"Area Chart for {x_area} vs {y_area}")
            st.plotly_chart(fig_area)

    # Scatter Plot
    st.write("### Scatter Plot")
    if numeric_columns:
        scatter_x = st.selectbox("Select X-axis for Scatter Plot", numeric_columns)
        scatter_y = st.selectbox("Select Y-axis for Scatter Plot", numeric_columns)
        if scatter_x and scatter_y:
            fig_scatter = px.scatter(df, x=scatter_x, y=scatter_y, title=f"Scatter Plot: {scatter_x} vs {scatter_y}")
            st.plotly_chart(fig_scatter)

    # Histogram
    st.write("### Histogram")
    if numeric_columns:
        hist_column = st.selectbox("Select a column for Histogram", numeric_columns)
        if hist_column:
            fig_hist = px.histogram(df, x=hist_column, title=f"Histogram for {hist_column}")
            st.plotly_chart(fig_hist)

    # Box Plot
    st.write("### Box Plot")
    if numeric_columns:
        box_column = st.selectbox("Select a column for Box Plot", numeric_columns)
        if box_column:
            fig_box = px.box(df, y=box_column, title=f"Box Plot for {box_column}")
            st.plotly_chart(fig_box)

    # Treemap
    st.write("### Treemap")
    if categorical_columns:
        treemap_column = st.selectbox("Select a column for Treemap", categorical_columns)
        if treemap_column:
            fig_treemap = px.treemap(df, path=[treemap_column], title=f"Treemap for {treemap_column}")
            st.plotly_chart(fig_treemap)

    # Heatmap
    st.write("### Heatmap")
    if len(numeric_columns) > 1:  # Ensure there are at least two numeric columns
        fig_heatmap = px.imshow(df[numeric_columns].corr(), text_auto=True, title="Heatmap of Correlations")
        st.plotly_chart(fig_heatmap)
    else:
        st.write("Not enough numeric data available for heatmap.")

    # KPI Cards
    st.write("### KPI Cards")
    if numeric_columns:
        kpi_column = st.selectbox("Select a column for KPI", numeric_columns)
        if kpi_column:
            st.metric(label=f"Mean of {kpi_column}", value=f"{df[kpi_column].mean():.2f}")
            st.metric(label=f"Sum of {kpi_column}", value=f"{df[kpi_column].sum():.2f}")
            st.metric(label=f"Max of {kpi_column}", value=f"{df[kpi_column].max():.2f}")
            st.metric(label=f"Min of {kpi_column}", value=f"{df[kpi_column].min():.2f}")

# Main Streamlit app
def main():
    st.sidebar.title("Simplified Visualization Dashboard")
    
    # Upload CSV file
    uploaded_file = st.sidebar.file_uploader("Upload your Dataset (CSV format)", type="csv")

    if uploaded_file is not None:
        # Read the CSV file with encoding handling
        try:
            df = pd.read_csv(uploaded_file, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(uploaded_file, encoding='latin1')
        
        st.write("### Data Preview", df.head())

        # Plot visualizations with filters
        plot_visualizations(df)

if __name__ == "__main__":
    main()
