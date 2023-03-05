import pickle
from random import choice
# from time import sleep
import discord
from bs4 import BeautifulSoup
import math
import urllib.request

# ---------------------------------------Scramble dict---------------------------------------
# reading scramble file
file = open(r"data.pkl", "rb")
# dat.pkl
# D:\Desktop\Things\WCA\dat.pkl
scramble_dict = pickle.load(file)
file.close()
# file=0
# ---------------------------------------Scramble dict---------------------------------------





# ---------------------------------------Functions---------------------------------------

# reads competition info
def get_comp(events="all",region="UK",comp_type="all"):
    """
    Return a list of tuple of the form ("comp-name","comp-location","comp-date")
    type: on, upcoming, all
    """
    
    "https://www.worldcubeassociation.org/competitions" 
    data1=urllib.request.Request("https://www.worldcubeassociation.org/competitions?region=United+Kingdom&search=&state=present&year=all+years&from_date=&to_date=&delegate=&show_registration_status=on&display=list", headers={'User-Agent': 'User-Agent:Mozilla/5.0'})
    content=urllib.request.urlopen(data1).read().decode(encoding='utf-8')
    bs=BeautifulSoup(content,"html.parser")
    if comp_type=="on":
        try:
            comps_on=bs.find(class_="col-md-12",id=("in-progress-comps")).find(class_="list-group").find_all(class_="list-group-item not-past")
        except:
            return [("Null","Null","Null")]
    elif comp_type=="upcoming":
        comps_on=bs.find(class_="col-md-12",id=("upcoming-comps")).find(class_="list-group").find_all(class_="list-group-item not-past")

    else:
        comps_on=[]
        comps_on+=bs.find(class_="col-md-12",id=("upcoming-comps")).find(class_="list-group").find_all(class_="list-group-item not-past")
        try:
            ongoningcomps=bs.find(class_="col-md-12",id=("in-progress-comps")).find(class_="list-group").find_all(class_="list-group-item not-past")
            comps_on+=ongoningcomps
        except:
            pass

    comp_info=[]
    for each in comps_on:
        comp_name=each.find("a",href=True).contents[0]
        comp_loc=each.find(class_="location").contents
        comp_location=comp_loc[1].contents[0]+comp_loc[2][:-9]
        comp_date=each.find(class_="date").contents[2][8:-7]
        l=each.contents[1].contents[1]
        if "red" in l["class"]:
            status="closed"
        elif "orange" in l["class"]:
            status="full"
        elif "green" in l["class"]:
            status="open"
        elif "blue" in l["class"]:
            status=l["title"]
        comp_info.append((comp_name,comp_location,comp_date,status))
    return comp_info

# the function the reads message and gives return
def reader(mess):
    # separating sentence
    contents=mess.split(" ")
    contents=[i for i in contents if i!=""]
    # scrambles
    events_map={
        ".3":"333",
        ".333":"333",
        ".4":"444",
        ".444":"444",
        ".5":"555",
        ".555":"555",
        ".6":"666",
        ".666":"666",
        ".7":"777",
        ".777":"777",
        ".clock":"clock",
        ".cl":"clock",
        ".pyr":"pyram",
        ".pyram":"pyram",
        ".py":"pyram",
        ".p":"pyram",
        ".mega":"minx",
        ".minx":"minx",
        ".skewb":"skewb",
        ".sk":"skewb",
        ".sq":"sq1",
        ".sq1":"sq1",
    }
    # First function: getting scrambles of WCA cubes
    if contents[0] in events_map.keys():
        try:
            num=int(contents[1])
        except:
            num=1
        scrambles=[]
        
        for i in range(num):
            while True:
                scr=choice(scramble_dict[events_map[contents[0]]])
                if not scr in scrambles:
                    scrambles.append(scr)
                    break
        txt=""
        for i in range(num):
            txt+=f"{i+1}. {scrambles[i]}\n"
        return txt[:-1]
    # second function: get WCA competition information
    elif contents[0]==".comp":
        comp_list=get_comp()
        txt="10 Recent competitions:\n"
        comp_list=comp_list[:10]
        for i in range(len(comp_list)):
            each=comp_list[i]
            txt+=f"{i+1}. {each[0]} | {each[1]} | {each[2]} | {each[3]}\n"
        return txt[:-1]
    else:
        return None

# ---------------------------------------Functions---------------------------------------










# ---------------------------------------login---------------------------------------
mode=int(input("Mode:"))
key=int(input("Key:"))
fac=(1/mode+1/(key**2+3.14159))+mode/1.3
content="bkR'uMTrAxt4kMvTAtIydNjxfEnyyMzPUCO3NgzVYqD5M jgFIswuMQnp. GuwUnUCcC1w.Wi8lXsG0CBj1dsNyrMRiSHBIvjsCM_ZiVopRzRbJfT1uHqTrgCvpLXDuLFGkfzpxpjgL0vM2oz9Y8'E"
sequence=[]
fac=(1/mode+1/(key**2+3.14159))+mode/1.3
len1=len(content)
len2=int(len(content)/ mode)
for n in range(0,len1):
    preout=int(n*fac+fac/(n+1)+n**2+math.sin(n))   
    out=preout%mode
    sequence.append(out)
cftable="0"*len2
cftable1=list(cftable)
for i in range(0,len2):
    x=i*mode+int(sequence[i])
    cftable1[i]=content[x]
content="".join(cftable1)
content=content[3:-1]
print(content)
print("MTA4MTAyNjEyMzU3NzY5MjIwMQ.GuUUC1.8XG0j1srRSBvsC_ioRbf1HTrCpXuFfpxg0M298")
# ---------------------------------------login---------------------------------------








# ---------------------------------------Bot Init---------------------------------------

# intents决定了机器人能干什么，default为默认，后续代码将向intents添加权限
intents = discord.Intents.default()
intents.members = True # bot可以访问群员列表和进行相关操作
intents.messages=True # bot可以发送接收消息
intents.message_content=True #bot可以查看消息
intents.voice_states=True
#intents.move_members=True
TOKEN = content
GUILD = "H2O"
client = discord.Client(intents=intents)
# ---------------------------------------Bot Init---------------------------------------


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    # for guild in client.guilds:
    #     print(guild.id)



'''
@client.event
async def on_ready():
    for guild in client.guilds:
        
        if guild.name == '???':
            print(guild.name)
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    #print(f'Guild Members:\n - {members}')
    for i in guild.members:
        #print(i.name,'-',i.id)

'''

@client.event
async def on_message(message):
    #print(message.content)
    result=reader(message.content)
    #print(result)
    if result is not None:
        await message.channel.send(result)
    
# @client.event
# async def on_voice_state_update(member, before, after):
#     
#     member_x=GUId.get_member(id)
#     member_y=GUId.get_member()#wo
#     status=member_y.voice
#     # if status.channel!=chufang:
#     #     await member_x.move_to(chufang)
#     #     print("!!!!")
#     # status=member_y.voice
#     if status.channel!=main_channel:
#         await member_y.move_to(None)
#         print("!!!!")
client.run(TOKEN)
