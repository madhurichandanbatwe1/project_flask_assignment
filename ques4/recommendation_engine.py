import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def get_user_recommendations(user_id, ratings_df, num_recommendations=5):
    user_ratings = ratings_df.pivot(index='user_id', columns='item_id', values='rating')
    user_similarity = cosine_similarity(user_ratings.fillna(0))
    similar_users = pd.Series(user_similarity[user_id - 1]).sort_values(ascending=False)
    
    recommendations = []
    for other_user in similar_users.index[1:]:
        user_rated_items = ratings_df[ratings_df['user_id'] == other_user]['item_id']
        recommendations.extend(user_rated_items)
    
    return pd.Series(recommendations).value_counts().head(num_recommendations).index.tolist()
