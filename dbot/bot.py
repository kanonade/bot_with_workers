import os

import discord
import queue_manager
from discord.ext import commands, tasks

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

queue_mgr = queue_manager.QueueManager()


@bot.event
async def on_ready():
    heartbeat_mq.start()
    return_images.start()
    print(f"Bot connected as {bot.user}")


@bot.command()
async def draw(ctx, *, prompt):

    req = {
        "user": ctx.author.id,
        "channel": ctx.channel.id,
        "prompt": prompt,
    }

    queue_mgr.enqueue_prompt(req)
    await ctx.message.add_reaction("👀")


@tasks.loop(seconds=3)
async def heartbeat_mq():
    queue_mgr.connection.heartbeat_check()


@tasks.loop(seconds=1)
async def return_images():
    msg, body = queue_mgr.dequeue_image()
    if msg is not None and body is not None:
        print(body)

        await bot.get_channel(body["channel"]).send(
            f'<@{str(body["user"])}> {body["image"]}'
        )

        msg.ack()


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
