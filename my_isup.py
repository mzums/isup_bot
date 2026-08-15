import os
from dotenv import load_dotenv
import aiohttp
import discord


load_dotenv(override=True)


bot_token = os.environ["ISUP_TOKEN"]
user_id = int(os.environ["DISCORD_USER_ID"])
channel_id = int(os.environ["ISUP_CHANNEL_ID"])


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"BOT ONLINE: {client.user}")
    print(f"Guilds: {len(client.guilds)}")


@client.event
async def on_disconnect():
    print("BOT DISCONNECTED")


@client.event
async def on_resumed():
    print("BOT RESUMED")


urls = [
    "https://mzums.com",
    "https://mzums.com/pl/gen",
    "https://mzums.com/fakewiki",
]

async def check_url(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            if 200 <= response.status < 400:
                print(f"✅ {url}")
                return f"✅ {url} — HTTP {response.status}\n", True
            else:
                print(f"❌ {url} — HTTP {response.status}")
                return f"❌ {url} — HTTP {response.status}\n", False

    except Exception as e:
        print(f"❌ {url} failed: {e}")
        return f"❌ {url} — failed: {e}\n", False


async def check():
    response = ""
    all_ok = True

    async with aiohttp.ClientSession() as session:
        for url in urls:
            result, ok = await check_url(session, url)
            response += result

            if not ok:
                all_ok = False

    if not all_ok:
        user = await client.fetch_user(user_id)
        await user.send(response)

    return response


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("check"):
        result = await check()
        await message.channel.send(result)


client.run(bot_token)

print("Token loaded:", bool(bot_token))
print("Token length:", len(bot_token))
