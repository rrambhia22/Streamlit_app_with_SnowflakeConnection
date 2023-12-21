import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title("My Parents New Healthy Diner")
streamlit.header("Breakfast Favorites")
streamlit.text("🥣 Omega 3 & Blueberry Oatmeal")
streamlit.text("🥗 Kale, Spinach & Rocket Smoothie")
streamlit.text("🐔 Hard-Bolied Free-Range Egg")
streamlit.text("🥑🍞 Avacoda Toast")
streamlit.header("🍌🥭 Build Your Own Fruit Smoothie 🥝🍇")

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index("Fruit")
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  # just writes the data to the screen
  # streamlit.text(fruityvice_response.json())  
  # take the json version of the response and normalize it
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  
# New Section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    # output it on the screen as a table
    # streamlit.dataframe(fruityvice_normalized)
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
    
except URLError as e:
  streamlit.error()
  
# streamlit.write('The user entered ', fruit_choice)

streamlit.header("The fruit load list contains:")
# Snowflake-related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()

# Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)

streamlit.stop()

fruit_choice2 = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thanks for adding', fruit_choice2)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")
