import os
import discord
from discord.ext import commands, tasks
import queue_manager

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

queue_mgr = queue_manager.QueueManager()


@bot.event
async def on_ready():
    heartbeat_mq.start()
    print(f"Bot connected as {bot.user}")


@bot.command()
async def draw(ctx, *, prompt):

    await ctx.send(f"queueing {prompt}")

    req = {
        "user": ctx.author.id,
        "channel": ctx.channel.id,
        "prompt": prompt,
    }

    queue_mgr.enqueue_prompt(req)


@tasks.loop(seconds=3)
async def heartbeat_mq():
    queue_mgr.connection.process_data_events(time_limit=0)

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
