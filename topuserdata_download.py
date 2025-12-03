from requests.auth import HTTPBasicAuth
from e621_api import e621Api
from tqdm import tqdm
import json
import csv

def get_user_interests(favs):
    user_interests = {}
    for fav in favs:
        for topic in fav["tags"]:
            for tag in fav["tags"][topic]:
                tag_name = f"{topic}:{tag}"
                if not tag_name in user_interests:
                    user_interests[tag_name] = 0
                user_interests[tag_name] += 1
    
    for tag in user_interests:
        user_interests[tag] /= len(favs)
    
    return user_interests

INTERESTS_FILE = "interests.json"
MIN_FAVORITES = 100
pages_to_scrape = 1

if __name__ == "__main__":
    e621 = e621Api()
    
    interests = {}

    total_users = 0
    for i in range(pages_to_scrape):
        users = e621.get_top_users(i)
        for user in tqdm(users, f" Analyzing page {i + 1} of users", unit=" users", total=len(users)):
            favs = e621.get_favorites(user["id"], 0)

            if len(favs) < MIN_FAVORITES:
                continue

            interests[user["id"]] = favs
            total_users += 1
    print(f"Processed {total_users} users")
    
    with open(INTERESTS_FILE, 'w') as f:
        json.dump(interests, f, indent=4)