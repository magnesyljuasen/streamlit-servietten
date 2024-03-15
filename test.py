selected_heat_input_mode = st.selectbox('Hvilke timeserier skal lastes opp?', options = ['', 'Romoppvarming og tappevann hver for seg', 'Romoppvarming og tappevann samlet'])
                    if selected_heat_input_mode == 'Romoppvarming og tappevann hver for seg':
                        df_empty = pd.DataFrame({
                            'Romoppvarming' : np.full(8760, None),
                            'Tappevann' : np.full(8760, None),
                            'Elspesifikt' : np.full(8760, None)
                            })
                        custom_column_config = {
                            'Romoppvarming' : st.column_config.NumberColumn(format="%d kW"),
                            'Tappevann' : st.column_config.NumberColumn(format="%d kW"),
                            'Elspesifikt' : st.column_config.NumberColumn(format="%d kW"),
                            }
                    elif selected_heat_input_mode == 'Romoppvarming og tappevann samlet':
                        df_empty = pd.DataFrame({
                            'Samlet varme' : np.full(8760, None),
                            'Elspesifikt' : np.full(8760, None)
                            })
                        custom_column_config = {
                            'Samlet varme' : st.column_config.NumberColumn(format="%d kW"),
                            'Elspesifikt' : st.column_config.NumberColumn(format="%d kW"),
                            }
                    if selected_heat_input_mode != '':
                        st.write('Lim inn data i tabellen under:')
                        st.caption('Tips! Marker første celle i tabellen og Ctrl + V fra Excel. Ha litt tålmodighet da det tar noen sekunder før dataene vises i tabellen.')
                        df = st.data_editor(
                            df_empty,
                            column_config=custom_column_config, 
                            use_container_width=True, 
                            hide_index=True, 
                            num_rows='fixed')
                        st.write(df.columns)