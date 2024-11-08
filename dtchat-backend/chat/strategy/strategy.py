from ..utils.connectors import dblp_conn, weather_conn, youtube_conn, guardian_conn, itunes_conn, hunter_conn

# 基类：所有策略类继承自这个类
class QueryStrategy:
    des = {}
    tools = []
    strategy = ""

    def get_tools(self):
        return self.tools
    
    def get_strategy(self):
        return self.strategy
    
    def get_des(self):
        return self.des
    
    async def execute(self, method_name, arguments):
        method = getattr(self, method_name, None)
        if method:
            return await method(arguments)
        else:
            raise NotImplementedError(f"Method '{method_name}' not implemented in {self.__class__.__name__}.")
    

# DBLP 策略类
class DblpQueryStrategy(QueryStrategy):
    strategy = "dblp_publications"

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_publications",
                "description": "get publication information through dblp api",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "q": {
                            "type": "string",
                            "description": "The keyword for generic query such as conference name or title of paper, e.g. CVPR 2020",
                        },
                        "author": {
                            "type": "string",
                            "description": "The name of a researcher, e.g. Andrew Y. Ng",
                        },
                        "count": {
                            "type": "integer",
                            "description": "The number of publications to return, default value 10",
                        }
                    },
                    "required": ["q", "author", "count"]
                },
            }
        },
    ]
        
    async def get_publications(self, arguments):
        q = arguments.get('q')
        author = arguments.get('author')
        count = arguments.get('count', 10)
        if author:
            df = await dblp_conn.query("publication", author=author, _count=count)
        else:
            df = await dblp_conn.query("publication", q=q, _count=count)
        data = df[["title", "authors", "venue", "year"]].reset_index(drop=True)
        return {"result": data.to_dict(orient='records'), "description": f"Publication Query Result for {q or author}", "have_schema": True}

# Weather 策略类
class WeatherQueryStrategy(QueryStrategy):
    strategy = "weather"

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "search real-time weather conditions based on the input address, returning local temperature, humidity, air pressure, wind speed, etc.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "q": {
                            "type": "string",
                            "description": "city or region name for weather query" 
                        }
                    },
                    "required": ["q"]
                }            
            },
        },
    ]
    async def get_weather(self, arguments):
        q = arguments.get('q')
        df = await weather_conn.query('weather', q=q)
        data = df[["description", "temp", "feels_like", "pressure", "humidity", "wind"]].reset_index(drop=True)
        return {"result": data.to_dict(orient='records'), "have_schema": False}

# YouTube 策略类
class YoutubeQueryStrategy(QueryStrategy):
    strategy = "youtube_videos"

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_videos",
                "description": "collect Youtube's video/channels.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "q": {
                            "type": "string",
                            "description": "keyword in video query, e.g. What are the top 10 Fitness Channels? Then Fitness is the q of this query" 
                        },
                        "type":{
                            "type": "string",
                            "description": "type of video query, e.g. What are the top 10 Fitness Channels? Then Channel is the type of this query" 
                        },
                        "count": {
                            "type": "integer",
                            "description": "The number of data to return, default value 10",
                        }
                    },
                    "required": ["q", "type", "count"]
                }            
            }
        },
    ]

    async def get_videos(self, arguments):
        q = arguments.get('q')
        type = arguments.get('type', 'video')
        count = arguments.get('count', 10)
        df = await youtube_conn.query('videos', q=q, part='snippet', type=type, _count=count)
        data = df[['title', 'description', 'channelTitle', 'publishTime']].reset_index(drop=True)
        return {"result": data.to_dict(orient='records'), "description": f"YouTube Query Result for {q}", "have_schema": True}

# Guardian 策略类
class GuardianQueryStrategy(QueryStrategy):
    strategy = "guardian_news"
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_news",
                "description": "search Guardian News/Articles Data by keyword.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "q": {
                            "type": "string",
                            "description": "keyword in news/articles query" 
                        },
                        "count": {
                            "type": "integer",
                            "description": "The number of data to return, default value 10",
                        }
                    },
                    "required": ["q", "count"]
                }            
            }
        },
    ]

    async def get_news(self, arguments):
        q = arguments.get('q')
        count = arguments.get('count', 10)
        df = await guardian_conn.query('article', _q=q, _count=count)
        return {"result": df.to_dict(orient='records'), "description": f"Guardian Query Result for {q}", "have_schema": True}

# iTunes 策略类
class ItunesQueryStrategy(QueryStrategy):
    strategy = "itunes_music"

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_itunes",
                "description": "collect iTune's Songs/MV MetaData.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "term": {
                            "type": "string",
                            "description": "keyword in Songs/MV query" 
                        },
                        "entity": {
                            "type": "string",
                            "enum": ["musicVideo", "movie", "song"],
                            "description": "expected return data type in query" 
                        },
                        "country": {
                            "type": "string",
                            "description": "country mentioned in user's query" 
                        },                    
                        "limit": {
                            "type": "integer",
                            "description": "The number of data to return, default value 10",
                        }
                    },
                    "required": ["term", "entity", "country", "limit"]
                }            
            }
        },
    ]

    async def get_itunes(self, arguments):
        term = arguments.get('term')
        entity = arguments.get('entity')
        country = arguments.get('country')
        limit = arguments.get('limit', 10)
        df = await itunes_conn.query('search', term=term, entity=entity, country=country, limit=limit)
        return {"result": df.to_dict(orient='records'), "description": f"iTunes Query Result for {term}", "have_schema": True}

class HunterQueryStrategy(QueryStrategy):
    strategy = "hunter_emails"

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_emails",
                "description": "Collect Professional Email Addresses",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "domain": {
                            "type": "string",
                            "description": "website domain in email query" 
                        },                  
                        "count": {
                            "type": "integer",
                            "description": "The number of data to return, default value 10",
                        }
                    },
                    "required": ["domain", "count"]
                }            
            }
        },
        {
            "type": "function",
            "function": {
                "name": "verify_email",
                "description": "Verify whether a provided email is valid",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email": {
                            "type": "string",
                            "description": "email to be verified" 
                        },                  
                    },
                    "required": ["email"]
                }            
            }
        },
    ]

    async def get_emails(self, arguments):
        domain = arguments.get('domain')
        count = arguments.get('count', 10)
        df = await hunter_conn.query('all_emails', domain=domain, _count=count)
        return {"result": df.to_dict(orient='records'), "description": f"hunter Query Result for {domain}", "have_schema": True}

    async def verify_email(self, arguments):
        email = arguments.get('email')
        df = await hunter_conn.query('email_verifier', email=email)
        return {"result": df.to_dict(orient='records'), "have_schema": False}