# HakimiBOT

Welcome to the HakimiBot project! We're utilizing the [PyCord](https://pycord.dev/) framework to develop our Discord Bot.

## Description

HakimiBOT is similar to other bots, but it's designed to be eager to assist you with your tasks anytime.

## Getting Started

### Dependencies

- [PyCord](https://pycord.dev/)
- [pytz](https://pythonhosted.org/pytz/)
- [Spotipy](https://spotipy.readthedocs.io/en/2.22.1/)
- [lyricsgenius](https://lyricsgenius.readthedocs.io/en/master/)


### Installation

To install all the required dependencies, please use the following command:

```bash
pip install -r requirements.txt
```

#### Insert all credentials into [config.json](config.json)
```json
{
    "spotifyApi": {
        "ClientID": "", 
        "ClientSecret": "" 
    },
    "discord":{
        "debug_guilds": [], 
        "token": "" 
    },
    "GeniusAPI": {
        "token": "" 
    }
}
```
> ##### Do you need help? Consult this

> - Discord: https://discord.com/developers/docs/getting-started#configuring-your-bot
> - GeniusAPI: *https://docs.genius.com/
> - Spotify: https://developer.spotify.com/documentation/web-api

### Creating an Embed Message.

* Here's an example of usage:

```python 
from embedBuilder import EmbedConstructor

embed_info = {
    "title": "Title of the Embed",
    "description": "Description of the Embed",
    "color": discord.Color.blue(),
    "timestamp": "now",
    "fields": [
        {
            "name": "Field 1",
            "value": "Value 1",
            "inline": False
        },
        {
            "name": "Field 2",
            "value": "Value 2",
            "inline": True
        }
    ],
    "author": {
        "name": "Author",
        "url": "https://example.com",
        "icon_url": "https://example.com/icon.png"
    },
    "footer": {
        "text": "Footer Text",
        "icon_url": "https://example.com/footer_icon.png"
    },
    "image": {
        "url": "https://example.com/image.png"
    },
    "thumbnail": {
        "url": "https://example.com/thumbnail.png"
    }
}

embed_constructor = EmbedConstructor(embed_info)
embed = embed_constructor.get_embed()

```
> You only need to fill in the information that you want to include.
