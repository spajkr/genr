#########################################################
#                     IMPORTS
#########################################################

import discord
import random
from discord import app_commands
import sqlite3
from colorama import Fore
from discord.utils import get
import yaml
from dotenv import load_dotenv
import os
import datetime
import time

load_dotenv()
#########################################################
#              GET FROM CONFIG
#########################################################

def get_embed_color():
    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config['embedColor']

def get_embed_footer_text():
    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config['embedFooterText']

def get_embed_footer_icon_url():
    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config['embedFooterIconUrl']

def get_admin_role_id():
    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config['administrationRoleID']

def get_nopermission():
    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config['noPermission']

def get_extreme_rank():
    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config['ExtremeGenRole']

def get_premium_rank():
    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config['PremiumGenRole']

def get_free_cooldown():
    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config['FreeGenCoolDown']

def get_premium_cooldown():
    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config['PremiumGenCoolDown']

def get_extreme_cooldown():
    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config['ExtremeGenCoolDown']

#########################################################
#                 LINES
#########################################################

def get_line_count(file_path):
    with open(file_path, 'r') as file:
        line_count = sum(1 for _ in file)
    return line_count

def get_random_line(file_path):
    with open(file_path, 'r+') as file:
        lines = file.readlines()
        if lines:
            random_line = random.choice(lines).strip()
            file.seek(0)
            file.truncate()
            for line in lines:
                if line.strip() != random_line:
                    file.write(line)
            return random_line
    return None

# Write new line
def write_new_line(file_path, line):
    with open(file_path, 'a') as file:
        verifylines = get_line_count(file_path)
        if verifylines == 0:
            file.write(line)
        else:
            file.write('\n' + line)

#########################################################
#                    SQLITE3
#########################################################

