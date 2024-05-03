
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title("Customize your smoothie")
st.write(
    """
    Choose the fruits you want in your custom smoothie.
    """
)

#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response.json())



name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your smoothies will be ', name_on_order)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table('smoothies.public.fruit_options').select(col('fruit_name'), col('SEARCH_ON'))

#st.dataframe(my_dataframe, use_container_width=True)
#st.stop()

pd_df=my_dataframe.to_pandas()
st.dataframe(pd.df)
st.stop()

ingredients_list = st.multiselect('Choose up to 5 ingredients:',
                                 my_dataframe, max_selections=5)

#st.write(ingredient_list)
if ingredients_list:
#and len(ingredient_list) < 6:
  #  st.write(ingredient_list)
 #   st.text(ingredient_list)
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
        fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)
    st.write(ingredients_string)
    my_insert_statement = "insert into SMOOTHIES.PUBLIC.ORDERS(INGREDIENTS, NAME_ON_ORDER) values('"+ingredients_string+"','"+name_on_order+"');"
    st.write(my_insert_statement)

    time_to_insert = st.button('Submit Order')

    if time_to_insert and my_insert_statement and len(ingredients_list) == 5:
        session.sql(my_insert_statement).collect()
        st.success('Your smoothie is ordered!', icon='✅')
