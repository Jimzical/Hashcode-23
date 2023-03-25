import streamlit as st
import plotly.express as px
import pandas

data = pandas.read_csv('archive/df4.csv')


def get_location(df):
    fig = px.density_mapbox(df, lat="Latitude", lon="Longitude", z="AverageCost",hover_name="Area",color_continuous_scale='Turbo', mapbox_style="stamen-terrain",opacity=0.5,height=900,width=900)
    fig.update_layout(mapbox_style="open-street-map", mapbox_zoom=11, mapbox_center_lat = 12.9716, mapbox_center_lon = 77.5946)
    # fig.show(width=9000, height=9000)
    return fig
    
df = pandas.read_csv('archive/df4.csv')
df = df.set_index('ID')


fig = get_location(df)


cuisine_list = ['Afghan', 'African', 'American', 'Andhra', 'Arabian', 'Asian',
       'Assamese', 'Awadhi', 'BBQ', 'Bakery', 'Bar Food', 'Bengali',
       'Beverages', 'Bihari', 'Biryani', 'British', 'Bubble Tea',
       'Burger', 'Burmese', 'Cafe', 'Cantonese', 'Charcoal Chicken',
       'Chettinad', 'Chinese', 'Coffee', 'Continental', 'Cuisine Varies',
       'Desserts', 'European', 'Fast Food', 'Finger Food', 'French',
       'Frozen Yogurt', 'German', 'Goan', 'Gujarati', 'Healthy Food',
       'Hot dogs', 'Hyderabadi', 'Ice Cream', 'Indonesian', 'Iranian',
       'Italian', 'Japanese', 'Juices', 'Kashmiri', 'Kebab', 'Kerala',
       'Konkan', 'Korean', 'Lebanese', 'Lucknowi', 'Maharashtrian',
       'Malaysian', 'Malwani', 'Mangalorean', 'Mediterranean', 'Mexican',
       'Middle Eastern', 'Mishti', 'Mithai', 'Modern Indian', 'Momos',
       'Mughlai', 'Naga', 'Nepalese', 'North Eastern', 'North Indian',
       'Odia', 'Oriental', 'Paan', 'Panini', 'Parsi', 'Pasta', 'Pizza',
       'Portuguese', 'Rajasthani', 'Raw Meats', 'Roast Chicken', 'Rolls',
       'Salad', 'Sandwich', 'Seafood', 'Shake', 'Sindhi', 'Singaporean',
       'South American', 'South Indian', 'Steak', 'Street Food', 'Sushi',
       'Tamil', 'Tea', 'Tex-Mex', 'Thai', 'Tibetan', 'Turkish',
       'Vietnamese', 'Waffle', 'Wraps']


# Define custom CSS
button_style = """
    <style>
        div.stButton > button:first-child {
            padding: 0.75rem 3rem;
            font-size: 50 em;
        }
    </style>
"""

# Add custom CSS to app
st.markdown(button_style, unsafe_allow_html=True)




#create a button in a sidebar
st.sidebar.title('Please Select a type of Recommendation')
st.sidebar.title('Locations for the specific Cuisine')
st.sidebar.write('Cuisines options given')
old_cuisine = cuisine_list[0]
cuisine = st.selectbox('Select a Cuisine', cuisine_list)
# print(change ) everytime a new item selected form selectbox



if st.sidebar.button('Restaurant-Name'):
    st.sidebar.write('Ask restaurant name and suggest Cuisines wise')
if st.sidebar.button('Restaurant-Location'):
    st.sidebar.write('map where the Cuisines is domianant ')
if st.sidebar.button('Cuisines Specific'):
    st.sidebar.write('Cuisines options given')
if st.sidebar.button('Location Specific'):
    
    df_cuisines = df[df['Cuisines'].str.contains(cuisine)]
    fig = get_location(df_cuisines)

    st.plotly_chart(fig)