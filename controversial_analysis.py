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
relevant_columns = ['user_id', 'id', 'sample', 'score', 'tags', 'artist', 'character', 'species', 'rating', 'fav_count']
existing_columns = [col for col in relevant_columns if col in df.columns]
df_trimmed = df[existing_columns].copy()

print(df_trimmed.head())

#Further parse df to flatten certain columns and generate new columns for score, sample, and tags
df_trimmed['sample'] = df_trimmed['sample'].apply(lambda x: x['url'] if isinstance(x, dict) and 'url' in x else None)
df_trimmed['score_up'] = df_trimmed['score'].apply(lambda x: x['up'] if isinstance(x, dict) and 'up' in x else None)
df_trimmed['score_down'] = df_trimmed['score'].apply(lambda x: x['down'] if isinstance(x, dict) and 'down' in x else None)
df_trimmed['total_score'] = df_trimmed['score'].apply(lambda x: x['total'] if isinstance(x, dict) and 'total' in x else None)
df_trimmed['score_ratio'] = (df_trimmed['score_up']/(df_trimmed['score_up']-df_trimmed['score_down']))*100 # Representation of how controversial a post is by dislike ratio
df_trimmed['general_tags'] = df_trimmed['tags'].apply(lambda x: x['general'] if isinstance(x, dict) and 'general' in x else None)
df_trimmed['artist_tags'] = df_trimmed['tags'].apply(lambda x: x['artist'] if isinstance(x, dict) and 'artist' in x else None)
df_trimmed['character_tags'] = df_trimmed['tags'].apply(lambda x: x['character'] if isinstance(x, dict) and 'character' in x else None)
df_trimmed['species_tags'] = df_trimmed['tags'].apply(lambda x: x['species'] if isinstance(x, dict) and 'species' in x else None)
df_final = df_trimmed.drop(columns=['tags', 'score'])
print(df_final.head())

df_final.to_csv("df_final.csv", index=False)
print ("Raw dataFrame saved to df_final.csv")

#Keep duplicate posts for analysis on tags correlation between favorites for each users (WIP)
#Calculate user profile tag presence, relative presence and enjoyment


#Look into understanding the need for tag pooling, but tentatively set hard limit for relative presence to exclude common tags 

#Build results of favorites tag correlation per user

#Aggregate tag correlation results across all users


#Remove duplicate posts before exploding tags for tags analysis and visualization (Tags popularity and score metrics across all users)
df_final = df_final.drop_duplicates(subset=['id'])
df_taganalysis = df_final.explode('general_tags')
df_taganalysis = df_taganalysis.dropna(subset=['general_tags']) 
# Group by tag and calculate average metrics
tag_stats = df_taganalysis.groupby('general_tags').agg(
    avg_score_up=('score_up', 'mean'),
    avg_score_down=('score_down', 'mean'),
    avg_score_ratio=('score_ratio', 'mean'),
    post_count=('id', 'count')  # popularity
).sort_values('post_count', ascending=False)
with pd.ExcelWriter("df_controversyscore.xlsx", engine='openpyxl') as writer:
    tag_stats.to_excel(writer, sheet_name="Tag_Stats", index=True)  # keep tag names as index
    print ("Tag statistics saved to df_controversyscore.xlsx")



