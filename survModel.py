
class survModel():

    def __init__(self, inputDf, eventTime, censorVar, label):
        self.inputDf = inputDf
        self.eventTime = eventTime
        self.censorVar = censorVar
        self.label = label


    def kaplanMeier(self):
        from lifelines.estimation import KaplanMeierFitter
        df = self.inputDf
        self.kmf = KaplanMeierFitter()
        time = df[self.eventTime].dt.days
        status = df[self.censorVar]
        lab = self.label
        self.kmf.fit(time, event_observed = status, label = lab)




