# Import python packages
import streamlit as st

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be: ', name_on_order)

# Create Snowflake session
cnx = st.connection("snowflake")
session = cnx.session()

# Get fruit options
my_dataframe = session.table("smoothies.public.fruit_options").select("FRUIT_NAME")

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe.collect(),
    max_selections=5
)

# Submit button
time_to_insert = st.button('Submit Order', type="primary")

if time_to_insert:
    if ingredients_list:

        ingredients_string = ', '.join(ingredients_list)

        my_insert_stmt = f"""
            INSERT INTO smoothies.public.orders (ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """

        st.write(my_insert_stmt)

        session.sql(my_insert_stmt).collect()

        st.success(f'Your Smoothie is ordered! 🥤 Name: **{name_on_order}**')

    else:
        st.warning("Please select at least one ingredient before submitting.")
