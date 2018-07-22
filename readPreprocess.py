import pandas as pd


class readPreprocess():
    """
    Read data from Input Files
    Pre-process and clean data
    """

    def __init__(self, filename):
        self.filename = filename
        self.data_df = pd.DataFrame()
        self.filter_df = pd.DataFrame()
        self.read_data()
        # self.preprocess()

    def read_data(self):
        print("Reading Input Data ....")
        self.data_df = pd.read_csv(self.filename)
        #return self.data_df


    def preprocess(self,dataframe):
        print("Filtering out required columns and cleaning data ...")
        import datetime as dt
        self.data_df = dataframe
        filter_df1 = self.data_df.iloc[:,[50, 64, 5, 6, 18, 19, 21, 49]]
        ##Selecting unique rows by using distinct Loan ID
        filter_df1 = filter_df1.drop_duplicates('LoanKey')


        ##Filter Loan Statuses useful for survival analysis
        statusOfInterest = ["Completed", "Current", "ChargedOff", "Defaulted", "Cancelled"]
        filter_df2 = filter_df1.loc[filter_df1['LoanStatus'].isin(statusOfInterest)]
        ##Assign Boolean (~Indicator for surv models) for Defaulted/ChargedOff Loan types
        # 0 = Censored Data, 1 = Non-censored(event) data
        def bool(row):
            if row.LoanStatus == 'Defaulted' or row.LoanStatus == 'ChargedOff':
                return 1
            else:
                return 0
        filter_df2.loc[:,'status'] = filter_df2.apply(bool, axis=1)
        ##Assign final dates fr all current loan types with nan
        filter_df2['ClosedDate'] = filter_df2['ClosedDate'].fillna("2018-07-03 00:00:00")

        filter_df2['ClosedDate'] = pd.to_datetime(filter_df2['ClosedDate'])
        filter_df2['LoanOriginationDate'] = pd.to_datetime(filter_df2['LoanOriginationDate'])
        filter_df2['timeDiff'] = filter_df2['ClosedDate'] - filter_df2['LoanOriginationDate']

        filter_df3 = filter_df2[(filter_df2['timeDiff'].dt.days > 0)]
        self.filter_df = filter_df3[filter_df3['LoanOriginationDate'].dt.year == 2006]
