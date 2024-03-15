import streamlit as st
from src.scripts import utilities

if __name__ == "__main__":
    utilities.set_page_configuration() # set page configuration
    utilities.set_css(filepath_css = 'src/scripts/styles/main.css') # set css style
    utilities.set_sidebar_logo(filepath_logo = 'src/scripts/img/av-logo.png') # set logo
    utilities.set_page_title(text = 'Tidligfasedimensjonering') # set page title
    #####
    input_object = utilities.Input() # initalize input object
    input_object.get_input_resolution() # set resolution input mode; hourly, monthly, yearly
    input_object.get_building_input()

    try:
        df = input_object.df_hourly_energy_data
    except:
        pass
    c1, c2, c3 = st.columns(3)
    with c1:
        try:
            st.line_chart(df)
        except:
            pass

