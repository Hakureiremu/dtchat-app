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
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_youtube",
            "description": "collect Youtube's video content MetaData.",
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
    {
        "type": "function",
        "function": {
            "name": "collect_guardian",
            "description": "collect Guardian's News/Articles Data.",
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
    {
        "type": "function",
        "function": {
            "name": "collect_itunes",
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
    {
        "type": "function",
        "function": {
            "name": "collect_emails",
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
]