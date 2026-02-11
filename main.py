import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# ----------------------------
# Load bot token
# ----------------------------
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# ----------------------------
# Setup bot
# ----------------------------
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} | PID: {os.getpid()}")

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
    "Toys": 1467124052010205258,
    "Alleyway": 1469168105988296880,
    "Phantom": 1469336418638758050,
    "chosen": 1469362745911545926,
    "Lemons": 1470553205980135572
}

# ----------------------------
# Helper function: check if user can assign roles
# ----------------------------
def has_permission(member):
    return any(role.id in ALLOWED_ROLES for role in member.roles)

# ----------------------------
# Helper function: normalize role names
# ----------------------------
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
    """Assign a team role to a member."""
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
    """Remove a team role from a member."""
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
