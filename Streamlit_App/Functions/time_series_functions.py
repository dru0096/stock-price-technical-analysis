def fill_dates(df, date_col = "Date"):

    df2 = df.copy()

    # We create a range of consecutive dates
    idx = pd.date_range(df2[date_col].min(), df2[date_col].max())

    # We reindex df2 to have the new dates
    df2 = df2.reindex(idx) 
    df2 = df2.reset_index()

    # Now we do a left join between the new df2 and the original based on columns date
    df2 = df2.merge(df, how='left', left_on='index', right_on=date_col)

    # From the merged dataframe, we select the columns of the old df and "index"
    new_cols = [ col for col in list(df2.columns) if ((col == "index") or ( "_y" in col)) ]
    df2 = df2[new_cols]

    # Now we strip the "_y" from the columns names
    df2.columns = [ col if ("y" not in col) else col.replace("_y","") for col in list(df2.columns) ]

    df2.index = df2['index']

    df2.drop(["index"], axis = 1, inplace = True)

    return df2

#Test for staionarity
def test_stationarity(timeseries):
    #Determing rolling statistics
    rolmean = timeseries.rolling(12).mean()
    rolstd = timeseries.rolling(12).std()
    #Plot rolling statistics:
    plt.plot(timeseries, color='blue',label='Original')
    plt.plot(rolmean, color='red', label='Rolling Mean')
    plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean and Standard Deviation')
    plt.show(block=False)
    print("Results of dickey fuller test")
    adft = adfuller(timeseries,autolag='AIC')
    # output for dft will give us without defining what the values are.
    #hence we manually write what values does it explains using a for loop
    output = pd.Series(adft[0:4],index=['Test Statistics','p-value','No. of lags used','Number of observations used'])
    for key,values in adft[4].items():
        output['critical value (%s)'%key] =  values
    print(output)

def kpss_test(timeseries):
    print("Results of KPSS Test:")
    kpsstest = kpss(timeseries, regression="c", lags = "auto") # In later versions, the "lags" option has been replaced by "nlags"
    kpss_output = pd.Series(
        kpsstest[0:3], index=["Test Statistic", "p-value", "Lags Used"]
    )
    for key, value in kpsstest[3].items():
        kpss_output["Critical Value (%s)" % key] = value
    print(kpss_output)