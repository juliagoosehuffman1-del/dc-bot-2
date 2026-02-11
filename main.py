import discord
from discord.ext import commands
import os

# ----------------------------
# Setup
# ----------------------------
TOKEN = os.getenv("DISCORD_TOKEN")  # Railway variable

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ----------------------------
# Config
# ----------------------------
BOOSTER_ROLE_NAME = "Booster"
ADMIN_ROLE_NAME = "Admin"

# ----------------------------
# Events
# ----------------------------

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

@bot.event
async def on_member_update(before, after):
    # Handle booster role addition
    if before.premium_since is None and after.premium_since is not None:
        guild = after.guild
        role = discord.utils.get(guild.roles, name=BOOSTER_ROLE_NAME)
        if role:
            try:
                await after.add_roles(role)
                print(f"Added {BOOSTER_ROLE_NAME} to {after.name}")
            except Exception as e:
                print(f"Error adding role: {e}")

    # Handle booster role removal if boost stops (optional)
    if before.premium_since is not None and after.premium_since is None:
        guild = after.guild
        role = discord.utils.get(guild.roles, name=BOOSTER_ROLE_NAME)
        if role:
            try:
                await after.remove_roles(role)
                print(f"Removed {BOOSTER_ROLE_NAME} from {after.name}")
            except Exception as e:
                print(f"Error removing role: {e}")

# ----------------------------
# Commands
# ----------------------------

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def addrole(ctx, member: discord.Member, role_name: str):
    """Admin or Booster command to manually add a role"""
    admin_role = discord.utils.get(ctx.guild.roles, name=ADMIN_ROLE_NAME)
    booster_role = discord.utils.get(ctx.guild.roles, name=BOOSTER_ROLE_NAME)

    if admin_role not in ctx.author.roles and booster_role not in ctx.author.roles:
        await ctx.send("You do not have permission to use this.")
        return

    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        await member.add_roles(role)
        await ctx.send(f"Added {role_name} to {member.display_name}")
    else:
        await ctx.send(f"Role `{role_name}` not found.")

@bot.command()
async def removerole(ctx, member: discord.Member, role_name: str):
    """Admin or Booster command to manually remove a role"""
    admin_role = discord.utils.get(ctx.guild.roles, name=ADMIN_ROLE_NAME)
    booster_role = discord.utils.get(ctx.guild.roles, name=BOOSTER_ROLE_NAME)

    if admin_role not in ctx.author.roles and booster_role not in ctx.author.roles:
        await ctx.send("You do not have permission to use this.")
        return

    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        await member.remove_roles(role)
        await ctx.send(f"Removed {role_name} from {member.display_name}")
    else:
        await ctx.send(f"Role `{role_name}` not found.")

# ----------------------------
# Run Bot
# ----------------------------

bot.run(TOKEN)

