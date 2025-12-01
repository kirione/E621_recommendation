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

#Modify df to include only relevant columns: user_id, post_id, sample, score, tags, artist, character, species, rating, fav_count
relevant_columns = ['user_id', 'id', 'sample', 'tags', 'artist', 'fav_count']
existing_columns = [col for col in relevant_columns if col in df.columns]
df_trimmed = df[existing_columns].copy()
print(f"df_trimmed: {df_trimmed.head()}")

#Further parse df to flatten certain columns and generate new columns for score, sample, and tags
df_trimmed['sample'] = df_trimmed['sample'].apply(lambda x: x['url'] if isinstance(x, dict) and 'url' in x else None)
df_trimmed['general_tags'] = df_trimmed['tags'].apply(lambda x: x['general'] if isinstance(x, dict) and 'general' in x else None)
df_trimmed['artist_tags'] = df_trimmed['tags'].apply(lambda x: x['artist'] if isinstance(x, dict) and 'artist' in x else None)
df_final = df_trimmed.drop(columns=['tags'])
print(f"df_final: {df_final.head()}")

#Calculate user profile tag presence, relative presence and enjoyment


#Look into understanding the need for tag pooling, but tentatively set hard limit for relative presence to exclude common tags 

#Build results of favorites tag correlation per user

#Aggregate tag correlation results across all users


#TF-IDF to identify distinctive tags per user profile
#Calculate user profile tag presence, relative presence and enjoyment
#calculate sample user average(relative presence) *ignores duplicate posts
average_taginterest_file = "users_taginterest.json"
#sum general tags interest per user
for user_id, group in df_final.groupby('user_id'):
    tag_counts = {}
    total_posts = len(group)
    
    for tags in group['general_tags']:
        for tag in tags:
            if tag not in tag_counts:
                tag_counts[tag] = 0
            tag_counts[tag] += 1
    
    # Calculate relative presence
    tag_relative_presence = {tag: count / total_posts for tag, count in tag_counts.items()}
    
    # Save to JSON
    
    with open(average_taginterest_file, 'a', encoding='utf-8') as f:
        json.dump({
        "user_id": user_id,
        "tag_interest": tag_relative_presence
    }, f)
        f.write('\n')



