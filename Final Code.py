import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


# Load data
df = pd.read_csv('/content/2024-2025 nba season dataset MODI.csv')

# Handle missing values
numerical_cols = df.select_dtypes(include=np.number).columns
df[numerical_cols] = df[numerical_cols].fillna(0)

# Feature selection (using the revised features)
selected_features = ['MP', 'PTS', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'FG%', '3P%', 'FT%']
df_selected = df[selected_features]

# Determine optimal k using RobustScaler
k_range = range(2, 11)
silhouette_scores_robust = []
inertia_robust = []

# RobustScaler
scaler_robust = RobustScaler()
df_scaled_robust = scaler_robust.fit_transform(df_selected)
for k in k_range:
    kmeans_robust = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans_robust.fit(df_scaled_robust)
    inertia_robust.append(kmeans_robust.inertia_)
    score_robust = silhouette_score(df_scaled_robust, kmeans_robust.labels_)
    silhouette_scores_robust.append(score_robust)


# Display silhouette scores
silhouette_table_robust = pd.DataFrame({
    'Number of Clusters (K)': k_range,
    'Silhouette Score (RobustScaler)': silhouette_scores_robust
})

display(silhouette_table_robust)

# Plot silhouette scores
plt.figure(figsize=(8, 6))
plt.plot(k_range, silhouette_scores_robust, marker='o')
plt.title('Silhouette Scores with RobustScaler')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Silhouette Score')
plt.xticks(k_range)
plt.grid(True)
plt.show()

# Add some space between plots
print("\n" * 2) # Add blank lines for spacing

# Plot Elbow Method
plt.figure(figsize=(8, 6))
plt.plot(k_range, inertia_robust, marker='o')
plt.title('Elbow Method with RobustScaler')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Inertia')
plt.xticks(k_range)
plt.grid(True)
plt.show()

# Add some space between plots
print("\n" * 2) # Add blank lines for spacing


# Apply K-Means with the optimal parameters (RobustScaler, K=4 based on previous analysis)
optimal_k = 4
kmeans_optimal = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
kmeans_optimal.fit(df_scaled_robust)
df['Cluster_Robust_k4'] = kmeans_optimal.labels_

# Visualize clusters using PCA
pca_robust = PCA(n_components=2)
df_pca_robust = pca_robust.fit_transform(df_scaled_robust)

plt.figure(figsize=(8, 6))
plt.scatter(df_pca_robust[:, 0], df_pca_robust[:, 1], c=df['Cluster_Robust_k4'], cmap='viridis', s=50, alpha=0.6)
plt.title(f'K-Means Clustering Results with RobustScaler (PCA 2D, K={optimal_k})')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.colorbar(label='Cluster')
plt.grid(True)
plt.show()

# Add some space between plots
print("\n" * 2) # Add blank lines for spacing

# Analyze cluster characteristics
cluster_characteristics_robust_k4 = df.groupby('Cluster_Robust_k4')[selected_features].mean()
display(cluster_characteristics_robust_k4)

# Add some space between plots
print("\n" * 2) # Add blank lines for spacing

# Examine players within clusters (show count only)
for cluster_label in df['Cluster_Robust_k4'].unique():
    players_in_cluster = df[df['Cluster_Robust_k4'] == cluster_label]['Player']
    num_players = len(players_in_cluster)
    print(f"--- Cluster {cluster_label} ({num_players} players) ---")
    print("\n" * 1) # Add blank line between cluster summaries
