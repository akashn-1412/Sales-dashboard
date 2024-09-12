import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
import seaborn as sns
import altair as alt
from sklearn.preprocessing import LabelEncoder

# Hide Streamlit footer
st.markdown("""
    <style>
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Streamlit app title and description
st.title('Sales Analysis Dashboard')
st.write('Upload your dataset to automatically generate and visualize relevant graphs and charts. Use the sidebar to filter and customize each visualization.')



# Function to plot network graphs
def plot_network_graph(df):
    if 'Source' in df.columns and 'Target' in df.columns:
        G = nx.from_pandas_edgelist(df, 'Source', 'Target')
        pos = nx.spring_layout(G, seed=42)
        edge_trace = go.Scatter(
            x=[],
            y=[],
            mode='lines',
            line=dict(width=0.5, color='#888'),
            hoverinfo='none'
        )
        node_trace = go.Scatter(
            x=[],
            y=[],
            mode='markers',
            text=[],
            marker=dict(size=10, color='#ff7f0e', line=dict(width=2, color='#000'))
        )
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace['x'] += (x0, x1, None)
            edge_trace['y'] += (y0, y1, None)
        
        for node in G.nodes():
            x, y = pos[node]
            node_trace['x'] += (x,)
            node_trace['y'] += (y,)
            node_trace['text'] += (node,)
        
        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=0, l=0, r=0, t=0)
                        ))
        st.plotly_chart(fig)

# Function to generate and display all visualizations
def generate_visualizations(df):
    st.write("## Automated Visualization Dashboard")

    if df.empty:
        st.error("The uploaded dataset is empty. Please upload a valid file.")
        return



    # Automatically display all charts initially
    # Bar Chart
    if df.select_dtypes(include=['object']).shape[1] > 0 and df.select_dtypes(include=['number']).shape[1] > 0:
        cat_col = df.select_dtypes(include=['object']).columns[0]
        num_col = df.select_dtypes(include=['number']).columns[0]
        fig_bar = px.bar(df, x=cat_col, y=num_col, title=f"Bar Chart for {cat_col} vs {num_col}")
        st.plotly_chart(fig_bar)

    # Line Chart
    if df.select_dtypes(include=['number']).shape[1] > 1:
        x_col = df.select_dtypes(include=['number']).columns[0]
        y_col = df.select_dtypes(include=['number']).columns[1]
        fig_line = px.line(df, x=x_col, y=y_col, title=f"Line Chart for {x_col} vs {y_col}")
        st.plotly_chart(fig_line)

    # Pie Chart
    if df.select_dtypes(include=['object']).shape[1] > 0:
        cat_col = df.select_dtypes(include=['object']).columns[0]
        fig_pie = px.pie(df, names=cat_col, title=f"Pie Chart for {cat_col}")
        st.plotly_chart(fig_pie)

    # Scatter Plot
    if df.select_dtypes(include=['number']).shape[1] > 1:
        x_col = df.select_dtypes(include=['number']).columns[0]
        y_col = df.select_dtypes(include=['number']).columns[1]
        fig_scatter = px.scatter(df, x=x_col, y=y_col, title=f"Scatter Plot: {x_col} vs {y_col}")
        st.plotly_chart(fig_scatter)

    # Histogram
    if df.select_dtypes(include=['number']).shape[1] > 0:
        num_col = df.select_dtypes(include=['number']).columns[0]
        fig_hist = px.histogram(df, x=num_col, title=f"Histogram for {num_col}")
        st.plotly_chart(fig_hist)

    # Box Plot
    if df.select_dtypes(include=['number']).shape[1] > 0:
        num_col = df.select_dtypes(include=['number']).columns[0]
        fig_box = px.box(df, y=num_col, title=f"Box Plot for {num_col}")
        st.plotly_chart(fig_box)

    # Heatmap
    if df.select_dtypes(include=['number']).shape[1] > 1:
        fig_heatmap = px.imshow(df.select_dtypes(include=['number']).corr(), text_auto=True, title="Heatmap of Correlations")
        st.plotly_chart(fig_heatmap)

    # Treemap
    if df.select_dtypes(include=['object']).shape[1] > 0:
        cat_col = df.select_dtypes(include=['object']).columns[0]
        fig_treemap = px.treemap(df, path=[cat_col], title=f"Treemap for {cat_col}")
        st.plotly_chart(fig_treemap)

    # Time Series Plot
    if 'Date' in df.columns and df.select_dtypes(include=['number']).shape[1] > 0:
        date_col = [col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col])][0]
        value_col = df.select_dtypes(include=['number']).columns[0]
        fig_time = px.line(df, x=date_col, y=value_col, title=f"Time Series for {value_col}")
        st.plotly_chart(fig_time)

    # Network Visualization
    if 'Source' in df.columns and 'Target' in df.columns:
        plot_network_graph(df)

    # Altair Chart
    if df.select_dtypes(include=['number']).shape[1] > 1:
        x_col = df.select_dtypes(include=['number']).columns[0]
        y_col = df.select_dtypes(include=['number']).columns[1]
        chart = alt.Chart(df).mark_point().encode(
            x=x_col,
            y=y_col
        ).properties(
            title=f"Altair Chart: {x_col} vs {y_col}"
        )
        st.altair_chart(chart)

    # Sidebar for customization
    st.sidebar.write("### Customize Visualizations")
    st.sidebar.write("Use the filters below to adjust the visualizations.")

    # Bar Chart customization
    st.sidebar.write("### Bar Chart Customization")
    if st.sidebar.checkbox('Show Custom Bar Chart'):
        if df.select_dtypes(include=['object']).shape[1] > 0 and df.select_dtypes(include=['number']).shape[1] > 0:
            cat_col = st.sidebar.selectbox('Select Categorical Column for Bar Chart', df.select_dtypes(include=['object']).columns)
            num_col = st.sidebar.selectbox('Select Numerical Column for Bar Chart', df.select_dtypes(include=['number']).columns)
            fig_bar = px.bar(df, x=cat_col, y=num_col, title=f"Bar Chart for {cat_col} vs {num_col}")
            st.plotly_chart(fig_bar)
        else:
            st.write("Not enough categorical or numerical data for a Bar Chart.")

    # Line Chart customization
    st.sidebar.write("### Line Chart Customization")
    if st.sidebar.checkbox('Show Custom Line Chart'):
        if df.select_dtypes(include=['number']).shape[1] > 1:
            x_col = st.sidebar.selectbox('Select X Column for Line Chart', df.select_dtypes(include=['number']).columns)
            y_col = st.sidebar.selectbox('Select Y Column for Line Chart', df.select_dtypes(include=['number']).columns)
            fig_line = px.line(df, x=x_col, y=y_col, title=f"Line Chart for {x_col} vs {y_col}")
            st.plotly_chart(fig_line)
        else:
            st.write("Not enough numerical data for a Line Chart.")

    # Pie Chart customization
    st.sidebar.write("### Pie Chart Customization")
    if st.sidebar.checkbox('Show Custom Pie Chart'):
        if df.select_dtypes(include=['object']).shape[1] > 0:
            cat_col = st.sidebar.selectbox('Select Categorical Column for Pie Chart', df.select_dtypes(include=['object']).columns)
            fig_pie = px.pie(df, names=cat_col, title=f"Pie Chart for {cat_col}")
            st.plotly_chart(fig_pie)
        else:
            st.write("Not enough categorical data for a Pie Chart.")

    # Scatter Plot customization
    st.sidebar.write("### Scatter Plot Customization")
    if st.sidebar.checkbox('Show Custom Scatter Plot'):
        if df.select_dtypes(include=['number']).shape[1] > 1:
            x_col = st.sidebar.selectbox('Select X Column for Scatter Plot', df.select_dtypes(include=['number']).columns)
            y_col = st.sidebar.selectbox('Select Y Column for Scatter Plot', df.select_dtypes(include=['number']).columns)
            fig_scatter = px.scatter(df, x=x_col, y=y_col, title=f"Scatter Plot: {x_col} vs {y_col}")
            st.plotly_chart(fig_scatter)
        else:
            st.write("Not enough numerical data for a Scatter Plot.")

    # Histogram customization
    st.sidebar.write("### Histogram Customization")
    if st.sidebar.checkbox('Show Custom Histogram'):
        if df.select_dtypes(include=['number']).shape[1] > 0:
            num_col = st.sidebar.selectbox('Select Numerical Column for Histogram', df.select_dtypes(include=['number']).columns)
            fig_hist = px.histogram(df, x=num_col, title=f"Histogram for {num_col}")
            st.plotly_chart(fig_hist)
        else:
            st.write("Not enough numerical data for a Histogram.")

    # Box Plot customization
    st.sidebar.write("### Box Plot Customization")
    if st.sidebar.checkbox('Show Custom Box Plot'):
        if df.select_dtypes(include=['number']).shape[1] > 0:
            num_col = st.sidebar.selectbox('Select Numerical Column for Box Plot', df.select_dtypes(include=['number']).columns)
            fig_box = px.box(df, y=num_col, title=f"Box Plot for {num_col}")
            st.plotly_chart(fig_box)
        else:
            st.write("Not enough numerical data for a Box Plot.")

    # Heatmap customization
    st.sidebar.write("### Heatmap Customization")
    if st.sidebar.checkbox('Show Custom Heatmap'):
        if df.select_dtypes(include=['number']).shape[1] > 1:
            fig_heatmap = px.imshow(df.select_dtypes(include=['number']).corr(), text_auto=True, title="Heatmap of Correlations")
            st.plotly_chart(fig_heatmap)
        else:
            st.write("Not enough numerical data for a Heatmap.")

    # Treemap customization
    st.sidebar.write("### Treemap Customization")
    if st.sidebar.checkbox('Show Custom Treemap'):
        if df.select_dtypes(include=['object']).shape[1] > 0:
            cat_col = st.sidebar.selectbox('Select Categorical Column for Treemap', df.select_dtypes(include=['object']).columns)
            fig_treemap = px.treemap(df, path=[cat_col], title=f"Treemap for {cat_col}")
            st.plotly_chart(fig_treemap)
        else:
            st.write("Not enough categorical data for a Treemap.")

    # Time Series Plot customization
    st.sidebar.write("### Time Series Plot Customization")
    if st.sidebar.checkbox('Show Custom Time Series Plot'):
        if 'Date' in df.columns and df.select_dtypes(include=['number']).shape[1] > 0:
            date_col = st.sidebar.selectbox('Select Date Column for Time Series Plot', [col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col])])
            value_col = st.sidebar.selectbox('Select Numerical Column for Time Series Plot', df.select_dtypes(include=['number']).columns)
            fig_time = px.line(df, x=date_col, y=value_col, title=f"Time Series for {value_col}")
            st.plotly_chart(fig_time)
        else:
            st.write("Not enough data for a Time Series Plot.")

    # Network Graph customization
    st.sidebar.write("### Network Graph Customization")
    if st.sidebar.checkbox('Show Custom Network Graph'):
        if 'Source' in df.columns and 'Target' in df.columns:
            plot_network_graph(df)
        else:
            st.write("Not enough data for a Network Graph.")

    # Altair Chart customization
    st.sidebar.write("### Altair Chart Customization")
    if st.sidebar.checkbox('Show Custom Altair Chart'):
        if df.select_dtypes(include=['number']).shape[1] > 1:
            x_col = st.sidebar.selectbox('Select X Column for Altair Chart', df.select_dtypes(include=['number']).columns)
            y_col = st.sidebar.selectbox('Select Y Column for Altair Chart', df.select_dtypes(include=['number']).columns)
            chart = alt.Chart(df).mark_point().encode(
                x=x_col,
                y=y_col
            ).properties(
                title=f"Altair Chart: {x_col} vs {y_col}"
            )
            st.altair_chart(chart)
        else:
            st.write("Not enough numerical data for an Altair Chart.")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    generate_visualizations(df)
else:
    st.info("Please upload a CSV file to get started.")
