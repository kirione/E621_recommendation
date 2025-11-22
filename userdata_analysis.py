import pandas as pd
import json

with open('interests.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

#Flatten the JSON structure into a DataFrame of posts with post ID as primary key, and user ID as secondary key
flat_posts = []

for user, posts in data.items():  # assuming data is a list of user dicts
    user_id = user
    for post in posts:
        # Make a single dict with user_id + post metadata
        flat_post = {'user_id': user_id}
        flat_post.update(post)  # add all post metadata
        flat_posts.append(flat_post)

# Convert to DataFrame
df = pd.DataFrame(flat_posts)

print(df.head())