import os, discord, aiohttp
from discord.ext import commands

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID", "0"))
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_FEED_URL")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"STAGE Bot online as {bot.user} — Guild {GUILD_ID}")

@bot.event
async def on_member_join(member):
    # Auto role: Waitlist
    role = discord.utils.get(member.guild.roles, name="Waitlist")
    if role:
        await member.add_roles(role)
    # Post to founding-feed webhook
    if WEBHOOK_URL:
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(WEBHOOK_URL, session=session)
            await webhook.send(f"👋 **{member.name}** joined STAGE — Founding #{member.guild.member_count} — Welcome!")

@bot.command()
async def verify(ctx):
    # Moves Waitlist -> Verified
    waitlist = discord.utils.get(ctx.guild.roles, name="Waitlist")
    verified = discord.utils.get(ctx.guild.roles, name="Verified")
    if waitlist in ctx.author.roles:
        await ctx.author.remove_roles(waitlist)
        await ctx.author.add_roles(verified)
        await ctx.send(f"✅ {ctx.author.mention} verified — welcome to STAGE!")

bot.run(TOKEN)
