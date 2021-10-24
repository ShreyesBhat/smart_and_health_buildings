import pandas as pd

df = pd.read_excel('StudentInfo.xlsx')


print('-----People who finished the assignment-----')
total = len(df)
print(total)
print('--------------------------------------------')

print('----------People who support Elmo-----------')
print(df.groupby('sesame')['username'].nunique())
elmoCount = df.groupby('sesame')['username'].nunique()['elmo']
print(elmoCount)
print('--------------------------------------------')

print('----Night owls supporting cookie monster----')
cookieOwl = df.groupby(['sesame', 'sleep']).size().groupby(level=0).max()
print(cookieOwl)
print('--------------------------------------------')

'''no elmo, no rock, morning birds'''

#df = df.groupby(['sesame', 'rps', 'sleep']).count().reset_index().sort_values('username', ascending=False)
print('-------No Elmo, No rock, Morning Bird-------')
df = df.drop(df[df['sesame']=='Elmo'].index).drop(df[df['rps']=='rock'].index)
print((df.sleep == 'morning bird').sum())
print('--------------------------------------------')
