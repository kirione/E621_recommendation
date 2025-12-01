import pandas as pd
import json


# Convert to DataFrame
df = pd.read_json("users_taginterest.json", lines=True)
print(df.head())


#Calculate user profile tag presence, relative presence and enjoyment


#Look into understanding the need for tag pooling, but tentatively set hard limit for relative presence to exclude common tags 

#Build results of favorites tag correlation per user

#Aggregate tag correlation results across all users


#TF-IDF to identify distinctive tags per user profile. Using which to calculate user profile tag presence, relative presence and enjoyment
#calculate sample user average(relative presence)
average_taginterest_file = "average_taginterest.json"
average_interests = {}
total_users = 0

for index, row in df.iterrows():
    for tag in row["tag_interest"]:
        if not tag in average_interests:
                average_interests[tag] = 0

    for tag in average_interests:
        user_interest_in_tag = row["tag_interest"].get(tag, 0.0)
        average_interests[tag] = (average_interests[tag] * total_users + user_interest_in_tag) / (total_users + 1)

    total_users += 1

with open(average_taginterest_file, 'w') as f:
        json.dump(average_interests, f, indent=4)





