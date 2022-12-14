#%% Imports
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Read in original data
df = pd.read_csv('MerchantData.csv')

#Review data quality
df.describe()
df.info()

#Verify no missing information
df['account'].isna().sum()
df['merchant'].isna().sum()
df['date'].isna().sum()
df['fraud'].isna().sum()

#Limit data to only frauded accounts
df = df[df['account'].isin(df[df['fraud']==True]['account'].unique())]

#Create df showing unique account interactions per day by merchant
account_interactions = pd.DataFrame(df.groupby(['merchant', 'date'])
                                    .count()['account'])

#Verify distribution of account transactions
sns.displot(data=account_interactions, x='account')
plt.title('Aggregate Unique Account Interactions per Merchant')
plt.xlabel('Daily Unique Account Interactions')
plt.ylabel('Count of Daily Occurences')
plt.show()

#Obtain top 10 instances of the most account interactions at a merchant
h=account_interactions.nlargest(10, 'account')

h.index[0][0]

#%% Harvest & Exploit Visuals
"""
Show that if the accounts were not transacted on day w/merchant that 
fraud amounts would be drastically lowered
"""
#Loop to auto-generate verification visuals for suspected merch/date
for i in range(len(h)):
    #Variables for suspect harvest period
    m = str(h.index[i][0])
    d = str(h.index[i][1])
     
    #List of flagged accounts
    flagged = df[(df['merchant']==m)&(df['date']==d)]['account'].unique()
    
    #Create subplot object
    f, ax = plt.subplots(1,2, figsize=(16,6))
    
    #Create transactions per suspect merch visual
    sns.histplot(data = df[df['merchant']==m],
                 x ='date',
                 ax=ax[0])
    
    #Axis & title labels, harvest date reference line
    ax[0].set_title('Daily Total Transactions', fontsize=15)
    ax[0].set_xlabel(None)
    ax[0].tick_params(rotation=90)
    ax[0].set_ylabel('Count of Total Transcations', fontsize=15)
    ax[0].axvline(x=d, color='red', ls='--')
        
    #Create fraud transactions per merch/deate visual
    sns.histplot(data=df[(df['account'].isin(flagged))&
                         (df['fraud']==True)],
                 x='date',
                 ax=ax[1])
    
    #Axis & title labels, harvest date reference line
    ax[1].set_title('Daily Fraudulent Transactions', fontsize=15)
    ax[1].set_xlabel(None)
    ax[1].tick_params(rotation=90)
    ax[1].set_ylabel('Count of Fraudulent Transcations', fontsize=15)

    #Overall Title
    f.suptitle(f'Merchant: {m}', fontsize=20)
    plt.show()

