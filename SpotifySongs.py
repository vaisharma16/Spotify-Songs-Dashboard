import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans

# Load the dataset
file_path = "Most Streamed Spotify Songs 2024.csv"
data = pd.read_csv(file_path, encoding="latin1")

# Clean and preprocess the data
# Ensure all relevant columns are strings and remove commas, then convert to numeric
def clean_column(col):
    # Ensure the column is a string, fill NaNs with empty string
    col = col.fillna('').astype(str)
    # Remove commas and convert to numeric
    col = col.apply(lambda x: x.replace(',', '') if isinstance(x, str) else x)
    return pd.to_numeric(col, errors='coerce')  # Convert to numeric, handle errors as NaN

# Apply the cleaning function to all relevant columns
data['Spotify Streams'] = clean_column(data['Spotify Streams'])
data['Spotify Playlist Count'] = clean_column(data['Spotify Playlist Count'])
data['Spotify Playlist Reach'] = clean_column(data['Spotify Playlist Reach'])
data['YouTube Views'] = clean_column(data['YouTube Views'])
data['TikTok Views'] = clean_column(data['TikTok Views'])
data['Apple Music Playlist Count'] = clean_column(data['Apple Music Playlist Count'])
data['Deezer Playlist Count'] = clean_column(data['Deezer Playlist Count'])
data['Amazon Playlist Count'] = clean_column(data['Amazon Playlist Count'])

# Convert Release Date to datetime and extract the year
data['Release Date'] = pd.to_datetime(data['Release Date'])
data['Year'] = data['Release Date'].dt.year

# Feature Engineering: Create Spotify Engagement
data['Spotify Engagement'] = data['Spotify Streams'] * 0.5 + data['Spotify Playlist Count'] * 0.3 + data['Spotify Popularity'] * 0.2

# Fill missing values for the clustering columns with the mean of each column
clustering_columns = ['Spotify Streams', 'Spotify Playlist Count', 'Spotify Popularity']
data[clustering_columns] = data[clustering_columns].fillna(data[clustering_columns].mean())

# Overview metrics
total_tracks = len(data)
total_streams = data['Spotify Streams'].sum()
most_streamed_track = data.loc[data['Spotify Streams'].idxmax()]

# Streamlit layout
st.set_page_config(page_title="Spotify Music Dashboard", layout="wide")
st.title("🎧 Spotify Music Dashboard 2024")

# Overview section
st.markdown("### Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Tracks", total_tracks)
col2.metric("Total Streams", f"{total_streams:,.0f}")
col3.metric("Most Streamed Track", most_streamed_track['Track'], f"{most_streamed_track['Spotify Streams'] / 1e6:.1f}M Streams")

# Visualization: Streams by Artist
st.markdown("### Top 10 Artists by Streams")
top_artists = data.groupby('Artist')['Spotify Streams'].sum().sort_values(ascending=False).head(10).reset_index()
fig_artists = px.bar(
    top_artists, 
    x='Spotify Streams', 
    y='Artist', 
    orientation='h', 
    title="Top 10 Artists by Spotify Streams", 
    text='Spotify Streams', 
    color='Spotify Streams', 
    color_continuous_scale='Viridis'
)
fig_artists.update_layout(paper_bgcolor="#121212", plot_bgcolor="#121212", font_color="black")
st.plotly_chart(fig_artists, use_container_width=True)

# Visualization: Streams by Year
st.markdown("### Streams by Release Year")
yearly_streams = data.groupby('Year')['Spotify Streams'].sum().reset_index()
fig_yearly = px.line(
    yearly_streams, 
    x='Year', 
    y='Spotify Streams', 
    title="Total Streams by Release Year", 
    markers=True
)
fig_yearly.update_layout(paper_bgcolor="#121212", plot_bgcolor="#121212", font_color="black")
st.plotly_chart(fig_yearly, use_container_width=True)

# Visualization: Playlist Reach Across Platforms
st.markdown("### Playlist Reach Across Platforms")

# Replace NaN values with 0 (or use another strategy based on your understanding of the dataset)
data_cleaned = data.fillna(0)

# Verify the sum of each platform's playlist reach
spotify_reach = data_cleaned['Spotify Playlist Reach'].sum()
apple_music_reach = data_cleaned['Apple Music Playlist Count'].sum()
deezer_reach = data_cleaned['Deezer Playlist Count'].sum()
amazon_reach = data_cleaned['Amazon Playlist Count'].sum()

