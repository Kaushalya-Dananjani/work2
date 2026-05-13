# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be: ', name_on_order)

session = get_active_session()

# Get fruit options
my_dataframe = session.table("smoothies.public.fruit_options").select("FRUIT_NAME")

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

# Submit button
time_to_insert = st.button('Submit Order', type="primary")

if time_to_insert:
    if ingredients_list:
        # Build ingredients string (as shown in the image)
        ingredients_string = ''
        for fruit_chosen in ingredients_list:
            ingredients_string += fruit_chosen + ', '
        
        # Remove trailing comma and space
        ingredients_string = ingredients_string.strip(', ')
        
        # Build the INSERT statement (including name_on_order)
        my_insert_stmt = f"""
            INSERT INTO smoothies.public.orders (ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """
        
        # Optional: Show the SQL for debugging (as suggested in the image)
        st.write(my_insert_stmt)
        
        # Execute the insert
        session.sql(my_insert_stmt).collect()
        
        st.success(f'Your Smoothie is ordered! 🥤\nName: **{name_on_order}**', icon="✅")
        
    else:
        st.warning("Please select at least one ingredient before submitting.")