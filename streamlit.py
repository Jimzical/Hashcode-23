import streamlit as st
import plotly.express as px
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

data = pd.read_csv('CleanZomato2.csv')

def get_weight(id, df):
    eff_wei_dine = (list(df['weighted_dine']-2.0581212948783363)[id])/(4.894122539591317 - 2.0581212948783363)
    eff_wei_deli = (list(df['weighted_deli']-3.1880727338481383)[id])/(4.452422745897621 - 3.1880727338481383)
    return eff_wei_dine * eff_wei_deli

def recommend_rest(str):
    
    df=pd.read_csv('CleanZomato2.csv')

    for i in range(len(df['Name'])):
        if str == list(df['Name'])[i]:
            id = i

    cv=CountVectorizer(max_features=110)
    vectors=cv.fit_transform(df['Cuisines']).toarray()

    similarity=cosine_similarity(vectors)
    listt = sorted(list(enumerate(similarity[i])),reverse=True,key=lambda x:x[1])
    for i in range(len(listt)):
        listt[i] = list(listt[i])

    new_listt = []

    temp = listt[5]
    if temp[1] < 0.9:
        new_listt.append(temp)
    else:
        for i in range(len(listt)):
            temp = listt[i]
            if temp[1] > 0.9:
                new_listt.append(temp)

    for i in range(len(new_listt)):
        temp = new_listt[i]
        temp[1] = float(temp[1]) * get_weight(temp[0], df)

    sorted_new_listt = sorted(new_listt, key=lambda x:x[1],reverse=True)[0:6]

    recommended_restaurants=[]
    for lists in sorted_new_listt:
        id = lists[0]
        recommended_restaurants.append(list(df['Name'])[id])

    return recommended_restaurants

def get_location(df):
    fig = px.density_mapbox(df, lat="Latitude", lon="Longitude", z="AverageCost",hover_name="Area",color_continuous_scale='Turbo', mapbox_style="stamen-terrain",opacity=0.5,height=900,width=900)
    fig.update_layout(mapbox_style="open-street-map", mapbox_zoom=11, mapbox_center_lat = 12.9716, mapbox_center_lon = 77.5946)
    # fig.show(width=9000, height=9000)
    return fig

def recommend_loc(str):
    same_loc = []
    for i in range(len(list(df['Area']))):
        if str == list(df['Area'])[i]:
            same_loc.append(i)
    for i in range(len(same_loc)):
        id = same_loc[i]
        same_loc[i] = [ id, list(df['weighted_dine'])[id] + list(df['weighted_deli'])[id] ]
    sorted_list = sorted(same_loc, key=lambda x:x[1],reverse=True)[0:6]
    recommended_restaurants=[]
    for lists in sorted_list:
        id = lists[0]
        recommended_restaurants.append(list(df['Name'])[id])
    return recommended_restaurants
    
df = pd.read_csv('CleanZomato2.csv')
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
area_list = list(df['Area'].unique())
rest_list = list(df['Name'].unique())

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
area = st.selectbox('Select Area', area_list)
rest = st.selectbox('Select Restaurant', rest_list)
# print(rest)
# print(change ) everytime a new item selected form selectbox


if st.sidebar.button('Restaurant-Name'):
    st.sidebar.write('Ask restaurant name and suggest Cuisines wise')
    output = recommend_rest(rest)
    for o in output:
        st.markdown("- "+o)
if st.sidebar.button('Restaurant-Location'):
    st.sidebar.write('map where the Cuisines is domianant ')
    df_cuisines = df[df['Cuisines'].str.contains(cuisine)]
    fig = get_location(df_cuisines)
    st.plotly_chart(fig)
if st.sidebar.button('Cuisines Specific'):
    st.sidebar.write('Cuisines options given')
if st.sidebar.button('Location Specific'):
    output = recommend_loc(area)
    st.write(output)
