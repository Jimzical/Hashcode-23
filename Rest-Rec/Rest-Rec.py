'''
Created on 25-3-2023 11:00:00
Last modified on 1-4-2023 20:00:00

Change History:
    - Added Documentation
    - Added Comments
    - Cleaned Code
    - Made It More Readable/Modular
'''

import streamlit as st
import plotly.express as px
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


def get_weight(id, df):
    '''
    ---------------------------------
    It returns the weighted value of the restaurant
    ---------------------------------
    ### Parameters:
    id: The ID of the restaurant (int)
    df: The dataframe containing the data (pandas dataframe)
    
    ### Returns:
    The weighted value of the restaurant (float)
    
    '''

    eff_wei_dine = (list(df['weighted_dine']-2.0581212948783363)[id])/(4.894122539591317 - 2.0581212948783363)
    eff_wei_deli = (list(df['weighted_deli']-3.1880727338481383)[id])/(4.452422745897621 - 3.1880727338481383)
    return eff_wei_dine * eff_wei_deli

@st.cache_data
def recommend_rest(str,df):
    '''
    ---------------------------------
    It returns the recommended restaurants
    ---------------------------------
    ### Parameters:
    str: The name of the restaurant (string)
    df: The dataframe containing the data (pandas dataframe)

    ### Returns:
    The recommended restaurants (list)
    
    '''

    for i in range(len(df['Name'])):
        if str == list(df['Name'])[i]:
            id = i

    cv=CountVectorizer(max_features=110)
    vectors=cv.fit_transform(df['Cuisines']).toarray()

    similarity=cosine_similarity(vectors)
    listt = sorted(list(enumerate(similarity[id])),reverse=True,key=lambda x:x[1])
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
        recommended_restaurants.append([list(df['Name'])[id], df['URL'][id], df['PhoneNumber'][id], df['Area'][id], df['AverageCost'][id],df['Cuisines'][id]])

    return recommended_restaurants


@st.cache_data
def get_location(df):
    '''
    ---------------------------------
    It returns the list of locations
    ---------------------------------
    ### Parameters:
    df: The dataframe containing the data (pandas dataframe)

    ### Returns:
    The list of locations (list)
    
    '''
    fig = px.density_mapbox(df, lat="Latitude", lon="Longitude", z="AverageCost",hover_name="Area",color_continuous_scale='Turbo', mapbox_style="stamen-terrain",opacity=0.5,height=900,width=900)
    fig.update_layout(mapbox_style="open-street-map", mapbox_zoom=11, mapbox_center_lat = 12.9716, mapbox_center_lon = 77.5946)
    return fig

@st.cache_data
def recommend_loc(str,df):
    '''
    ---------------------------------
    It returns the recommended restaurants
    ---------------------------------
    ### Parameters:
    str: The name of the restaurant (string)
    df: The dataframe containing the data (pandas dataframe)

    ### Returns:

    The recommended restaurants (list)
    
    '''
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
        recommended_restaurants.append([list(df['Name'])[id],df['URL'][id],df['PhoneNumber'][id],df['Area'][id],df['AverageCost'][id],df['Cuisines'][id]])
    return recommended_restaurants

def LoadData(location = 'CleanZomato.csv'):  
    '''
    ---------------------------------
    It returns the dataframe containing the data
    ---------------------------------
    ### Parameters:
    location: The location of the csv file (string)
        
    ### Returns:
    The dataframe containing the data (pandas dataframe)
    '''  
    df = pd.read_csv(location)
    df = df.set_index('ID')
    return df

def DataListGenerator(df):
    '''
    ---------------------------------
    It returns the list of restaurants
    ---------------------------------
    ### Parameters:
    df: The dataframe containing the data (pandas dataframe)

    ### Returns:
    cuisine_list: The list of cuisines (list)
    area_list: The list of locations (list)
    rest_list: The list of restaurants (list)
    '''

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
    return cuisine_list, area_list, rest_list
    # Define custom CSS

def DynamicButton(df,ButtonDesc = 'Recommendations',ButtonFuntion = None,ButtonData = ['Name','URL','PhoneNumber','Area','AverageCost','Cuisines'],FunctionArgs = None):
    
    st.sidebar.markdown(f"# {ButtonDesc}")
    output = ButtonFuntion(FunctionArgs,df)
    out_df = pd.DataFrame(output,columns=ButtonData)
    tab = st.tabs(list(out_df['Name'].values))
    for i in range(len(out_df.columns)):
        with tab[i]:
            st.markdown(f"Website For :  [{out_df['Name'][i]}]({out_df['URL'][i]})")    
            st.write(f"Area : {out_df['Area'][i]}")
            st.write(f"Average Cost : {out_df['AverageCost'][i]}")
            st.write(f"Cuisines : {out_df['Cuisines'][i]}")
            st.write("------------")


def BuildGUI(df):
    '''
    ---------------------------------
    It builds the GUI
    ---------------------------------
    ### Parameters:
    df: The dataframe containing the data (pandas dataframe)

    ### Returns:
    None
    '''

    # Read data
    cuisine_list, area_list, rest_list = DataListGenerator(df)

    st.title("Restaurant Recommendation System")
    st.write("This is a simple recommendation system for restaurant")
    
    # Add custom CSS to app
    button_style = """
        <style>
            div.stButton > button:first-child {
                padding: 0.75rem 3rem;
                font-size: 50 em;
            }
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)


    #create a button in a sidebar
    st.sidebar.markdown('# Please Select a type of Recommendation')
    st.sidebar.markdown('<b>Cuisines options given</b>', unsafe_allow_html=True)
    cuisine = st.selectbox('Select a Cuisine', cuisine_list)
    area = st.selectbox('Select Area', area_list)
    rest = st.selectbox('Select Restaurant', rest_list)


    if st.sidebar.button('Restaurant-Name'):
        DynamicButton(df,ButtonDesc = 'Ask restaurant name and suggest Cuisines wise',ButtonFuntion = recommend_rest,ButtonData = ['Name','URL','PhoneNumber','Area','AverageCost','Cuisines'],FunctionArgs = rest)
        
    if st.sidebar.button('Restaurant-Location'):
        st.sidebar.markdown('## Map indicating where the Cuisines is domianant ')
        df_cuisines = df[df['Cuisines'].str.contains(cuisine)]
        fig = get_location(df_cuisines)
        st.plotly_chart(fig)
        
    if st.sidebar.button('Location Specific'):
        DynamicButton(df,ButtonDesc = 'Ask Location and suggest Cuisines wise',ButtonFuntion = recommend_loc,ButtonData = ['Name','URL','PhoneNumber','Area','AverageCost','Cuisines'],FunctionArgs = area)
def main():
    df = LoadData()
    BuildGUI(df)

if __name__ == '__main__':
    main()
