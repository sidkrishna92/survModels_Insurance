from __future__ import print_function
from readPreprocess import readPreprocess as rp
from survModel import survModel as sm
import matplotlib.pyplot as plt
from lifelines.statistics import logrank_test
import warnings
warnings.filterwarnings('ignore')

'''
Read/Pre-process Data
'''
# Input File Name
insurance_data = 'prosperLoanData.csv'

# Read, preprocess and filter input data
instance1 = rp(insurance_data)
instance1.preprocess(instance1.data_df)
filtered_data = instance1.filter_df

print("\nStatistics for defaulted loans:\n%s" % filtered_data[filtered_data['status']==1].timeDiff.describe())
print("-"*20)
print("\n\nCensored v/s Failure Events:\n%s" % filtered_data['status'].value_counts())

print("-"*20)
'''
Fit Survival Models
'''
#Fit required Survival Model Estimate to input data
timeToEvent = 'timeDiff'
censor = 'status'
survivalModel = sm(filtered_data, timeToEvent, censor, 'KM_Estimate')
survivalModel.kaplanMeier()

#Model by Home ownership
f1 = filtered_data.IsBorrowerHomeowner==True
f2 = filtered_data.IsBorrowerHomeowner==False

survival_model2 = sm(filtered_data[f1], timeToEvent, censor, 'Home Owner')
survival_model2.kaplanMeier()

survival_model3 = sm(filtered_data[f2], timeToEvent, censor, 'NOT Home Owner')
survival_model3.kaplanMeier()

'''
Plot Survival Models
'''
## Uncomment for plot of Surv Function without CI
# survivalModel.kmf.survival_function_.plot()
# plt.title('Survival function of Insurance Defaulters')
# plt.show()
survivalModel.kmf.plot()
plt.title('KM Estimate w CI of Insurance Defaulters')
plt.show()

ax = plt.subplot(111)
survival_model2.kmf.survival_function_.plot(ax = ax)
survival_model3.kmf.survival_function_.plot(ax = ax)

plt.title('Survival Rate of loans based on Home Ownership')
plt.show()

'''
Significance Tests
'''
##Check statistical significance of survival b/w the Groups
result = logrank_test(filtered_data[f1]['timeDiff'].dt.days,
                       filtered_data[f2]['timeDiff'].dt.days,
                       filtered_data[f1]['status'],
                       filtered_data[f2]['status'],
                       alpha=0.99)
print("\n\nResults of Log Rank Test:")
result.print_summary()
