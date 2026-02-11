import os
TOKEN = os.getenv("DISCORD_TOKEN")

from discord.ext import commands
from flask import Flask
from threading import Thread

# ================= KEEP-ALIVE SERVER =================
app = Flask("")

@app.route("/")
def home():
    return "Bot is alive!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    Thread(target=run).start()

# ================= INTENTS =================
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ================= NORMALIZATION =================
def normalize_role_name(name: str) -> str:
    # lowercase, strip spaces & punctuation
    return "".join(c for c in name.lower() if c.isalnum())

# ================= ROLE SETTINGS =================
RAW_ROLE_IDS = {
    "Lime's Lemons": 1470553205980135572,
    "Lime's": 1470553205980135572,  # only keep if this is INTENTIONALLY the same role
    "The Muplims": 1469010352258682922,
    "Joojoo's Gooner's": 1464013516943130698,
    "Phantom Goose": 1469336418638758050,
    "Bunnie's Herd": 1464642955058086187,
    "Baddies": 1464888310877917299,
    "Doll's Toys": 1467124052010205258,
    "Alleyway Royalty": 1469168105988296880,
    "Dumdum's Chosen Bimbo's": 1469362745911545926,
}

ROLE_IDS = {normalize_role_name(name): role_id for name, role_id in RAW_ROLE_IDS.items()}

BOOSTER_ROLE_ID = 1463961292392890410
LOG_CHANNEL_ID = 1469398064727986186

# ================= BOT TOKEN =================
TOKEN = "INSERT_YOUR_TOKEN_HERE"


# ================= READY =================
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# ================= LOGGING =================
async def log_role_change(guild, actor, target, role, action):
    channel = guild.get_channel(LOG_CHANNEL_ID)
    if not channel:
        return

    embed = discord.Embed(
        title="Role Change Log",
        color=discord.Color.blurple()
    )
    embed.add_field(name="Action", value=action, inline=True)
    embed.add_field(name="Role", value=role.mention, inline=True)
    embed.add_field(name="Target", value=target.mention, inline=False)
    embed.add_field(name="By", value=actor.mention, inline=False)

    await channel.send(embed=embed)

# ================= COMMANDS =================
@bot.command()
async def roles(ctx):
    role_list = "\n".join(f"• {name}" for name in RAW_ROLE_IDS.keys())
    await ctx.send(
        f"**Available roles:**\n{role_list}\n\n"
        f"Use `!add <role>` or `!remove <role>`\n"
        f"Mods / Boosters may target others with `@user`"
    )

@bot.command()
async def add(ctx, *, role_name: str):
    member = ctx.message.mentions[0] if ctx.message.mentions else None
    target = member or ctx.author

    normalized = normalize_role_name(role_name.replace(f"<@{target.id}>", "").strip())
    role_id = ROLE_IDS.get(normalized)

    if not role_id:
        await ctx.send("❌ That role does not exist.")
        return

    role = ctx.guild.get_role(role_id)
    if not role:
        await ctx.send("❌ I can’t find that role in this server.")
        return

    if role >= ctx.guild.me.top_role:
        await ctx.send("❌ That role is higher than my permissions.")
        return

    if target != ctx.author:
        is_mod = ctx.author.guild_permissions.manage_roles
        is_booster = discord.utils.get(ctx.author.roles, id=BOOSTER_ROLE_ID)
        if not (is_mod or is_booster):
            await ctx.send("❌ You can only assign roles to yourself.")
            return

    await target.add_roles(role)
    await ctx.send(f"✅ Added **{role.name}** to **{target.display_name}**")
    await log_role_change(ctx.guild, ctx.author, target, role, "ADD")

@bot.command()
async def remove(ctx, *, role_name: str):
    member = ctx.message.mentions[0] if ctx.message.mentions else None
    target = member or ctx.author

    normalized = normalize_role_name(role_name.replace(f"<@{target.id}>", "").strip())
    role_id = ROLE_IDS.get(normalized)

    if not role_id:
        await ctx.send("❌ That role does not exist.")
        return

    role = ctx.guild.get_role(role_id)
    if not role:
        await ctx.send("❌ I can’t find that role in this server.")
        return

    if role >= ctx.guild.me.top_role:
        await ctx.send("❌ That role is higher than my permissions.")
        return

    if target != ctx.author:
        is_mod = ctx.author.guild_permissions.manage_roles
        is_booster = discord.utils.get(ctx.author.roles, id=BOOSTER_ROLE_ID)
        if not (is_mod or is_booster):
            await ctx.send("❌ You can only remove roles from yourself.")
            return

    await target.remove_roles(role)
    await ctx.send(f"✅ Removed **{role.name}** from **{target.display_name}**")
    await log_role_change(ctx.guild, ctx.author, target, role, "REMOVE")

# ================= START =================
keep_alive()
TOKEN = "INSERT_YOUR_TOKEN_HERE"


