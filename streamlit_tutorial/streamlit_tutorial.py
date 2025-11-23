## streamlit run streamlit_tutorial/streamlit_tutorial.py
# https://medium.com/@verinamk/streamlit-for-beginners-build-your-first-dashboard-58b764a62a2d
import streamlit as st
from PIL import Image
import seaborn as sns
import plotly.express as px

# streamlit page config
st.set_page_config(
    page_title="Iris Dashboard",  # the page title shown in the browser tab
    page_icon=":bar_chart:",  # the page favicon shown in the browser tab
    layout="wide",  # page layout : use the entire screen
)
# add page title
st.title("My Iris Dataset Dashboard :bar_chart::hibiscus:")

# about dataset section
# expander to show/hide the 'about dataset' section
with st.expander('About Iris'):
    st.header("About the Iris Dataset")
    st.write("""The Iris dataset consists of 150 samples of iris flowers from three different species:
            Setosa, Versicolor, and Virginica. Each sample includes four features: sepal length,
            sepal width, petal length, and petal width. It was introduced by the British biologist
            and statistician Ronald Fisher in 1936 as an example of discriminant analysis.""")
    # iris_image = Image.open("imgs/iris_species.png")
    # st.image(iris_image)


# load data
df = sns.load_dataset('iris')
# get column and species names
attributes = df.columns[:-1].tolist()
species = df['species'].unique().tolist()

# # basic statistics
# st.header("Basic Statistics")
# st.dataframe(df.describe(), use_container_width=True)

# create sidebar with filtering options
with st.sidebar:  
    # add header  
    st.header("Filters", divider=True)
    # dropdown to select attributes
    selected_attribute = st.selectbox("Attribute: ", attributes, index=0)
    # multiselect to select species
    selected_species = st.multiselect("Species: ", species, placeholder="Filter by species")

# handle filter selections
if not selected_species:
    selected_species = species
    
filtered_df = df[df['species'].isin(selected_species)]
# basic statistics
st.header("Basic Statistics")
st.dataframe(filtered_df.describe(), use_container_width=True)

# plotly graphs:
st.header("Data Visualization")
fig = px.scatter_matrix(df, dimensions=attributes, color="species")
st.plotly_chart(fig)

# histogram
def create_histogram(df, attribute):
    fig = px.histogram(df, x=attribute,
                            color="species",
                            marginal="box",
                            barmode="overlay")
    fig.update_traces(marker=dict(line=dict(
                                        width=1,
                                        color="rgba(100,100,100,0.5)")
                                        ))
    fig.update_layout(title=f"Histogram of {attribute}", hovermode="x unified")
    return fig

# violin plot
def create_violin_plot(df, attribute, points='all'):
    fig = px.violin(df, x="species", y=attribute,
                            color="species",
                            box=True,
                            points=points)
    fig.update_layout(title=f"Violin Plot of {attribute}")
    return fig

# plot by selected attribute
st.subheader("Single Attribute Distribution")
# # Histogram
# hist_fig = create_histogram(filtered_df, selected_attribute)
# st.plotly_chart(hist_fig, use_container_width=True)
# # Violin Plot
# # violin_fig = create_violin_plot(filtered_df, selected_attribute, points="all")
# # st.plotly_chart(violin_fig, use_container_width=True)

# show_points = st.checkbox("Show individual points", value=True)
# # Violin Plot
# violin_fig = create_violin_plot(filtered_df, selected_attribute, points="all" if show_points else False)
# st.plotly_chart(violin_fig, use_container_width=True)

# columns to add 2 plots side by side
col1, col2 = st.columns(2)
# Histogram
with col1:
    hist_fig = create_histogram(filtered_df, selected_attribute)
    st.plotly_chart(hist_fig, use_container_width=True)
# Violin Plot
with col2:
    show_points = st.checkbox("Show individual points", value=True)
    violin_fig = create_violin_plot(filtered_df, selected_attribute, points="all" if show_points else False)
    st.plotly_chart(violin_fig, use_container_width=True)