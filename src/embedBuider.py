import discord
from datetime import datetime
from pytz import timezone

class EmbedConstructor:
    """
    A utility class for constructing Discord embeds based on a provided dictionary.

    Parameters:
        info (dict): A dictionary containing the configuration details for the embed.
    """

    def __init__(self, info:dict):
        """
        Initializes an instance of the EmbedConstructor class.

        Parameters:
            info (dict): A dictionary containing the configuration details for the embed.
        """
        self.embed = discord.Embed(
            title=info.get("title", None),
            description=info.get("description", None),
            color=info.get("color", discord.Color.default())
        )

        if "timestamp" in info:
            timestamp = info["timestamp"]
            if timestamp == "now":
                timestamp = datetime.now(timezone("UTC"))
            self.embed.timestamp = timestamp

        if "fields" in info:
            fields = info["fields"]
            for field in fields:
                name = field.get("name", None)
                value = field.get("value", None)
                inline = field.get("inline", True)
                self.embed.add_field(name=name, value=value, inline=inline)

        if "author" in info:
            author = info["author"]
            name = author.get("name", None)
            url = author.get("url", None)
            icon_url = author.get("icon_url", '')
            self.embed.set_author(name=name, url=url, icon_url=icon_url)

        if "footer" in info:
            footer = info["footer"]
            text = footer.get("text", None)
            icon_url = footer.get("icon_url", '')
            self.embed.set_footer(text=text, icon_url=icon_url)

        if "image" in info:
            image = info["image"]
            url = image.get("url", '')
            self.embed.set_image(url=url)

        if "thumbnail" in info:
            thumbnail = info["thumbnail"]
            url = thumbnail.get("url", '')
            self.embed.set_thumbnail(url=url)

    def get_embed(self):
        """
        Returns the constructed Discord embed.

        Returns:
            discord.Embed: The constructed Discord embed.
        """
        return self.embed