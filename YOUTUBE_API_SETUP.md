# 📺 YouTube API Integration Guide

## Current Implementation

The enhanced web app currently uses **sample/mock YouTube videos**. To integrate real YouTube API:

## 🔑 Step 1: Get YouTube API Key

1. **Go to Google Cloud Console:**

   - Visit: https://console.cloud.google.com/

2. **Create a New Project:**

   - Click "Select a project" → "New Project"
   - Name: "Pneumonia Detection App"
   - Click "Create"

3. **Enable YouTube Data API v3:**

   - Go to "APIs & Services" → "Library"
   - Search for "YouTube Data API v3"
   - Click "Enable"

4. **Create API Credentials:**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "API Key"
   - Copy your API key
   - (Optional) Restrict the key to YouTube Data API v3

## 🔧 Step 2: Add API Key to Your Project

### Option A: Environment Variable (Recommended)

```bash
# Create .env file
echo "YOUTUBE_API_KEY=your_api_key_here" > .env
```

### Option B: Streamlit Secrets

```bash
# Create .streamlit/secrets.toml
mkdir -p .streamlit
echo 'YOUTUBE_API_KEY = "your_api_key_here"' > .streamlit/secrets.toml
```

## 💻 Step 3: Update Code with Real API

Replace the `get_youtube_videos()` function in `enhanced_web_app.py`:

```python
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def get_youtube_videos(query, max_results=5):
    """Get real YouTube video recommendations using YouTube Data API"""

    # Get API key from environment or Streamlit secrets
    try:
        api_key = st.secrets["YOUTUBE_API_KEY"]
    except:
        api_key = os.getenv("YOUTUBE_API_KEY")

    if not api_key:
        st.warning("YouTube API key not configured. Showing sample videos.")
        return get_sample_videos(query)  # Fallback to sample videos

    try:
        # Build YouTube API client
        youtube = build('youtube', 'v3', developerKey=api_key)

        # Search for videos
        search_response = youtube.search().list(
            q=query,
            part='id,snippet',
            maxResults=max_results,
            type='video',
            relevanceLanguage='en',
            safeSearch='strict',
            videoEmbeddable='true'
        ).execute()

        videos = []

        for item in search_response.get('items', []):
            video_id = item['id']['videoId']
            snippet = item['snippet']

            # Get video details for duration
            video_response = youtube.videos().list(
                part='contentDetails,statistics',
                id=video_id
            ).execute()

            if video_response['items']:
                duration = video_response['items'][0]['contentDetails']['duration']
                view_count = video_response['items'][0]['statistics'].get('viewCount', 'N/A')

                videos.append({
                    'title': snippet['title'],
                    'channel': snippet['channelTitle'],
                    'url': f'https://www.youtube.com/watch?v={video_id}',
                    'thumbnail': snippet['thumbnails']['medium']['url'],
                    'duration': parse_duration(duration),
                    'views': format_views(view_count),
                    'published': snippet['publishedAt'][:10]
                })

        return videos

    except HttpError as e:
        st.error(f"YouTube API error: {e}")
        return get_sample_videos(query)  # Fallback to sample videos

def parse_duration(duration):
    """Convert ISO 8601 duration to readable format"""
    import isodate
    try:
        td = isodate.parse_duration(duration)
        minutes = int(td.total_seconds() // 60)
        seconds = int(td.total_seconds() % 60)
        return f"{minutes}:{seconds:02d}"
    except:
        return "N/A"

def format_views(views):
    """Format view count"""
    try:
        views = int(views)
        if views >= 1000000:
            return f"{views/1000000:.1f}M views"
        elif views >= 1000:
            return f"{views/1000:.1f}K views"
        else:
            return f"{views} views"
    except:
        return "N/A"

def get_sample_videos(query):
    """Fallback sample videos (current implementation)"""
    # Your existing sample videos code here
    pass
```

## 📊 Step 4: Update Video Display

Update the video card display to show real thumbnails:

```python
for video in videos:
    col1, col2 = st.columns([1, 3])

    with col1:
        if 'thumbnail' in video and video['thumbnail'].startswith('http'):
            st.image(video['thumbnail'], use_column_width=True)
        else:
            st.write(video.get('thumbnail', '🎥'))

    with col2:
        st.markdown(f"**{video['title']}**")
        st.caption(f"{video['channel']} • {video.get('views', '')} • {video.get('published', '')}")
        st.markdown(f"[▶️ Watch on YouTube]({video['url']})")
```

## 🚀 Step 5: Deploy with API Key

### For Streamlit Cloud:

1. Go to your app settings
2. Click "Secrets"
3. Add:
   ```toml
   YOUTUBE_API_KEY = "your_api_key_here"
   ```

### For Heroku:

```bash
heroku config:set YOUTUBE_API_KEY=your_api_key_here
```

### For Docker:

```yaml
# docker-compose.yml
services:
  web:
    environment:
      - YOUTUBE_API_KEY=${YOUTUBE_API_KEY}
```

## 💰 API Quota Limits

YouTube Data API v3 has daily quotas:

- **Free Tier**: 10,000 units per day
- **Search request**: 100 units
- **Video details**: 1 unit

**Calculation:**

- Each video search (5 results) = ~105 units
- Daily limit: ~95 searches per day
- Enough for moderate usage

## 🔒 Security Best Practices

1. **Never commit API keys to Git:**

   ```bash
   # Add to .gitignore
   .env
   .streamlit/secrets.toml
   ```

2. **Restrict API key:**

   - Limit to YouTube Data API v3 only
   - Add HTTP referrer restrictions
   - Set application restrictions

3. **Monitor usage:**
   - Check Google Cloud Console regularly
   - Set up quota alerts
   - Implement caching to reduce API calls

## 🎯 Alternative: Embed Videos

If you don't want to use API, you can manually curate videos:

```python
def get_curated_videos(condition):
    """Manually curated educational videos"""

    if condition == "PNEUMONIA":
        return [
            {
                'title': 'Understanding Pneumonia',
                'video_id': 'dQw4w9WgXcQ',  # Replace with real video ID
                'channel': 'Medical Education',
                'embed_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'
            },
            # Add more curated videos
        ]

# Display embedded video
st.video(video['embed_url'])
```

## 📝 Current Status

The enhanced web app works **without YouTube API** using sample videos. This is perfect for:

- ✅ Development and testing
- ✅ Demo presentations
- ✅ Local deployment

To add real YouTube integration:

1. Get API key (5 minutes)
2. Update code (10 minutes)
3. Deploy with secrets (5 minutes)

**Total setup time: ~20 minutes**
