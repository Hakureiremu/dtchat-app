from dataprep.connector import connect

# 各种第三方API连接
dblp_conn = connect("dblp")
itunes_conn = connect("itunes")
weather_conn = connect("openweathermap", _auth={'access_token': 'a59917f8806b7123f8b103bc2d4afe30'})
youtube_conn = connect('youtube', _auth={'access_token': 'AIzaSyAEvuXqZE4FZTllSSZGfWMvfbIfvxZYVCo'})
guardian_conn = connect('guardian', _auth={'access_token': 'a3378fb0-4b4e-4f72-890d-955f994527ba'})
hunter_conn = connect("hunter", _auth={"access_token":'889bad75b2222f069c1f402578382f68d3e6b5aa'})


# What publications have Ziyao Wang published in recent years? 
# What is the weather like in Singapore today? 
# Is there any news or articles related to US election? 
# How to get songs of Jay Chou published in China? 
# What are the top 10 Fitness Channels on Youtube?
# Who are executives of asana.com and what are their emails?
# Is this email dustin@asana.com valid?

# API service Provider chapter2 

# chapter 3 add a overall 
