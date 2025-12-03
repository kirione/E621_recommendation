import pandas as pd
import json

#Set thresholds
min_percent = 0.05 # Minimum percent tag frequency to consider a tag
relative_presence_threshold = 1.5 # Minimum relative presence compared to global average to consider a tag

#Targeted tag for subset profile
target_tag = "bondage"
# Convert average users tag interest to DataFrame
with open("average_taginterest.json") as f:
    data = json.load(f)
    average_taginterest_series = pd.Series(data)
    print(average_taginterest_series)

# Convert top users tag interest to DataFrame
users_taginterest_df = pd.read_json("users_taginterest.json", lines=True)
print(users_taginterest_df.head())

# Subset profile
# Get the average target tag rate across all users
global_interest = average_taginterest_series[target_tag]
print (f"Global {target_tag} average: {global_interest}")

#Iterate all scraped users to calculate their tag interest profile compared to global average
tag_enjoyer_dict = {}
for idx, user in users_taginterest_df.iterrows():
    user_id = user["user_id"]

    user_interest = user["tag_interest"].get(target_tag)
    if user_interest is None:
        continue
    print("User:", user_id, "Interests:", user_interest)
    if user_interest > global_interest:
        tag_enjoyer_dict[user_id] = user_interest

print("Tag enjoyers:", tag_enjoyer_dict)


# Average tag enjoyer interests by creating a subset profile
df_indexed = users_taginterest_df.set_index("user_id")

subset_interests = {}
total_users = 0
for user_id in sorted(tag_enjoyer_dict):
    tags_dict = df_indexed.at[user_id, "tag_interest"]
    #init missing tags in subset_interest dict
    for tag in tags_dict:
        if tag not in subset_interests:
                subset_interests[tag] = 0
    #update averages
    for tag in subset_interests:
        user_interest_in_tag = tags_dict.get(tag, 0.0)
        subset_interests[tag] = (subset_interests[tag] * total_users + user_interest_in_tag) / (total_users + 1)

    total_users += 1

for tag in list(subset_interests.keys()):
    if subset_interests[tag] < min_percent:
        del subset_interests[tag]
print("Subset interests:", subset_interests)

#filter for relative presence from global average
subset_interests_relativepresence = {}
for tag in subset_interests:
    if tag == target_tag:
        continue
    if (subset_interests[tag]/average_taginterest_series.get(tag, 0.0)) > relative_presence_threshold:
        subset_interests_relativepresence[tag] = subset_interests[tag]/average_taginterest_series.get(tag, 0.0)
        print (f"Tag {tag} has an relative presence of {subset_interests_relativepresence[tag]}: average interest {subset_interests[tag]:.3f} vs global {average_taginterest_series.get(tag, 0.0):.3f}")

#Convert to dataframe for better visualization
subset_interests_relativepresence_df = pd.DataFrame(
    [(k, float(v)) for k, v in subset_interests_relativepresence.items()],
    columns=["tag", "value"]
)
# Sort descending (optional)
subset_interests_relativepresence_df = subset_interests_relativepresence_df.sort_values("value", ascending=False).reset_index(drop=True)

print(subset_interests_relativepresence_df.to_string(index=False))
        
#Deriving enjoyment from harmonic mean of presence and relative presence
subset_interests_enjoyment = {}
RELATIVE_PRESENCE_CAP = 3.0
for tag in subset_interests_relativepresence:
    subset_interests_enjoyment[tag] = 2 / (1 / (min(RELATIVE_PRESENCE_CAP, subset_interests_relativepresence[tag]) / RELATIVE_PRESENCE_CAP) + 1 / subset_interests[tag])
    print (f"Tag {tag} has an enjoyment of {subset_interests_enjoyment[tag]}")










