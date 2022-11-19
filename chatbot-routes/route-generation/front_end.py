# Copyright (c) 2022 Cohere Inc. and its affiliates.
#
# Licensed under the MIT License (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License in the LICENSE file at the top
# level of this repository.

import streamlit as st
from streamlit import session_state
import pandas as pd
import numpy as np
from pipeline import generate_example_embeddings, search, umap_reduce
import plotly.express as px

if __name__ == "__main__":
  # some formatting
  st.set_page_config(layout="wide")

  # persist state of data for each session
  if not 'df' in session_state:
    data = pd.DataFrame(columns=["Route Name", 'Route Description', 'Deployed'])
    session_state['df'] = data 
  if not 'deployed_routes' in session_state:
    session_state['deployed_routes'] = []
  if not 'routes' in session_state:
    session_state['routes'] = []
  if not 'embeds' in session_state:
    session_state['embeds'] = []
  if not 'texts' in session_state:
    session_state['texts'] = []
  if not 'search_embed' in session_state:
    session_state['search_embed'] = None 

  # title and image
  h1, h2 = st.columns([1, 10])
  h1.image('./assets/profile-white-logo.png', width=100)
  h2.title('Route Generation with Cohere')
  with st.empty():
    st.write('\n#\n#\n')


  # start of containers
  ####################################
  # right hand side
  # this is handling the search function
  ####################################
  st.subheader('Try it out!')
  message = st.text_input('Message')
  if st.button('Send'):
    if not message:
      st.text('please input a message')
    else:
      result, search_embed = search(message, session_state.embeds, session_state.routes, n_comparisons=5)
      session_state['search_embed'] = search_embed
      st.subheader(result)

  # button to insert default values
  defaults = {
    'Route Name': ['Periods', 'Sexuality', 'Sex', 'Feminine Hygiene', 'Dating', 'Body Image', 'Puberty'],
    'Route Description': [
      'This handles questions about female periods and menstrual cycles',
      'This handles questions about sexuality',
      'This handles questions about safe sex, contraception, pregnancy, and consent',
      'This handles questions about feminine hygiene regarding the vagina, hormones, and breasts',
      'This handles questions about starting to date, how to go on dates, and crushes', 
      'This handles questions about body image, body insecurity, and comparing yourself to social media',
      'This handles questions about puberty, acne, teenage girls and their changing bodies, and hair'
      ]
      }
  default_df = pd.DataFrame(defaults)
  default_df['Deployed'] = 'No'
  session_state.df = session_state.df.append(default_df)

  routes_to_run = []
  descriptions_to_run = []
  for i, r in enumerate(list(session_state.df['Route Name'])):
    if not r in session_state['deployed_routes']:
      session_state['deployed_routes'].append(r)
      routes_to_run.append(r)
      descriptions_to_run.append(list(session_state.df['Route Description'])[i])
  if len(descriptions_to_run) > 0:
    r, e, t = generate_example_embeddings(routes_to_run, descriptions_to_run)
    session_state.routes.extend(r)
    session_state.embeds.extend(e)
    session_state.texts.extend(t)
    st.text('All Routes Deployed!')
  else:
    st.text('No routes to deploy')

  if not session_state.df.empty:
    session_state.df['Deployed'] = session_state.df.apply(lambda x: 'Yes' if x['Route Name'] in session_state['deployed_routes'] else 'No', axis=1)