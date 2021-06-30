import discord
import os
from discord.ext import commands, tasks
import io
import aiohttp
from keep_alive import keep_alive

channel_id=857050945627226133 #id of the discord channel to post 
bot = commands.Bot(command_prefix="/" , help_command = None)
    

@bot.command()
@commands.has_role("👮Staff") # Checks if a user post a command to bot has specific role attached
async def post(context, *, msg):
    embed=discord.Embed(
        title= "Post command",
        description = "Command to post messages in announcement room"
    )
    channel = bot.get_channel(channel_id)
    last_line = get_last_line(msg)
    if (last_line == True):
        #Variables
      img_url = get_url(msg)
      new_msg = remove_image_url(msg)
        #Process
      await channel.send(new_msg)
      print(channel)
      async with aiohttp.ClientSession() as session:
        async with session.get(img_url) as resp:
            if resp.status != 200:
                return await channel.send('Could not download file...')
            data = io.BytesIO(await resp.read())
            channel = bot.get_channel(channel_id)
            await channel.send(file=discord.File(data, 'Bsides_img.png'))
    else: await channel.send(msg)



@tasks.loop(hours=336.0) # 14*24 i.e 2 weeks time
async def huddle_reminder():
  await bot.wait_until_ready()

  channel = bot.get_channel(channel_id)
  reminder_message= (":loudspeaker: @everyone Fortnightly GupShup call at 6PM tonight.") 
  reminder_message_giff= ("https://media.discordapp.net/attachments/736609006553923688/858632867068248084/Friendly_Reminder.gif")
  await channel.send(reminder_message)
  await channel.send(reminder_message_giff)


#Returns the message to post with image URL (last line) removed
def remove_image_url(msg):
    return msg[:msg.rfind('\n')]

#Returns last line to see if there is an image to post or not
def get_last_line(msg):
    last_line = "\n".join(msg.splitlines()[-1:])
    if ((last_line[0:4])=="http"):
        return True
    else :
        return False
#Returns the URL of the image to post
def get_url(msg):
    return "\n".join(msg.splitlines()[-1:])

# Custom help command
@bot.command()
async def help(context):
    await context.send("use /post {msg} to post a {msg}} in the #announcement rooom. To add an image in the post, add a URL of the image in the end of the post ")


huddle_reminder.start()
keep_alive()
bot.run(os.getenv('TOKEN'))
