import streamlit as st
import snowflake.connector
import requests
import pandas
from urllib.error import URLError

st.title('My parents New Healty Diner')

st.header('Breakfast Menu')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

#=============================================
st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
st.dataframe(fruits_to_show)
#=============================================
def get_fruitvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  # st.text(fruityvice_response)
  # st.text(fruityvice_response.json()) # Writting data to the screen
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
    
# Getting reponse from fruityvice.com
st.header("Fruityvice Fruit Advice!")

try:
  fruit_choice = st.text_input('What fruit would you like information about?')
  # st.write('The user entered ', fruit_choice)

  if not fruit_choice:
    st.error("Please Select a fruit to get information")
  else:
    back_from_function = get_fruitvice_choice(fruityvice_normalized)
    st.dataframe(back_from_function)

except URLError as e:
  st.error()

# Adding a stop point
st.stop()

#=============================================
# Snowflake Connection
st.header("The Fruit Load List Contains:")
# Snowflake-related function
def get_fruit_load_list():
#   my_cur = my_cnx.cursor()
  with mycnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    # my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
    return my_cur.fetchall()

if st.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  st.dataframe(my_data_rows)

st.dataframe(my_data_rows)
add_my_fruit = st.text_input('What fruit would you like to add?')
if (add_my_fruit):
  my_cur.execute("insert into fruit_load_list values('" + add_my_fruit + "')")
  st.text('Thanks for adding ' + add_my_fruit)