# Display these sums for debugging
st.write(f"Spotify Playlist Reach: {spotify_reach}")
st.write(f"Apple Music Playlist Count: {apple_music_reach}")
st.write(f"Deezer Playlist Count: {deezer_reach}")
st.write(f"Amazon Playlist Count: {amazon_reach}")

# Prepare the dictionary with total reach per platform
platforms_data = {
    'Spotify Playlist Reach': spotify_reach,
    'Apple Music Playlist Count': apple_music_reach,
    'Deezer Playlist Count': deezer_reach,
    'Amazon Playlist Count': amazon_reach,
}

# Calculate the total reach across all platforms
total_reach = sum(platforms_data.values())

# Check if the total reach is as expected (this should give us an idea if any one column is overwhelming)
st.write(f"Total Playlist Reach (sum of all platforms): {total_reach}")

# Normalize the data (to ensure the pie chart makes sense)
platforms_data_normalized = {k: v / total_reach for k, v in platforms_data.items()}

# Check the distribution of 'Spotify Playlist Reach' using a histogram
import plotly.express as px

# Histogram to see the distribution of Spotify Playlist Reach
fig = px.histogram(data, x='Spotify Playlist Reach', title="Distribution of Spotify Playlist Reach")
fig.update_layout(paper_bgcolor="#121212", font_color="black")
st.plotly_chart(fig, use_container_width=True)

# Create a new column 'Total Reach' that sums the reach across all platforms
data['Total Reach'] = data['Spotify Playlist Reach'] + data['Apple Music Playlist Count'] + data['Deezer Playlist Count'] + data['Amazon Playlist Count']

# Sort the tracks by 'Total Reach' in descending order to get the most streamed track at the top
most_streamed_track = data.sort_values(by='Total Reach', ascending=False).head(10)  # top 10 most streamed tracks

import plotly.express as px

# Select the top 10 most streamed tracks
top_10_tracks = most_streamed_track[['Track', 'Total Reach']].head(10)

# Create a bar chart to visualize the top 10 most streamed tracks
fig = px.bar(top_10_tracks, x='Track', y='Total Reach', 
             title="Top 10 Most Streamed Tracks Across Platforms",
             labels={'Track Name': 'Track', 'Total Reach': 'Total Reach (Streams)'},
             color='Total Reach', color_continuous_scale='Viridis')

fig.update_layout(paper_bgcolor="#121212", font_color="black")
st.plotly_chart(fig, use_container_width=True)

import plotly.graph_objects as go
import streamlit as st

# Function to create a highly styled table
def create_styled_table(df, title, column_mapping):
    df = df.rename(columns=column_mapping)  # Rename columns for better readability
    df = df.reset_index(drop=True)  # Reset index to remove the default numerical index

    # Highlight top row (optional)
    highlight_color = "#FFD700"  # Gold color for top row
    cell_colors = [
        [highlight_color if i == 0 else "#FFFFFF" for i in range(len(df))],  # Row-specific colors
        ["#F9F9F9" if i % 2 == 0 else "#EFEFEF" for i in range(len(df))],  # Alternating row colors
    ]

    # Create Plotly Table with advanced styling
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=[f"<b>{col}</b>" for col in df.columns],  # Bold column names
                    fill_color="#1DB954",  # Spotify Green color for header
                    align="center",
                    font=dict(color="white", size=16),  # Larger, white header text
                    height=35,
                ),
                cells=dict(
                    values=[df[col] for col in df.columns],  # Data for each column
                    fill=dict(color=cell_colors),  # Apply row-specific colors
                    align="center",
                    font=dict(color="#333333", size=14),  # Slightly larger cell text
                    height=28,
                ),
            )
        ]
    )
    # Add title with larger font and spacing
    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(size=22, color="#444444"),  # Larger, bold title
            x=0.5,  # Center align title
            xanchor="center",
        ),
        paper_bgcolor="#F4F4F4",  # Subtle gray background for the dashboard
        margin=dict(l=0, r=0, t=60, b=0),  # Adjust margins for better spacing
    )
    st.plotly_chart(fig, use_container_width=True)

# Prepare the data
most_streamed_spotify = data.sort_values(by='Spotify Playlist Reach', ascending=False).head(10)[['Track', 'Spotify Playlist Reach']]
most_streamed_apple_music = data.sort_values(by='Apple Music Playlist Count', ascending=False).head(10)[['Track', 'Apple Music Playlist Count']]
most_streamed_deezer = data.sort_values(by='Deezer Playlist Count', ascending=False).head(10)[['Track', 'Deezer Playlist Count']]
most_streamed_amazon = data.sort_values(by='Amazon Playlist Count', ascending=False).head(10)[['Track', 'Amazon Playlist Count']]

