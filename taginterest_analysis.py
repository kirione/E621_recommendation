import pandas as pd
import json


# Convert to DataFrame
df = pd.read_json("users_taginterest.json", lines=True)
print(df.head())


#Calculate user profile tag presence, relative presence and enjoyment


#Look into understanding the need for tag pooling, but tentatively set hard limit for relative presence to exclude common tags 

#Build results of favorites tag correlation per user

#Aggregate tag correlation results across all users


#TF-IDF to identify distinctive tags per user profile
#Calculate user profile tag presence, relative presence and enjoyment
#calculate sample user average(relative presence) *ignores duplicate posts




