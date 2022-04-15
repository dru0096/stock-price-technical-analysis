import streamlit as st
import pickle
import imghdr



def hammer_scanner(df, company_name = None, min_wick_ratio=5, min_candle_size=0.4):
    
    df2 = df.copy()
    
    #Adding columns
    df2['Hammer']=" "
 
    for i in range(len(df2)):
        cond1 = df2.iloc[i,[0,3]].min() - df2.iloc[i,2] > (df2.iloc[i,1] - df2.iloc[i,[0,3]].max())*min_wick_ratio
        cond2 = df2.iloc[i,[0,3]].min() > (df2.iloc[i,2]+((df2.iloc[i,1]-df2.iloc[i,2])/2))
        cond3 = df2.iloc[i,2] < df2.iloc[i-10:i,2].min()
        cond4 = abs(df2.iloc[i,0]-df2.iloc[i,3])<((df2.iloc[i,1]-df2.iloc[i,2])*min_candle_size)

        if ( ( cond1 == True )  and ( cond2 == True ) and ( cond3 == True ) and (cond4 == True) ):
                df2.iloc[i,-1] = 1
                st.write(" ")
                st.write("A hammer is formed on", df2.index[i])
                st.write("According to our research on this company's historical data, \
    if you buy at tomorrow's Open, there is: X% probability of making a positive return in 5 days \
    X% probability of making a positive return in 14 days, \
    X% probability of making a positive return in 28 days, GIVEN an expected increase in prices")
                st.write(" ")
                
                
                #if (df2.iloc[i,-1] == 1) and (df2.index[i]== datetime.today().date()):
                    
        else: 
                df2.iloc[i,-1] = 0
    
    return df2

def shooting_star_scanner(df, company_name = None, min_wick_ratio=5, min_candle_size=0.4):
    
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
                st.write(" ")
                st.write("A shooting star is formed on", df2.index[i])
                st.write("According to our research on this company's historical data, \
    if you sell at tomorrow's Open,  there is: X% probability of making a positive return in 5 days \
    X% probability of making a positive return in 14 days,  \
    X% probability of making a positive return in 28 days, GIVEN an expect drop in prices")
                st.write(" ")
              
                #if (df2.iloc[i,-1] == 1) and (df2.index[i]== datetime.today().date()):
                    
                
        else: 
                df2.iloc[i,-1] = 0

    return df2

def pattern_inspector_no_email(data_dictionary, company_name = None, min_wick_ratio=5, min_candle_size=0.25):
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

        company_hammers= df[df['Hammer'] == 1]
        company_shooting_stars=df[df['Shooting Star'] == 1]
        
        if not company_hammers.empty:
            st.dataframe(company_hammers)
        else: st.write("No hammers found")
        st.write(" ")
        
        if not company_shooting_stars.empty:
            st.dataframe(company_shooting_stars)
        else: st.write("No shooting stars found")
