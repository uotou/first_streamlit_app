import streamlit as sl
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

sl.title('My Parents New Healthy Diner')
sl.header('Breakfast Menu')

sl.text('🥣 Omega 3 & Blueberry Oatmeal')
sl.text('🥗 Kale, spinach & Rocket Smoothie')
sl.text('🐔 Hard-Boiled Free-Range Egg')
sl.text('🥑🍞 Avocado Toast')

sl.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


#import pandas

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = sl.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

sl.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized


sl.header('Fruityvice Fruit Advice!')
try:
    fruit_choice = sl.text_input('What fruit would you like information about?')
    if not fruit_choice:
        sl.error("Please select a fruit to get information")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        sl.dataframe(back_from_function)

except URLError as e:
        sl.error()


sl.header("The fruit load list contains:")
#Snowflake-related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()

# Add a button to load the fruit
if sl.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**sl.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    sl.dataframe(my_data_rows)

sl.stop()

# Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('from streamlit')")
        return 'Thanks for adding ' + add_my_fruit

add_my_fruit = sl.text_input('What fruit would you like to add?', 'jackfruit')
if sl.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**sl.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    sl.text(back_from_function)
