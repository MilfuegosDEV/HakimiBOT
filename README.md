# HakimiBOT

Welcome to the HakimiBot project! We're utilizing the [PyCord](https://pycord.dev/) framework to develop our Discord Bot.

## Description

HakimiBOT is similar to other bots, but it's designed to be eager to assist you with your tasks anytime.

## Getting Started

### Dependencies

- [PyCord](https://pycord.dev/)
- [pytz](https://pythonhosted.org/pytz/)

### Installation

To install all the required dependencies, please use the following command:

```bash
pip install -r requirements.txt
```

### Execution
* Fill out the necessary information in [config.json](config.json):
```json
{
    "debug_guilds": [], 
    "token": ""
}
```

> Please read: [how to find the server's ID?](https://www.alphr.com/discord-find-server-id/) and then insert the server ID(s) into the "debug_guilds" array.

> "token" is a reference to the bot's secret token.

* Run the program.

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

