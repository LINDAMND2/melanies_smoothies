import streamlit as st
import requests
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import pandas as pd

# Establecer el título y la introducción de la aplicación
# Write directly to the app
st.title("🥤Customize Your Smoothie!🥤")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop() 

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
    )

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        # Filter the DataFrame for the selected fruit
        fruit_df = pd_df[pd_df['FRUIT_NAME'] == fruit_chosen]

        # Check if any rows are returned
        if not fruit_df.empty:
            # Access the SEARCH_ON value if it's not NULL
            search_on = fruit_df['SEARCH_ON'].iloc[0]
            st.subheader(fruit_chosen + ' Nutrition Information')
            fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
            fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
        else:
            st.write("No nutrition information available for", fruit_chosen)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """', '"""+name_on_order+ """')"""

    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered, ' + name_on_order, icon="✅")
