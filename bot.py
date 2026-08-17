import os, discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

print(f"Starting bot... TOKEN exists: {bool(TOKEN)} GUILD_ID: {GUILD_ID}")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ LOGGED IN as {bot.user} - ONLINE!")
    try:
        guild = discord.Object(id=int(GUILD_ID)) if GUILD_ID else None
        if guild:
            bot.tree.copy_global_to(guild=guild)
            await bot.tree.sync(guild=guild)
            print(f"Synced commands to guild {GUILD_ID}")
    except Exception as e:
        print(f"Sync error: {e}")

@bot.command()
async def verify(ctx):
    try:
        role = discord.utils.get(ctx.guild.roles, name="Verified")
        if role:
            await ctx.author.add_roles(role)
            await ctx.send(f"✅ {ctx.author.mention} verified — welcome to STAGE!")
        else:
            await ctx.send("Verified role not found — create role named Verified")
    except Exception as e:
        await ctx.send(f"Verify error: {e}")
        print(e)

@bot.event 
async def on_member_join(member):
    print(f"Member joined: {member}")
    # webhook feed
    webhook_url = os.getenv("DISCORD_WEBHOOK_FEED_URL")
    if webhook_url:
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                count = member.guild.member_count
                await session.post(webhook_url, json={"content": f"👋 {member.mention} joined STAGE — Founding #{count} — Welcome!"})
        except Exception as e:
            print(f"Webhook error: {e}")

bot.run(TOKEN)
