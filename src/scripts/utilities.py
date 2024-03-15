import streamlit as st
import numpy as np
import pandas as pd

def set_page_configuration():
    st.set_page_config(
        page_title="AutoGrunnvarme",
        page_icon="",
        layout="wide",
        initial_sidebar_state="expanded",
    )

def set_css(filepath_css):
    with open(filepath_css) as f:
        st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

def set_sidebar_logo(filepath_logo):
    with st.sidebar:
        st.image(filepath_logo)

def set_page_title(text):
    st.title(text)

class Input:
    def __init__(self):
        pass

    def get_input_resolution(self):
        with st.sidebar:
            selected_input_mode = st.selectbox('Velg oppløsning på inndata', options = ['', 'Timer', 'Måneder', 'Årlig'])
            if selected_input_mode == 'Timer':
                self.input_resolution = 'hourly'
            elif selected_input_mode == 'Måneder':
                self.input_resolution = 'monthly'
            elif selected_input_mode == 'Årlig':
                self.input_resolution = 'yearly'
            else:
                self.input_resolution = None

    def _get_default_input_file(self):
        with open('src/scripts/data/default_input_file.xlsx', 'rb') as f:
            data = f.read()
        st.download_button(
            label='Last ned inndata-mal',
            data=data,
            file_name='Inndata.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    def get_building_input(self):
        with st.sidebar:
            if self.input_resolution == 'hourly':
                selected_input_mode = st.radio("?", options = ['Estimere med PROFet', 'Laste inn fra fil'], horizontal = True, label_visibility='collapsed')
                if selected_input_mode == 'Estimere med PROFet':
                    self.mode = 'profet'
                    self.profet_building_area = st.number_input('Oppgi bygningsareal [m²]', value = None, format = '%g', step = 1)
                    self.profet_building_type = st.selectbox('Velg bygningstype', options = ['', 'Hus', 'Leilighet', 'Kontor', 'Butikk', 'Hotell', 'Barnehage', 'Skole', 'Universitet', 'Kultur', 'Sykehjem', 'Sykehus', 'Andre'])
                    self.profet_building_standard = st.selectbox('Velg bygningsstandard', options = ['', 'Lite energieffektivt', 'Middels energieffektivt', 'Veldig energieffektivt'])
                elif selected_input_mode == 'Laste inn fra fil':
                    self._get_default_input_file()
                    uploaded_file = st.file_uploader(label = 'Last opp utfylt inndata-mal', accept_multiple_files=False, )
                    if uploaded_file:
                        df = pd.read_excel(uploaded_file)
                        df = df.drop(columns=['Indeks'], axis=1)
                        self.df_hourly_energy_data = df
                    
                        



            
                    
        

