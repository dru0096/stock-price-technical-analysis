import smtplib
from smtplib import SMTP
from email.message import EmailMessage
from email_config_gmail import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import glob
import os
import streamlit as st
import pickle
import imghdr


def hammer_email_alert(company_name=None, email_to='devi.rughani@gmail.com'):
    if ( not (email_to is None)):
        #Server
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465) 
        smtp_server.ehlo()
        smtp_server.login(mail_username, password)

        #Set up email content
        email_text = "According to our research on this company's historical data, \
                    if you buy at tomorrow's Open, there is more than 50% probability of making a positive return at the 5, 14 and 28 day close GIVEN an expected increase in prices"

        msg=EmailMessage()
        msg.set_content(email_text)
     
        
        #get date with os and cast into string with datetime
        

        file_options = glob.glob("/Users/devirughani/Desktop/Ironhack/Week_9_Final/Streamlit_App/Plotly_Candlestick_Charts/email_png/"+company_name+"*.png")
        latest_file = max( file_options, key=os.path.getctime)
       
        with open (latest_file, 'rb') as f:
            file_data=f.read()
            file_type=imghdr.what(f.name)
            file_name= company_name+"_last_90_days_prices.png"
        
        msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)

        
        msg['From'] = 'devi.rughani@gmail.com'
        #msg['To'] = email_to
        msg['To']= 'devi.rughani@gmail.com'
        msg['Subject'] = 'Turning point in Stock Prices for ' + company_name + '!'

        #Send email
        smtp_server.send_message(msg)
        smtp_server.quit()


def shooting_star_email_alert(company_name=None, email_to='devi.rughani@gmail.com'):

    if ( not (email_to is None)) :

        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465) 
        smtp_server.ehlo()
        smtp_server.login(mail_username, password)

        #Set up email
        email_text = "According to our research on this company's historical data, \
                    if you sell at tomorrow's Open, there is more than 50% probability of making a positive return at the 5, 14 and 28 day close GIVEN an expected drop in prices"

        msg=EmailMessage()
        msg.set_content(email_text)

        
        file_options = glob.glob("/Users/devirughani/Desktop/Ironhack/Week_9_Final/Streamlit_App/Plotly_Candlestick_Charts/email_png/"+company_name+"*.png")
        latest_file = max( file_options, key=os.path.getctime)
     
        with open (latest_file, 'rb') as f:
            file_data=f.read()
            file_type=imghdr.what(f.name)
            file_name= company_name+"_last_90_days_prices.png"
        
        

        msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)

        msg['From'] = 'devi.rughani@gmail.com'
        #msg['To'] = email_to
        msg['To'] = 'devi.rughani@gmail.com'
        msg['Subject'] = 'Turning point in Stock Prices for ' + company_name + '!'

        #Send email
        smtp_server.send_message(msg)
        smtp_server.quit()




def hammer_scanner(df, company_name = None, email_to='devi.rughani@gmail.com', min_wick_ratio=5, min_candle_size=0.4):
    
    df2 = df.copy()
    
    df2['Hammer']=" "
 
    for i in range(len(df2)):
        cond1 = df2.iloc[i,[0,3]].min() - df2.iloc[i,2] > (df2.iloc[i,1] - df2.iloc[i,[0,3]].max())*min_wick_ratio
        cond2 = df2.iloc[i,[0,3]].min() > (df2.iloc[i,2]+((df2.iloc[i,1]-df2.iloc[i,2])/2))
        cond3 = df2.iloc[i,2] < df2.iloc[i-10:i,2].min()
        cond4 = abs(df2.iloc[i,0]-df2.iloc[i,3])<((df2.iloc[i,1]-df2.iloc[i,2])*min_candle_size)

        if ( ( cond1 == True )  and ( cond2 == True ) and ( cond3 == True ) and (cond4 == True) ):
                df2.iloc[i,-1] = 1
                st.write("Hammers")

                company_hammers= df2[df2['Hammer'] == 1]
                if not company_hammers.empty:
                    st.dataframe(company_hammers)
                    st.write("According to our research on this company's historical data, \
                    if you buy at tomorrow's Open, there is more than 50% probability of making a positive return at the 5, 14 and 28 day close GIVEN an expected increase in prices")
                    st.write(" ")

                if (email_to is not None):
                    hammer_email_alert(company_name, email_to)
                
                #if (df2.iloc[i,-1] == 1) and (df2.index[i]== datetime.today().date()):
                    
        else: 
                df2.iloc[i,-1] = 0
        
    return df2

def shooting_star_scanner(df, company_name = None, email_to='devi.rughani@gmail.com', min_wick_ratio=5, min_candle_size=0.4):
    
    df2 = df.copy()
    
    df2['Shooting Star']=" "
        
    for i in range(len(df2)):
        cond1 = ( df2.iloc[i,1] > df2.iloc[i-10:i,1].max() )
        x =  df2.iloc[i,1] - df2.iloc[i,[0,3]].max() 
        y = ( df2.iloc[i,[0,3]].min() - df2.iloc[i,2] ) * min_wick_ratio 
        cond2 = ( x > y ) 
        cond3 =  abs( df2.iloc[i,0] - df2.iloc[i,3] ) <  ( df2.iloc[i,1] - df2.iloc[i,2] ) * min_candle_size 

        if ( ( cond1 == True )  and ( cond2 == True ) and ( cond3 == True ) ):
                df2.iloc[i,-1] = 1
                st.write("Shooting Stars")
                company_shooting_stars = df2[df2['Shooting Star'] == 1]  

                if not company_shooting_stars.empty:
                    st.write( "According to our research on this company's historical data, \
                    if you sell at tomorrow's Open, there is more than 50% probability of making a positive return at the 5, 14 and 28 day close GIVEN an expected drop in prices")
                    st.dataframe(company_shooting_stars)
                     

                if ( email_to is not None ):
                    shooting_star_email_alert(company_name, email_to)
                #if (df2.iloc[i,-1] == 1) and (df2.index[i]== datetime.today().date()):
        else: 
                df2.iloc[i,-1] = 0
                #st.write("No shooting stars found")  

                

    return df2


def pattern_inspector(data_dictionary, email_to='devi.rughani@gmail.com', company_name=None, min_wick_ratio=5, min_candle_size=0.25):
    #load company info
    with open('Notebooks/pickles/company_info.pkl','rb') as file1:
        company_info=pickle.load(file1)
    
    with open('Notebooks/pickles/ndl_company_data_dict.pkl','rb') as file2:
        ndl_company_data_dict=pickle.load(file2)
        
    for company in company_info:
        name = company[0]
        ticker = company[1]

        st.write(" ")
        st.header("Checking for new pattern formation for "+name+"...🔎 ")
        st.write(" ")

        df = ndl_company_data_dict[name]['data']
       
        df = hammer_scanner(df, name, min_wick_ratio=min_wick_ratio, min_candle_size=min_candle_size)
        df = shooting_star_scanner(df, name, min_wick_ratio=min_wick_ratio, min_candle_size=min_candle_size)

        #company_hammers= df[df['Hammer'] == 1]
        #company_shooting_stars=df[df['Shooting Star'] == 1]
        
        #if not company_hammers.empty:
         #   st.write("A hammer is formed on", df.index[i])
          #  st.dataframe(company_hammers)
        #else: st.write("No hammers found")
        #st.write(" ")
        
        #if not company_shooting_stars.empty:
         #   st.write("A shooting star is formed on", df.index[i])
          #  st.dataframe(company_shooting_stars)
        #else: st.write("No shooting stars found")
