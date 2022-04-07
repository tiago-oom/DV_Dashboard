df = pd.read_csv(
    "C:/Users/tsoom/OneDrive/Documentos/IMS - Data Science/2º Semester/Data Visualization/Github/CSVs/types_of_conflits.csv")

df.drop(columns=['Code'], inplace=True)

df.rename(columns={'Entity': 'world_region',
                   'Year': 'year',
                   'Number of civil conflicts with foreign state intervention': 'civil-foreign conflits',
                   'Number of civil conflicts': 'civil conflicts',
                   'Number of conflicts between states': 'between states conflicts',
                   'Number of colonial or imperial conflicts': 'colonial/imperial conflicts'}, inplace=True)

df['world_region'] = df['world_region'].astype('string')

df['total number of conflicts'] = df['civil-foreign conflicts'] + df['civil conflicts'] + df[
    'between states conflicts'] + df['colonial/imperial conflicts']

#############################################
df2 = df.loc[df['world_region'] != 'World']
df2 = df2.loc[df['year'] > 2000]  # !!!!!!!!

###############################################
df1 = df.drop(['civil-foreign state conflits', 'civil conflicts', 'between states conflicts', 'colonial/imperial conflicts'], axis = 1)
df1.set_index('world_region', inplace = True)
df1 = pd.pivot_table(df1, values = 'total number of conflicts', index = 'world_region', columns = 'year')
df1.drop('World', axis = 0, inplace = True)
colors = ['#B6E880', '#FF97FF', '#FECB52', '#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692']