import streamlit as st
import numpy as np
import pandas as pd
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient

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
        self.mode = ''
        self.BUILDING_STANDARDS = {
            "Lite energieffektivt": "Reg", 
            "Middels energieffektivt": "Eff-E", 
            "Veldig energieffektivt": "Vef"
            }
        self.BUILDING_TYPES = {
            "Hus": "Hou",
            "Leilighet": "Apt",
            "Kontor": "Off",
            "Butikk": "Shp",
            "Hotell": "Htl",
            "Barnehage": "Kdg",
            "Skole": "Sch",
            "Universitet": "Uni",
            "Kultur": "CuS",
            "Sykehjem": "Nsh",
            "Sykehus": "Other",
            "Andre": "Other"
        }

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

    def download_input_file(self):
        with open('src/data/default_input_file.xlsx', 'rb') as f:
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
                    self.selected_mode_outdoor_temperature = st.selectbox('Utetemperatur', options = ['', 'Osloklima (NS3031)', 'Last inn fra inndata-mal'])
                elif selected_input_mode == 'Laste inn fra fil':
                    self.mode = 'from_file'
                    self.download_input_file()
                    uploaded_file = st.file_uploader(label = 'Last opp utfylt inndata-mal', accept_multiple_files=False)
                    if uploaded_file:
                        df = pd.read_excel(uploaded_file)
                        df = df.drop(columns=['Indeks'], axis=1)
                        self.df_energy = df
                        
    def get_energy_demand(self):
        if (self.mode == 'profet') and (self.profet_building_area is not None) and (len(self.profet_building_type) > 0) and (len(self.profet_building_standard) > 0) and (len(self.selected_mode_outdoor_temperature) > 0):
            if self.selected_mode_outdoor_temperature == 'Osloklima (NS3031)':
                temperature_array = []
            else:
                #inndata fil
                pass
                
            self.df_energy = self.profet_api(
                building_standard=self.profet_building_standard,
                building_type=self.profet_building_type,
                building_area=self.profet_building_area,
                temperature_array=temperature_array)
            
    def profet_api(self, building_standard, building_type, building_area, temperature_array):
        def get_secret(filename):
            with open(filename) as file:
                secret = file.readline()
            return secret
        oauth = OAuth2Session(client=BackendApplicationClient(client_id="profet_2024"))
        predict = OAuth2Session(
            token=oauth.fetch_token(
                token_url="https://identity.byggforsk.no/connect/token",
                client_id="profet_2024",
                client_secret=get_secret("src/config/profet_secret.txt"),
            )
        )
        selected_standard = self.BUILDING_STANDARDS[building_standard]
        if selected_standard == "Reg":
            regular_area, efficient_area, veryefficient_area = building_area, 0, 0
        if selected_standard == "Eff-E":
            regular_area, efficient_area, veryefficient_area = 0, building_area, 0
        if selected_standard == "Vef":
            regular_area, efficient_area, veryefficient_area = 0, 0, building_area
        # --
        if len(temperature_array) == 0:
            request_data = {
                "StartDate": "2023-01-01", 
                "Areas": {f"{self.BUILDING_TYPES[building_type]}": {"Reg": regular_area, "Eff-E": efficient_area, "Eff-N": 0, "Vef": veryefficient_area}},
                "RetInd": False,  # Boolean, if True, individual profiles for each category and efficiency level are returned
                "Country": "Norway"}
        else:
            request_data = {
            "StartDate": "2023-01-01", 
            "Areas": {f"{self.BUILDING_TYPES[building_type]}": {"Reg": regular_area, "Eff-E": efficient_area, "Eff-N": 0, "Vef": veryefficient_area}},
            "RetInd": False,  # Boolean, if True, individual profiles for each category and efficiency level are returned
            "Country": "Norway",  # Optional, possiblity to get automatic holiday flags from the python holiday library.
            "TimeSeries": {"Tout": temperature_array}}
            
        r = predict.post(
            "https://flexibilitysuite.byggforsk.no/api/Profet", json=request_data
        )
        if r.status_code == 200:
            df = pd.DataFrame.from_dict(r.json())
            df.reset_index(drop=True, inplace=True)
            df_profet = df[["Electric", "DHW", "SpaceHeating"]]
            df_profet.rename(columns={'Electric' : 'Elspesifikt behov', 'DHW' : 'Tappevannsbehov', 'SpaceHeating' : 'Oppvarmingsbehov'}, inplace=True)
            return df_profet
        else:
            raise TypeError("PROFet virker ikke")
                    
                        



            
                    
        

