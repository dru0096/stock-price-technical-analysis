def up_or_down(x):
    if x > 0:
        return 'Up'
    elif x < 0:
        return 'Down'
    else:" "

def candlestick_plot(df):
    last_90_days=df.last('90D')
    last_90_days.reset_index(inplace=True)

    fig = go.Figure(data=[go.Candlestick(x=last_90_days['Date'],
                    open=last_90_days['Open'],
                    high=last_90_days['High'],
                    low=last_90_days['Low'],
                    close=last_90_days['Close'])])
    fig.update_layout(
        title='Last 90 days price movements',
        yaxis_title='Kaveri Seeds Stock Price (Rs)',
        xaxis_title='Date')

    fig.show()










def shooting_star_scanner(df, min_wick_ratio=5, min_candle_size=0.4):
    
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
                print("A shooting star is formed on", df2.index[i])
                print(" ")
                
                if (df2.iloc[i,-1] == 1) and (df2.index[i]== datetime.today().date()):
                    shooting_star_email_alert()
                
        else: 
                df2.iloc[i,-1] = 0




def hammer_scanner(df, min_wick_ratio=5, min_candle_size=0.4):
    
    df2 = df.copy()
    
    #Adding columns
    df2['Hammer']=" "
 
    #df2['Return % 5 days after']= " "
    #df2['Return % 14 days after']= " "
    #df2['Return % 28 days after']= " "
    
    for i in range(len(df2)):
        cond1 = df2.iloc[i,[0,3]].min() - df2.iloc[i,2] > (df2.iloc[i,1] - df2.iloc[i,[0,3]].max())*min_wick_ratio
        cond2 = df2.iloc[i,[0,3]].min() > (df2.iloc[i,2]+((df2.iloc[i,1]-df2.iloc[i,2])/2))
        cond3 = df2.iloc[i,2] < df2.iloc[i-10:i,2].min()
        cond4 = abs(df2.iloc[i,0]-df2.iloc[i,3])<((df2.iloc[i,1]-df2.iloc[i,2])*min_candle_size)

        if ( ( cond1 == True )  and ( cond2 == True ) and ( cond3 == True ) and (cond4 == True) ):
                df2.iloc[i,-1] = 1
                print("A hammer is formed on", df2.index[i])
                print(" ")
                
                if (df2.iloc[i,-1] == 1) and (df2.index[i]== datetime.today().date()):
                    hammer_email_alert()
        else: 
                df2.iloc[i,-1] = 0
    
    return df2


def pattern_inspector(df, min_wick_ratio=5, min_candle_size=0.25):
    
    print("Checking for new pattern formation...")
    
    df2 = df.copy()
   
    df2 = hammer_scanner(df2, min_wick_ratio=min_wick_ratio, min_candle_size=min_candle_size)
    df2 = shooting_star_scanner(df2, min_wick_ratio=min_wick_ratio, min_candle_size=min_candle_size)
    
    display(df2[df2['Hammer'] == 1])
    display(df2[df2['Shooting Star'] == 1])
    candlestick_plot(df2)
    
    return df2