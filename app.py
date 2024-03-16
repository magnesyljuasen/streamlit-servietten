import streamlit as st
import numpy as np
from src.scripts import utilities, figures

if __name__ == "__main__":
    utilities.set_page_configuration() # set page configuration
    utilities.set_css(filepath_css = 'src/styles/main.css') # set css style
    utilities.set_sidebar_logo(filepath_logo = 'src/img/av-logo.png') # set logo
    utilities.set_page_title(text = 'Tidligfasedimensjonering') # set page title
    #####
    input_object = utilities.Input() # initalize input object
    input_object.get_input_resolution() # set resolution input mode; hourly, monthly, yearly
    input_object.get_building_input()
    input_object.get_energy_demand()
    #####
    c1, c2, c3 = st.columns(3)
    ymin = input_object.df_energy.min().min()*1.5
    ymax = input_object.df_energy.max().max()*1.5
    with c1:
        figures.plot_hourly_series(
            input_object.df_energy['Oppvarmingsbehov'],
            'Oppvarmingsbehov',
            ymin=ymin,
            ymax=ymax,
            height=150
            )
    with c2:
        figures.plot_hourly_series(
            input_object.df_energy['Tappevannsbehov'],
            'Tappevannsbehov',
            ymin=ymin,
            ymax=ymax,
            height=150
            )
    with c3:
        figures.plot_hourly_series(
            input_object.df_energy['Elspesifikt behov'],
            'Elspesifikt behov',
            ymin=ymin,
            ymax=ymax,
            height=150
            )
    c1, c2 = st.columns([2,1])
    with c1:
        figures.plot_hourly_series(
            input_object.df_energy['Oppvarmingsbehov'] + input_object.df_energy['Tappevannsbehov'],
            'Totalt varmebehov',
            height=150
            #linemode=True,
            #xtick_datemode=False,
            )

