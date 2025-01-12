# Movie Recommendation System

## Overview
This movie recommendation system employs a hybrid approach, combining Collaborative Filtering and Content-Based Filtering, to generate personalized movie suggestions.

---

## Dataset | [Link](https://grouplens.org/datasets/movielens/100k/)
MovieLens 100K movie ratings. Stable benchmark dataset. 100,000 ratings from 1000 users on 1700 movies. Released 4/1998.

---

## Architecture

### Collaborative Filtering
- **Model**: Singular Value Decomposition (SVD)
- **Methodology**: Utilizes user-movie interaction data (ratings) to learn latent features for users and movies, enabling prediction of unseen ratings.
- **Assumptions**: Users with similar rating behaviors are likely to enjoy similar movies.
- **Trade-offs**:
  - **Strength**: Effective for large datasets with extensive user-movie interactions.
  - **Limitation**: Faces cold-start issues for new users or movies with no prior interactions.

### Content-Based Filtering
- **Model**: Cosine Similarity
- **Methodology**: Computes similarity between movies based on their genre attributes to recommend movies similar to a user's favorites.
- **Assumptions**: Movies with similar features (e.g., genres) appeal to the same audience.
- **Trade-offs**:
  - **Strength**: Handles new movies well by focusing on their attributes.
  - **Limitation**: May overfit to user preferences, leading to limited diversity in recommendations.

### Hybrid Approach
- **Methodology**: Combines collaborative and content-based scores using tunable weights.
- **Weighting Scheme**: 
  - Collaborative Filtering: 70%  
  - Content-Based Filtering: 30%

---

## Implementation

### Data Preparation
- **Dataset**: MovieLens 100K
- **Preprocessing Steps**:
  - Normalized user ratings.
  - Merged `u.data` (ratings) with `u.item` (movie metadata).

### Collaborative Filtering
- **Implementation**: Used the `Surprise` library's SVD algorithm.
- **Evaluation**: Performed using a train-test split (80%-20%).

### Content-Based Filtering
- **Feature Extraction**: Extracted genre attributes from movie metadata.
- **Similarity Calculation**: Computed a cosine similarity matrix for all movies.

### Hybrid Recommendation
- **Methodology**: Merged scores from both methods to recommend movies.

### Precision@K
- **Purpose**: Added as an evaluation metric to measure recommendation relevance.

---

## Evaluation

### Metrics Used
- **RMSE (Root Mean Squared Error)**: Evaluates prediction accuracy of user ratings.
  - Collaborative Filtering RMSE: **0.9354**
- **Precision@K**: Measures relevance of top recommendations.
  - Precision@3: **0.7202**

### Sample Recommendations
#### Content-Based Filtering
- Recommendations for a user:
  - *African Queen, The (1951)*
  - *Star Wars (1977)*
  - *Face/Off (1997)*
  - *Terminator, The (1984)*
  - *Mad Love (1995)*

#### Collaborative Filtering
- Top recommendations for a user:
  - *Johnny Mnemonic (1995)*
  - *Breakfast at Tiffany's (1961)*
  - *Dead Man Walking (1995)*

---

## Future Enhancements

### Cold-Start Problem
- Include demographic and contextual data for new users.
- Use external movie databases (e.g., IMDb) to enrich metadata for new movies.

### Explainability
- Display top factors influencing recommendations (e.g., similar genres, highly rated by similar users).
- Visualize latent features learned by the model.

### Scalability
- Integrate real-time recommendation pipelines using tools like Apache Spark.
- Optimize collaborative filtering for distributed environments.

### User Engagement
- Allow users to provide feedback to refine future recommendations.
- Introduce filtering options by attributes like genre, release year, etc.

---

## Conclusion
The implemented movie recommendation system effectively combines collaborative filtering and content-based filtering, leveraging their strengths to address diverse user needs. With high accuracy and relevance, it provides a robust foundation for future enhancements in real-world applications.
