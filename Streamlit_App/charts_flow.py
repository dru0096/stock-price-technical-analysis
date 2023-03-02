import nasdaqdatalink as ndl
#my api config file
from ndl_api_config import my_ndl_api_key
#Plotly Graphs
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
#Other
from datetime import datetime
import pickle

def candlestick_plot(df, company_name = None):
        last_90_days=df.last('101D')
        last_90_days.reset_index(inplace=True)

        fig = go.Figure(data=[go.Candlestick(x=last_90_days['Date'],
                        open=last_90_days['Open'],
                        high=last_90_days['High'],
                        low=last_90_days['Low'],
                        close=last_90_days['Close'])])
        fig.update_layout(
            title=company_name,
            yaxis_title='Price (Rs)',
            xaxis_title='Date')
        
       
        url="/Users/devirughani/Desktop/Ironhack/Week_9_Final/Streamlit_App/Plotly_Candlestick_Charts/plotly_html/"+company_name+"_"+datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")+".html"
        fig.write_html(url)
        #fig.to_image(format="png")
        png="/Users/devirughani/Desktop/Ironhack/Week_9_Final/Streamlit_App/Plotly_Candlestick_Charts/email_png/"+company_name+"_"+datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")+".png"
        fig.write_image(png, engine="kaleido")
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("Use 👆🏼 range slider to zoom in on the data")

        st.write('---')

def load_all_data():
        
        #load company info and ndl dataframe store
        with open('Notebooks/pickles/company_info.pkl','rb') as file1:
            company_info=pickle.load(file1)
        with open('Notebooks/pickles/ndl_company_data_dict.pkl','rb') as file2:
            ndl_company_data_dict=pickle.load(file2)
        
        #API config
        ndl.ApiConfig.api_key = my_ndl_api_key #put this isin config file
        
        #Iterate to request data for every company in company info
        for company in company_info:
            name = company[0]
            ticker = company[1]
            print("Fetching data for company", name)
            
            company_data=ndl.get(ticker, limit=90)
            company_data=company_data.iloc[:, :4]
            
            #Save df in ndl company data dictionary
            ndl_company_data_dict[name]['data'] = company_data
            #display(ndl_company_data_dict[name]['data'])
            print()
            
            candlestick_plot(company_data, name)
            #last_90_day_plot=candlestick_plot(company_data, name)
            #st.plotly_chart(last_90_day_plot)
        
        #Save last 90 days of company data in pickle file - can add date so new file every time
        with open('Notebooks/pickles/ndl_company_data_dict.pkl','wb') as file2:
            pickle.dump(ndl_company_data_dict,file2)
        
        
        return ndl_company_data_dict

def load_selected_data(company_info=None):
        
        #API config
        ndl.ApiConfig.api_key = my_ndl_api_key #put this isin config file
        
        #Iterate to request data for every company in company info
        for company in company_info:
            name = company[0]
            ticker = company[1]
            print("Fetching data for company", name)
            
            company_data=ndl.get(ticker, limit=90)
            company_data=company_data.iloc[:, :4]
   
            
            candlestick_plot(company_data, name)
          
   