conn = sqlite3.connect('database3.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS cooldown (
                    userID INTEGER,
                    timestamp DATETIME)''')

conn.commit()

#########################################################
#                    CLIENT STARTUP
#########################################################
class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False
    
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            print (Fore.RED + "Starting the bot please wait....")
            #await tree.sync() # reload slsh command
            self.synced = True  
            print ( Fore.BLACK + "------------------------------------------------------")
            print ( Fore.MAGENTA + "We started bot!.")
            print ( "Congratulations! ")
            print ( Fore.BLACK + "------------------------------------------------------")
            print ( Fore.WHITE + "")
#########################################################
#                    VARIABLES
#########################################################
client = aclient()
tree = app_commands.CommandTree(client)
nopermission = get_nopermission()
#########################################################
#                    COMMANDS
#########################################################


@tree.command(name="gen", description="blabla")
@app_commands.choices(account=[
    app_commands.Choice(name="[Free] Crunchyroll", value="crunchyroll"),
    app_commands.Choice(name="[Free] Deezer", value="deezer"),
    app_commands.Choice(name="[Free] EmailFA", value="emailfa"),
    app_commands.Choice(name="[Free] Fox", value="fox"),
    app_commands.Choice(name="[Free] GeoGuesser", value="geoguesser"),
    app_commands.Choice(name="[Extreme] NordVPN", value="nordvpn"),
    app_commands.Choice(name="[Extreme] Paramount", value="paramount"),
    app_commands.Choice(name="[Extreme] UFC", value="ufc"),
    app_commands.Choice(name="[Extreme] Pufelix", value="pufelix"),
    app_commands.Choice(name="[Extreme] Funimation", value="funimation"),
    app_commands.Choice(name="[Premium] BWW", value="bww"),
    app_commands.Choice(name="[Premium] Disney", value="disney"),
    app_commands.Choice(name="[Premium] Kahoot", value="kahoot"),
    app_commands.Choice(name="[Premium] Valorant", value="valorant"),
    app_commands.Choice(name="[Premium] Voyo", value="voyo"),
])
async def generator(interaction: discord.Integration, account: app_commands.Choice[str]):
    #--------------------cooldown checker-----------------------
    notindatabase1 = "None"

    conn = sqlite3.connect('database3.db')
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp FROM cooldown WHERE userID = ?", (interaction.user.id,))
    result = cursor.fetchone()

    if result is not None:
        timestamp = datetime.datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S.%f")
        current_timestamp = datetime.datetime.now()

        if current_timestamp < timestamp:
            await interaction.response.send_message(f"Please wait you are on cooldown until **{timestamp}**!", ephemeral=True)
            return
        
        notindatabase1 = "false"
    if result is None:
        notindatabase1 = "true"
    
    extreme_rank = get(interaction.guild.roles, name=get_extreme_rank())
    premium_rank = get(interaction.guild.roles, name=get_premium_rank())

    if premium_rank or extreme_rank not in interaction.user.roles:
        cooldown = get_free_cooldown()
    
    if premium_rank in interaction.user.roles:
        cooldown = get_premium_cooldown()

    if extreme_rank in interaction.user.roles:
        cooldown = get_extreme_cooldown()
    #--------------------cooldown checker-----------------------


    # Free
    if account.value == "crunchyroll" or "deezer" or "emailfa" or "fox" or "geoguesser":
        verifylines = get_line_count("stock/" + account.value + ".txt")
        if verifylines == 0:
            await interaction.response.send_message(f"**{account.value}** is out of stock :(")
            return
        
        randomaccount = get_random_line("stock/" + account.value + ".txt")
        embed = discord.Embed(title=f"Generation of {account.value} accounts!", description=f"Here is your generated account: ```{randomaccount}```", color=int(get_embed_color(), 16))
        embed.set_footer(text=get_embed_footer_text(), icon_url=get_embed_footer_icon_url())
        member = interaction.user
        await member.send(embed=embed)
        embed1 = discord.Embed(title=f"Generated!", description=f"Generation of **{account.value}** was successfull :white_check_mark: \n Check your DMS", color=int(get_embed_color(), 16))
        embed1.set_footer(text=get_embed_footer_text(), icon_url=get_embed_footer_icon_url())
        await interaction.response.send_message(embed=embed1)

        current = datetime.datetime.now()
        b = current + datetime.timedelta(0,cooldown)
        timestamp = b

        
        if notindatabase1 == "true":
            cursor.execute("INSERT INTO cooldown (userID, timestamp) VALUES (?, ?)", (interaction.user.id, timestamp))
            conn.commit()
        else:
            cursor.execute("UPDATE cooldown SET timestamp = ? WHERE userID = ?", (timestamp, interaction.user.id))
            conn.commit()
        return



    # Extreme
    if account.value == "nordvpn" or "paramount" or "ufc" or "pufelix" or "funimation":
        verifylines = get_line_count("stock/" + account.value + ".txt")
        if verifylines == 0:
            await interaction.response.send_message(f"**{account.value}** is out of stock :(")
            return
        
        randomaccount = get_random_line("stock/" + account.value + ".txt")
        embed = discord.Embed(title=f"Generation of {account.value} accounts!", description=f"Here is your generated account: ```{randomaccount}```", color=int(get_embed_color(), 16))
        embed.set_footer(text=get_embed_footer_text(), icon_url=get_embed_footer_icon_url())
        member = interaction.user
        await member.send(embed=embed)
        embed1 = discord.Embed(title=f"Generated!", description=f"Generation of **{account.value}** was successfull :white_check_mark: \n Check your DMS", color=int(get_embed_color(), 16))
        embed1.set_footer(text=get_embed_footer_text(), icon_url=get_embed_footer_icon_url())
        await interaction.response.send_message(embed=embed1)

        current = datetime.datetime.now()
        b = current + datetime.timedelta(0,cooldown)
        timestamp = b

        
        if notindatabase1 == "true":
            cursor.execute("INSERT INTO cooldown (userID, timestamp) VALUES (?, ?)", (interaction.user.id, timestamp))
            conn.commit()
        else:
            cursor.execute("UPDATE cooldown SET timestamp = ? WHERE userID = ?", (timestamp, interaction.user.id))
            conn.commit()
        return
    # Premium
    if account.value == "bww" or "disney" or "kahoot" or "valorant" or "voyo":
        verifylines = get_line_count("stock/" + account.value + ".txt")
        if verifylines == 0:
            await interaction.response.send_message(f"**{account.value}** is out of stock :(")
            return
        
        randomaccount = get_random_line("stock/" + account.value + ".txt")
        embed = discord.Embed(title=f"Generation of {account.value} accounts!", description=f"Here is your generated account: ```{randomaccount}```", color=int(get_embed_color(), 16))
        embed.set_footer(text=get_embed_footer_text(), icon_url=get_embed_footer_icon_url())
        member = interaction.user
        await member.send(embed=embed)
        embed1 = discord.Embed(title=f"Generated!", description=f"Generation of **{account.value}** was successfull :white_check_mark: \n Check your DMS", color=int(get_embed_color(), 16))
        embed1.set_footer(text=get_embed_footer_text(), icon_url=get_embed_footer_icon_url())
        await interaction.response.send_message(embed=embed1)

        current = datetime.datetime.now()
        b = current + datetime.timedelta(0,cooldown)
        timestamp = b

        
        if notindatabase1 == "true":
            cursor.execute("INSERT INTO cooldown (userID, timestamp) VALUES (?, ?)", (interaction.user.id, timestamp))
            conn.commit()
        else:
            cursor.execute("UPDATE cooldown SET timestamp = ? WHERE userID = ?", (timestamp, interaction.user.id))
            conn.commit()
        return



@tree.command(name="stock", description="stock command description")
async def stock(interaction: discord.Integration):
    crunchyroll_lines = get_line_count('stock/crunchyroll.txt')
    deezer_lines = get_line_count('stock/deezer.txt')
    emailfa_lines = get_line_count('stock/emailfa.txt')
    fox_lines = get_line_count('stock/fox.txt')
    geoguesser_lines = get_line_count('stock/geoguesser.txt')

    bww_lines = get_line_count('stock/bww.txt')
    disney_lines = get_line_count('stock/disney.txt')
    kahoot_lines = get_line_count('stock/kahoot.txt')
    valorant_lines = get_line_count('stock/valorant.txt')
    voyo_lines = get_line_count('stock/voyo.txt')

    nordvpn_lines = get_line_count('stock/nordvpn.txt')
    paramount_lines = get_line_count('stock/paramount.txt')
    ufc_lines = get_line_count('stock/ufc.txt')
    pufelix_lines = get_line_count('stock/pufelix.txt')
    funimation_lines = get_line_count('stock/funimation.txt')

    embed = discord.Embed(title="Stock Gen server", description="Stock command:", color=int(get_embed_color(), 16))
    embed.add_field(name="**Free**", value=f"Crunchyroll: **{crunchyroll_lines}**\nDeezer: **{deezer_lines}**\nEmailFA: **{emailfa_lines}**\nFox: **{fox_lines}**\nGeoGuesser: **{geoguesser_lines}**", inline=False)
    embed.add_field(name="**Premium**", value=f"BWW: **{bww_lines}**\nDisney: **{disney_lines}**\nKahoot: **{kahoot_lines}**\nValorant: **{valorant_lines}**\nVoyo: **{voyo_lines}**", inline=False)
    embed.add_field(name="**Extreme**", value=f"NordVPN: **{nordvpn_lines}**\nParamount: **{paramount_lines}**\nUFC: **{ufc_lines}**\nPufelix: **{pufelix_lines}**\nFunimation: **{funimation_lines}**", inline=False)
    embed.set_footer(text=get_embed_footer_text(), icon_url=get_embed_footer_icon_url())
    await interaction.response.send_message(embed=embed)

@tree.command(name="add", description="blabla")
@app_commands.choices(account=[
    app_commands.Choice(name="Crunchyroll", value="crunchyroll"),
    app_commands.Choice(name="Deezer", value="deezer"),
    app_commands.Choice(name="EmailFA", value="emailfa"),
    app_commands.Choice(name="Fox", value="fox"),
    app_commands.Choice(name="GeoGuesser", value="geoguesser"),
    app_commands.Choice(name="NordVPN", value="nordvpn"),
    app_commands.Choice(name="Paramount", value="paramount"),
    app_commands.Choice(name="UFC", value="ufc"),
    app_commands.Choice(name="Pufelix", value="pufelix"),
    app_commands.Choice(name="Funimation", value="funimation"),
    app_commands.Choice(name="BWW", value="bww"),
    app_commands.Choice(name="Disney", value="disney"),
    app_commands.Choice(name="Kahoot", value="kahoot"),
    app_commands.Choice(name="Valorant", value="valorant"),
    app_commands.Choice(name="Voyo", value="voyo"),
])
async def add(interaction: discord.Integration, account: app_commands.Choice[str], text: str):
    adminrole = get(interaction.guild.roles, name=get_admin_role_id())
    if adminrole in interaction.user.roles:
        if '\n' in text:
            await interaction.response.send_message("Symbol **\n** is disabled for buggy actions.")
        write_new_line("stock/" + account.value + ".txt", text)
        await interaction.response.send_message(f"Adding to **{account.value}** account **{text}** :white_check_mark: ", ephemeral=True)
    else:
        await interaction.response.send_message(nopermission, ephemeral=True)

@tree.command(name="drop", description="blabla")
@app_commands.choices(account=[
    app_commands.Choice(name="Crunchyroll", value="crunchyroll"),
    app_commands.Choice(name="Deezer", value="deezer"),
    app_commands.Choice(name="EmailFA", value="emailfa"),
    app_commands.Choice(name="Fox", value="fox"),
    app_commands.Choice(name="GeoGuesser", value="geoguesser"),
    app_commands.Choice(name="NordVPN", value="nordvpn"),
    app_commands.Choice(name="Paramount", value="paramount"),
    app_commands.Choice(name="UFC", value="ufc"),
    app_commands.Choice(name="Pufelix", value="pufelix"),
    app_commands.Choice(name="Funimation", value="funimation"),
    app_commands.Choice(name="BWW", value="bww"),
    app_commands.Choice(name="Disney", value="disney"),
    app_commands.Choice(name="Kahoot", value="kahoot"),
    app_commands.Choice(name="Valorant", value="valorant"),
    app_commands.Choice(name="Voyo", value="voyo"),
])
async def drop(interaction: discord.Integration, account: app_commands.Choice[str]):
    adminrole = get(interaction.guild.roles, name=get_admin_role_id())
    if adminrole in interaction.user.roles:
        txtverify = "stock/" + account.value + ".txt"
        verifylines = get_line_count(txtverify)
        if verifylines == 0:
            await interaction.response.send_message(f"**{account.value}** is out of stock :(", ephemeral=True)
            return

        await interaction.response.send_message(f"Generating random account from {account.value}. Be Ready in **10 seconds!** :yum:")
        randomaccount = get_random_line("stock/" + account.value + ".txt")
        time.sleep(10)
        embed = discord.Embed(title="Random Account!", description=f"Random account from **{account.value}** is ```{randomaccount}```", color=int(get_embed_color(), 16))
        embed.set_footer(text=get_embed_footer_text(), icon_url=get_embed_footer_icon_url())
        await interaction.edit_original_response(content=" ", embed=embed)
    else:
        await interaction.response.send_message(nopermission, ephemeral=True)

@tree.command(name="help", description="blabla")
async def help(interaction: discord.Integration):
    embed = discord.Embed(title="Gen Commands Helper", description="Commands for this server:", color=int(get_embed_color(), 16))
    embed.add_field(name="/stock", value="command", inline=False)
    embed.add_field(name="/gen", value="command", inline=False)
    embed.add_field(name="/add", value="command", inline=False)
    embed.add_field(name="/drop", value="command", inline=False)
    embed.add_field(name="/help", value="command", inline=False)
    embed.set_footer(text=get_embed_footer_text(), icon_url=get_embed_footer_icon_url())
    await interaction.response.send_message(embed=embed)

token = os.getenv('TOKEN')
client.run(token)