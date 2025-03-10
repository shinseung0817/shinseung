import discord
import re
import os
from pymongo import MongoClient
import discord.utils
import datetime
import 금지어
import asyncio
import discord.ext.commands
bot = discord.Bot(intents=discord.Intents.all())
connection = MongoClient("mongodb+srv://shinseung0819:eoy803SuQanAX2p6@cluster0.zth9m.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
class dbf():
    def __init__(self,dbc):
        self.db = dbc
    async def insert(self,document):
        self.db.insert_one(document)
    def find(self,document):
        return self.db.find_one(document)
    async def update(self,document1,document2):
        self.db.update_one(document1,{"$set":document2})
    async def count(self,document):
        return self.db.count_documents(document)
    async def sort(self,document):
        return self.db.find().sort(document,-1)
@bot.event
async def on_message(message):
    db = dbf(connection.user.db)
    if await db.count({"id":message.author.id}) == False:
        await db.insert({"id":message.author.id,"warn":int(),"whitelist":bool(False),"beforemessage":str(),"count":0})
    else:
        
        if db.find({"id":message.author.id})["whitelist"] == True:
            return None
        else:
            if db.find({"id":message.author.id})['count'] == 0:
                await db.update({"id":message.author.id},{"beforemessage":message.content})
                await db.update({"id":message.author.id},{"count":db.find({"id":message.author.id})['count']+1})
            else:
                 if db.find({"id":message.author.id})['beforemessage'] == message.content:
                    await db.update({"id":message.author.id},{"count":db.find({"id":message.author.id})['count']+1})
                 else:
                        await db.update({"id":message.author.id},{"count":0})
                        await db.update({"id":message.author.id},{"beforemessage":message.content})
            if db.find({"id":message.author.id})['count'] == 6:
                 await db.update({"id":message.author.id},{"count":0})
                 await db.update({"id":message.author.id},{"beforemessage":None})
                 await message.author.timeout_for(datetime.timedelta(minutes=3))

            for i in range(len(금지어.금지어)):
                if re.search(금지어.금지어[i],str(message.content)) != None:
                    await message.author.timeout_for(datetime.timedelta(minutes=5))
@bot.event
async def on_message_delete(message):
    embed= discord.Embed(title="메세지 삭제 감지",description=f"{message.author.display_name}님이 **{message.content}**를 삭제하였습니다.")
    await bot.get_channel(1348285120704024696).send(embed=embed)
    return None
@bot.event
async def on_message_edit(before, after):
    embed= discord.Embed(title="메세지 수정 감지",description=f"{before.author.display_name}님이 **{before.content}**를 **{after.content}**로 수정하였습니다.")
    await bot.get_channel(1348285120704024696).send(embed =embed)
@bot.event
async def on_guild_role_create(role):
    embed = discord.Embed(title="역할 생성됨",description=f"{role.mention}이 생성되었습니다.")
    await bot.get_channel(1348289681065775105).send(embed =embed)
@bot.event
async def on_member_update(before,after):
    c = after.display_name
    embed = discord.Embed(title="역할 변경됨",description=f"{c}님의 역할이 변경되었습니다.")
    embed.add_field(name="변경 전",value=", ".join([str(r.mention) for r in before.roles]))
    embed.add_field(name="변경 후",value=", ".join([str(r.mention) for r in after.roles]))
    await bot.get_channel(1348289681065775105).send(embed =embed)
@bot.event
async def on_member_ban(guild, user):
        embed = discord.Embed(title="유저 영구추방됨",description=f"{user.display_name}님이 영구추방되었습니다.")
        await bot.get_channel(1348285131458084864).send(embed =embed)
@bot.event
async def on_member_kick(guild,user):
        embed = discord.Embed(title="유저 추방됨",description=f"{user.display_name}님이 추방되었습니다.")
        await bot.get_channel(1348285131458084864).send(embed =embed)
@bot.event
async def on_member_update(before, after):
    if after.timed_out == True:
        embed = discord.Embed(title="유저 타임아웃됨",description=f"{after.display_name}님이 타임아웃되었습니다.")
        await bot.get_channel(1348285131458084864).send(embed =embed)
@bot.event
async def on_guild_channel_create(channel):
        embed = discord.Embed(title="채널 생성됨",description=f"{channel.name} 채널이 생성되었습니다.")
        await bot.get_channel(1348289681065775105).send(embed =embed)
@bot.event
async def on_guild_channel_delete(channel):
        embed = discord.Embed(title="채널 삭제됨",description=f"{channel.name} 채널이 삭제되었습니다.")
        await bot.get_channel(1348289681065775105).send(embed =embed)
@bot.event
async def on_guild_channel_update(before, after):
    if before.name == after.name:
        return None
    else:
        embed = discord.Embed(title="채널 이름 변경됨",description=f"채널의 이름이 변경되었습니다.")
        embed.add_field(name="변경 전",value=before.name)
        embed.add_field(name="변경 후",value=after.name)
        await bot.get_channel(1348289681065775105).send(embed =embed)
@bot.event
async def on_ready():
    bot.add_view(view())
    bot.add_view(view2())
class view2(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # timeout of the view must be set to None
    @discord.ui.button(label="닫기", row=0, style=discord.ButtonStyle.gray,custom_id="1")
    async def first_button_callback(self, button, interaction):
        await interaction.channel.edit(name=f"{interaction.channel.name} - 닫힘")
        await interaction.respond("티켓이 성공적으로 닫혔습니다.")
    @discord.ui.button(label="제거", row=0, style=discord.ButtonStyle.red,custom_id="2")
    async def s_button_callback(self, button, interaction):

        await interaction.respond("5초 뒤 티켓을 제거합니다..")
        await asyncio.sleep(5)
        await interaction.channel.delete()
class view(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # timeout of the view must be set to None
    @discord.ui.button(label="문의하기", row=0, style=discord.ButtonStyle.primary,custom_id="4")
    async def second_button_callback(self, button, interaction):
        role = bot.get_guild(1345036705622786119).get_role(1348289977536221214)
        everyone = discord.utils.get(bot.get_guild(1345036705622786119).roles,name="@everyone")
        user = bot.get_user(interaction.user.id)
        overwrites = {
            role: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            everyone : discord.PermissionOverwrite(view_channel=False, send_messages=False, read_message_history=False)
        }
        embed = discord.Embed(title = "문의하기",description="곧 한국재단 수뇌부가 도착할것입니다 조금만 기다려주세요 <@1339084836706451517>")
        a = await bot.get_guild(1345036705622786119).create_text_channel(name=f"{interaction.user.name}-문의하기",overwrites=overwrites)
        await a.send(embed=embed,view=view2())
        await interaction.respond("티켓이 성공적으로 열렸습니다.", ephemeral=True)
@bot.command(name="경고")
@discord.ext.commands.has_permissions(administrator=True)
async def 경고(ctx,개수:int,user:discord.Member):
     
     db = dbf(connection.user.db)
     a= int(db.find({"id":user.id})['warn'])
     print(a)
     if a+개수 !=5 or a+개수 !=10 or a+개수 !=15 or a+개수 !=20:
         embed= discord.Embed(title="경고 처리됨",description=f"{user.display_name} 님에게 {개수}개 경고가 지급되었습니다.")
         await db.update({"id":user.id},{"warn":a+개수})
         await ctx.respond(embed=embed)
         await bot.get_channel(1348285131458084864).send(embed =embed)
         if a+개수 ==5:
            embed = discord.Embed(title="유저 경고 누적됨",description=f"{user.display_name} 유저 경고가 5회 누적되어 1일 타임아웃 처리되었습니다.")
            await ctx.respond(embed=embed)
            await user.timeout_for(datetime.timedelta(days=1))
            await bot.get_channel(1348285131458084864).send(embed =embed)
         if a+개수 ==10:
            embed = discord.Embed(title="유저 경고 누적됨",description=f"{user.display_name} 유저 경고가 10회 누적되어 1주일 타임아웃 처리되었습니다.")
            await ctx.respond(embed=embed)
            await user.timeout_for(datetime.timedelta(weeks=1))
            await bot.get_channel(1348285131458084864).send(embed =embed)
         if a+개수 ==15:
            embed = discord.Embed(title="유저 경고 누적됨",description=f"{user.display_name} 유저 경고가 15회 누적되어 역할이 모두 해임되었습니다.")
            await ctx.respond(embed=embed)
            await user.remove_roles()
            await bot.get_channel(1348285131458084864).send(embed =embed)
         if a+개수 ==20:
            embed = discord.Embed(title="유저 경고 누적됨",description=f"{user.display_name} 유저 경고가 20회 누적되어 벤 처리되었습니다.")
            await ctx.respond(embed=embed)
            await user.ban()
            await bot.get_channel(1348285131458084864).send(embed =embed)
@bot.command(name="공지")
@discord.ext.commands.has_permissions(administrator=True)
async def 공지(ctx,text):
     await bot.get_channel(1345321936682749972).send(text)
     embed = discord.Embed(title="공지 전송됨",description="공지가 전송되었습니다.")
     await ctx.respond(embed=embed)
@bot.command(name="버튼생성")
@discord.ext.commands.has_permissions(administrator=True)
async def mkbutton(ctx):
    embed = discord.Embed(title = "티켓 열기", description="아래 버튼을 눌러 티켓을 생성하세요.")
    await ctx.send(view=view(),embed= embed)
@bot.command(name="화이트리스트추가")
@discord.ext.commands.has_permissions(administrator=True)
async def 화리추가(ctx,user:discord.Member):
     db = dbf(connection.user.db)
     await db.update({"id":user.id},{"whitelist":True})
     embed = discord.Embed(title="화이트리스트 추가됨",description=f"{user.display_name}님의 화이트리스트가 추가되었습니다.")
     await ctx.respond(embed=embed)
@bot.command(name="화이트리스트제거")
@discord.ext.commands.has_permissions(administrator=True)
async def 화리제거(ctx,user:discord.Member):
     db = dbf(connection.user.db)
     await db.update({"id":user.id},{"whitelist":False})
     embed = discord.Embed(title="화이트리스트 제거됨",description=f"{user.display_name}님의 화이트리스트가 해제되었습니다.")
     await ctx.respond(embed=embed)
bot.run(봇 토큰)