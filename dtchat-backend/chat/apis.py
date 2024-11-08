# import inspect
# from .strategy import *
# connectors = []
# for name, obj in inspect.getmembers(__import__('chat.strategy')):
#     if inspect.isclass(obj) and hasattr(obj, 'des'):
#         # 使用 `des` 的名称作为键，将实例化的connector
#         connectors.append(obj.des)
connectors = [
    {
        "type": "function",
        "function": {
            "name": "dblp_publications",
            "description": "get publication information through dblp api"
        }
    },
    {
        "type": "function",
        "function": {
            "name": "weather",
            "description": "search real-time weather conditions based on the input address, returning local temperature, humidity, air pressure, wind speed, etc."       
        }
    },
    {
        "type": "function",
        "function": {
            "name": "youtube_videos",
            "description": "collect Youtube's video content MetaData."          
        }
    },
    {
        "type": "function",
        "function": {
            "name": "guardian_news",
            "description": "collect Guardian's News/Articles Data."        
        }
    },
    {
        "type": "function",
        "function": {
            "name": "itunes_music",
            "description": "collect iTune's Songs/MV MetaData."         
        }
    },
    {
        "type": "function",
        "function": {
            "name": "hunter_emails",
            "description": "Collect and Verify Professional Email Addresses"          
        }
    },
]