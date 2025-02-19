# Spotify-Songs-Dashboard

## Overview

This repository contains a Streamlit dashboard for visualizing and analyzing data from Spotify's most streamed songs of 2024. The dashboard provides insights into top artists, stream trends, playlist reach across various platforms, and track segmentation based on engagement and popularity.

## Features

-   **Data Cleaning and Preprocessing**: Handles missing values, converts data types, and prepares the dataset for analysis.
-   **Interactive Visualizations**: Utilizes Plotly to create dynamic and interactive charts, including bar charts, line charts, pie charts, and heatmaps.
-   **Overview Metrics**: Displays key metrics such as total tracks, total streams, and the most-streamed track.
-   **Platform Comparison**: Compares playlist reach across Spotify, Apple Music, Deezer, and Amazon.
-   **Track Segmentation**: Segments tracks into clusters based on engagement and popularity using KMeans.
-   **Interactive Filtering**: Allows users to explore tracks by selecting specific artists.
-   **Stylish Tables**: Uses Plotly tables with custom styling for enhanced readability.
-   **Responsive Layout**: Designed to provide an optimal viewing experience on various screen sizes.

## Requirements

To run this project, you need:

-   Python 3.x
-   Libraries:

    -   Streamlit
    -   Pandas
    -   Plotly
    -   Scikit-learn
-   Install the required libraries using pip:

```bash
pip install streamlit pandas plotly scikit-learn
```

## Getting Started

### Dataset

The dataset used in this project, `Most Streamed Spotify Songs 2024.csv`, should be placed in the same directory as the Streamlit application. Ensure the dataset is properly formatted for the application to function correctly.

### Running the Code

1.  Clone the repository:

```bash
git clone https://github.com/yourusername/Spotify-Songs-Dashboard.git
cd Spotify-Songs-Dashboard
```

2.  Navigate to the directory containing the Streamlit application.
3.  Run the Streamlit app:

```bash
streamlit run your_app_name.py
```

Replace `your_app_name.py` with the name of your Streamlit application file.

### Usage

-   **Overview Section**: Provides a summary of key metrics related to the dataset.
-   **Top Artists by Streams**: Visualizes the top 10 artists based on Spotify streams.
-   **Streams by Release Year**: Displays the trend of total streams by release year.
-   **Playlist Reach Across Platforms**: Compares the reach of playlists across Spotify, Apple Music, Deezer, and Amazon using pie charts and bar charts.
-   **Correlation Between Key Features**: Shows the correlation matrix between Spotify Streams, Spotify Playlist Count, Spotify Popularity, YouTube Views, TikTok Views, and Apple Music Playlist Count.
-   **Track Segmentation**: Segments tracks into clusters based on engagement and popularity using KMeans.
-   **Interactive Filtering**: Allows users to select an artist and view their tracks with relevant metrics.
-   **Styled Tables**: Displays the top 10 most-streamed tracks across different platforms in a visually appealing table.
-   **Conclusion Section**: Provides a summary and acknowledgment of the data source.

## Code Explanation

### Data Cleaning and Preprocessing

The `clean_column` function ensures that the relevant columns are strings, removes commas, and converts them to numeric values. This step is crucial for handling data inconsistencies and preparing the data for analysis.

### Visualization

-   **Bar Charts**: Used to display the top artists by streams.
-   **Line Charts**: Used to visualize streams by release year.
-   **Pie Charts**: Used to compare playlist reach across platforms.
-   **Heatmaps**: Used to show the correlation between key features.
-   **Scatter Plots**: Used to segment tracks into clusters based on engagement and popularity.

### Machine Learning

-   **KMeans Clustering**: Used to segment tracks into different clusters based on Spotify Streams, Spotify Playlist Count, and Spotify Popularity.

### Interactive Filtering

The `st.selectbox` function allows users to select an artist from a dropdown menu, displaying their tracks and related metrics.

### Styled Tables

The `create_styled_table` function creates visually appealing tables with custom styling for displaying the top 10 most-streamed tracks across different platforms.


## Additional Information

### Customization

-   **Colors and Themes**: Customize the dashboard's colors and themes by modifying the CSS styles in the code.
-   **Metrics**: Add or modify the displayed metrics to suit your specific analysis needs.
-   **Visualizations**: Experiment with different Plotly chart types and configurations to enhance the visual appeal of the dashboard.
-   **Interactivity**: Add more interactive elements, such as sliders and dropdown menus, to allow users to explore the data in different ways.
-   **Data Sources**: Integrate additional data sources to enrich the dashboard with more comprehensive insights.
