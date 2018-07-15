
class survModel():

    def __init__(self, inputDf, eventTime, censorVar):
        self.inputDf = inputDf
        self.eventTime = eventTime
        self.censorVar = censorVar


    def kaplanMeier(self):
        from lifelines.estimation import KaplanMeierFitter
        df = self.inputDf
        self.kmf = KaplanMeierFitter()
        time = df[self.eventTime].dt.days
        status = df[self.censorVar]
        self.kmf.fit(time, event_observed = status, label='KM_Estimate')




