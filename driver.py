from __future__ import print_function
from readPreprocess import readPreprocess as rp
from survModel import survModel as sm
import matplotlib.pyplot as plt

insurance_data = 'prosperLoanData.csv'

## Read, preprocess and filter input data
instance1 = rp(insurance_data)
instance1.preprocess(instance1.data_df)
filtered_data = instance1.filter_df

print("Statistics for defaulted loans:\n%s" % filtered_data[filtered_data['status']==1].timeDiff.describe())
print("\n\nCensored v/s Failure Events:\n%s"% filtered_data['status'].value_counts())

## Fit required Survival Model Estimate to input data
timeToEvent = 'timeDiff'
censor = 'status'
survivalModel = sm(filtered_data, timeToEvent, censor)
survivalModel.kaplanMeier()

survivalModel.kmf.survival_function_.plot()
plt.title('Survival function of Insurance Defaulters')
plt.show()

survivalModel.kmf.plot()
plt.title('KM Estimate w CI of Insurance Defaulters')
plt.show()


print('....')