# Display the styled tables
create_styled_table(most_streamed_spotify, "Top 10 Most Streamed Tracks on Spotify", {"Track": "Track Name", "Spotify Playlist Reach": "Reach"})
create_styled_table(most_streamed_apple_music, "Top 10 Most Streamed Tracks on Apple Music", {"Track": "Track Name", "Apple Music Playlist Count": "Reach"})
create_styled_table(most_streamed_deezer, "Top 10 Most Streamed Tracks on Deezer", {"Track": "Track Name", "Deezer Playlist Count": "Reach"})
create_styled_table(most_streamed_amazon, "Top 10 Most Streamed Tracks on Amazon", {"Track": "Track Name", "Amazon Playlist Count": "Reach"})



import numpy as np

# Apply log transformation to the reach data to handle large values
platforms_data_logged = {
    'Spotify Playlist Reach': np.log1p(spotify_reach),
    'Apple Music Playlist Count': np.log1p(apple_music_reach),
    'Deezer Playlist Count': np.log1p(deezer_reach),
    'Amazon Playlist Count': np.log1p(amazon_reach),
}

# Calculate the total reach after log transformation
total_logged_reach = sum(platforms_data_logged.values())

# Normalize the data using the logged values
platforms_data_logged_normalized = {k: v / total_logged_reach for k, v in platforms_data_logged.items()}

# Create a pie chart of normalized playlist reach (log scale)
fig_logged_platforms = px.pie(
    names=list(platforms_data_logged_normalized.keys()), 
    values=list(platforms_data_logged_normalized.values()), 
    title="Normalized Playlist Reach (Log Scale) Distribution Across Platforms"
)
fig_logged_platforms.update_layout(paper_bgcolor="#121212", font_color="black")
st.plotly_chart(fig_logged_platforms, use_container_width=True)

# Visualization: Correlation Between Key Features
st.markdown("### Correlation Between Key Features")
correlation_matrix = data[['Spotify Streams', 'Spotify Playlist Count', 'Spotify Popularity', 'YouTube Views', 'TikTok Views', 'Apple Music Playlist Count']].corr()
fig_heatmap = px.imshow(correlation_matrix, text_auto=True, title="Correlation Between Key Features")
fig_heatmap.update_layout(paper_bgcolor="#121212", font_color="black")
st.plotly_chart(fig_heatmap, use_container_width=True)

# Clustering: Segment tracks based on multiple metrics
st.markdown("### Track Segmentation Based on Engagement and Popularity")
X = data[['Spotify Streams', 'Spotify Playlist Count', 'Spotify Popularity']]
kmeans = KMeans(n_clusters=3)
data['Cluster'] = kmeans.fit_predict(X)

fig_clusters = px.scatter(
    data, 
    x='Spotify Streams', 
    y='Spotify Playlist Count', 
    color='Cluster', 
    title="Track Segmentation Based on Engagement and Popularity"
)
fig_clusters.update_layout(paper_bgcolor="#121212", plot_bgcolor="#121212", font_color="black")
st.plotly_chart(fig_clusters, use_container_width=True)

# Interactive filtering
st.markdown("### Explore Tracks by Artist")
selected_artist = st.selectbox("Select an Artist", options=data['Artist'].dropna().unique())
artist_data = data[data['Artist'] == selected_artist]
st.write(f"### Tracks by {selected_artist}")
st.dataframe(artist_data[['Track', 'Spotify Streams', 'Spotify Playlist Count', 'Spotify Popularity']])

# Conclusion section
st.markdown("---")
st.markdown("**Note:** This dashboard is powered by data from the most streamed Spotify songs of 2024, showcasing insights across platforms and key features.")

# Footer with your name (Creative and Professional, not fixed)
footer = """
    <style>
        .footer {
            width: 100%;
            background-color: #1DB954;
            color: white;
            text-align: center;
            font-size: 14px;
            padding: 10px 0;
            font-family: 'Arial', sans-serif;
            margin-top: 20px;
        }
        .footer a {
            color: white;
            text-decoration: none;
            font-weight: bold;
        }
    </style>
    <div class="footer">
        <p>Made with ❤️ by <a href="https://www.linkedin.com/in/vaisharma16/" target="_blank">Vaibhav Sharma</a></p>
    </div>
"""

# Display footer at the end
st.markdown(footer, unsafe_allow_html=True)
