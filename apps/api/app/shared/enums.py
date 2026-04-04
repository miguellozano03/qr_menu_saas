from enum import Enum

class LinkType(str, Enum):
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    TIKTOK = "tiktok"
    TWITTER = "twitter"
    YOUTUBE = "youtube"
    WHATSAPP = "whatsapp"
    WEBSITE = "website"
    OTHER = "other"