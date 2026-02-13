import discord
from discord.ext import commands
import os
import sys

# ---------------------------- 
# Startup token check
# ----------------------------
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    print("❌ ERROR: DISCORD_TOKEN is not set.")
    sys.exit(1)

if TOKEN.lower().startswith("your") or " " in TOKEN:
    print("❌ ERROR: DISCORD_TOKEN looks invalid.")
    sys.exit(1)

# ---------------------------- 
# Setup bot
# ----------------------------
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ---------------------------- 
# Bot ready event
# ----------------------------
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} | PID: {os.getpid()}")

# ---------------------------- 
# Server role IDs (who can assign roles)
# ----------------------------
ADMIN_ROLE_ID = 1464280949003915395
MOD_ROLE_ID = 1463625148098936892
BOOSTER_ROLE_ID = 1463961292392890410

ALLOWED_ROLES = [ADMIN_ROLE_ID, MOD_ROLE_ID, BOOSTER_ROLE_ID]

# ---------------------------- 
# Assignable Team Roles
# ----------------------------
TEAM_ROLES = {
    "Gooners": 1464013516943130698,
    "Muplims": 1469010352258682922,
    "Herd": 1464642955058086187,
    "Baddies": 1464888310877917299,
    "Waiters": 1471208583965442287,
    "Toys": 1467124052010205258,
    "Alleyway": 1469168105988296880,
    "Cuties": 1471247421509075166,
    "chosen": 1469362745911545926,
    "Lemons": 1470553205980135572
}

# ---------------------------- 
# Helper functions
# ----------------------------
def has_permission(member):
    return any(role.id in ALLOWED_ROLES for role in member.roles)

def normalize_role_name(name):
    return name.replace("'", "").strip().lower()

def find_role_id(name):
    norm_name = normalize_role_name(name)
    for role_name, role_id in TEAM_ROLES.items():
        if normalize_role_name(role_name) == norm_name:
            return role_id
    return None

# ---------------------------- 
# Commands
# ----------------------------
@bot.command(name="assign", aliases=["add"])
async def assign_role(ctx, member: discord.Member, *, role_name: str):
    if not has_permission(ctx.author):
        await ctx.send("❌ You do not have permission to assign roles.")
        return

    role_id = find_role_id(role_name)
    if not role_id:
        await ctx.send(f"❌ Role `{role_name}` is not an assignable team role.")
        return

    role = ctx.guild.get_role(role_id)
    if role in member.roles:
        await ctx.send(f"⚠ {member.mention} already has the `{role_name}` role.")
        return

    await member.add_roles(role)
    await ctx.send(f"✅ {ctx.author.mention} assigned `{role_name}` to {member.mention}.")

@bot.command(name="remove", aliases=["rm"])
async def remove_role(ctx, member: discord.Member, *, role_name: str):
    if not has_permission(ctx.author):
        await ctx.send("❌ You do not have permission to remove roles.")
        return

    role_id = find_role_id(role_name)
    if not role_id:
        await ctx.send(f"❌ Role `{role_name}` is not an assignable team role.")
        return

    role = ctx.guild.get_role(role_id)
    if role not in member.roles:
        await ctx.send(f"⚠ {member.mention} does not have the `{role_name}` role.")
        return

    await member.remove_roles(role)
    await ctx.send(f"✅ {ctx.author.mention} removed `{role_name}` from {member.mention}.")

# ---------------------------- 
# Help command
# ----------------------------
@bot.command(name="mybothelp")
async def mybot_help(ctx):
    msg = "**Assignable Team Roles:**\n"
    for role_name in TEAM_ROLES:
        msg += f"- `{role_name}`\n"
    msg += "\n**Commands:**\n"
    msg += "- `!assign @member <TeamRole>` or `!add @member <TeamRole>` — Assign a team role\n"
    msg += "- `!remove @member <TeamRole>` or `!rm @member <TeamRole>` — Remove a team role"
    await ctx.send(msg)

# ---------------------------- 
# Run bot
# ----------------------------
bot.run(TOKEN)
