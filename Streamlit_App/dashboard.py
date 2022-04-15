###############################
# This program lets you       #
# - Create a dashboard        #
# - Every dashboard page is  #
# created in a separate file  #  
###############################

# Python libraries
import pandas as pd
import streamlit as st
from PIL import Image
import requests
import json
import datetime as dt

#Streamlit libraries
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu

# User module files
from charts_flow import *
from  pattern_inspector_and_alerts import *
from  pattern_inspector_no_email_alert import *

with open('Notebooks/pickles/company_info.pkl','rb') as file1:
    company_info=pickle.load(file1)

with open('Notebooks/pickles/ndl_company_data_dict.pkl','rb') as file2:
 ndl_company_data_dict=pickle.load(file2)



# Animations

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
      return None
    return r.json()

lottie_data_pattern = load_lottieurl('https://assets9.lottiefiles.com/private_files/lf30_70ooxacp.json')
lottie_question = load_lottieurl('https://assets1.lottiefiles.com/packages/lf20_HIDvWF.json')
lottie_btc = load_lottieurl('https://assets1.lottiefiles.com/packages/lf20_SwvPOd.json')



def main():
  
    #############  
    # Main page #
    #############   

    st.set_page_config(page_title="my project", page_icon=":mag:", layout="wide")

    
    #options = ['Home','My Portfolio','Pattern Inspector']
    #choice = st.sidebar.selectbox("Menu",options, key = '1')
    
    #if ( choice == 'Home' ):

    selected = option_menu(
      menu_title=None,
      options=['Home','My Portfolio','Pattern Inspector', 'Stop'],
      icons=['house', 'graph-up','graph-up','stop-circle'],
      menu_icon='list',
      default_index=0,
      orientation='horizontal',
      styles={
        "container": {"padding": "0!important", "background-color": "#f0f2f6"},
        "icon": {"color": "white", "font-size": "20px"}, 
        "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#1048C3"},
      }
    )


    if ( selected == 'Home' ):




      st.markdown("<h1 style='text-align: center; color: black;'>Welcome to isPYpatterns 🔎 </h1>", unsafe_allow_html=True)
      now= dt.datetime.now().strftime("%Y_%m_%d-%I:%M")
      st.markdown(f"<h6 style='text-align: center; color: black;'> Today's Date is: {now} </h6>", unsafe_allow_html=True)
  

      padding = 20
      st.markdown(f""" <style>
        .reportview-container .main .block-container{{
            padding-top: {padding}rem;
            padding-right: {padding}rem;
            padding-left: {padding}rem;
            padding-bottom: {padding}rem;
        }} </style> """, unsafe_allow_html=True)

      #st.write('---')
    
      c1 = st.container()
      with c1:
        col1, col2, col3 = st.columns([1,2,1])

        with col1:
          st_lottie(lottie_data_pattern , height=200, key='data_pattern_1')
        with col2:
          st.header('Make consistent profits while buying and selling your stocks:')
          st.write('👉🏼 Based on decades of historical price data')
          st.write('👉🏼 Irrespective of which company')
          st.write('👉🏼 Automated daily alerts to save you time')
        with col3:
          st_lottie(lottie_data_pattern , height=200, key='data_pattern')
        

      pass
      


    elif ( selected == 'My Portfolio' ):
      st.markdown("<h1 style='text-align: center; color: black;'>Last 90 Days Price Movements</h1>", unsafe_allow_html=True)
      company_list = company_info
      
      select_companies = st.sidebar.multiselect('Select which companies to view:',company_list) 
      click1=st.button('Load Selected Data')
      

      if click1:
        load_selected_data(company_info=select_companies)


      
      #load_all_data()



      pass
    
    elif (selected == 'Pattern Inspector'):
      #Patten inspector which returns datframes and sends emails
      st.markdown("<h1 style='text-align: center; color: black;'>Daily Pattern Inspector</h1>", unsafe_allow_html=True)
      
      st.header('Do you want to receive daily alerts and data to your inbox?')

      q1=st.radio ('Answer:',['Yes', 'No'] )
      
      if q1 =='Yes':
        user_email = st.text_input("Please enter a valid email address:", type="default", placeholder='myemail@gmail.com' )

        if (user_email):
          pattern_inspector(ndl_company_data_dict, email_to=user_email)

      if q1 =='No':
          pattern_inspector(ndl_company_data_dict)

      pass

    else:
      st.stop()
      
    
main()