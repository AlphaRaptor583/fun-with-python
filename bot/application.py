import discord
from discord.ext import commands
import aiohttp

# Data set

basic = {
    "categories-and-channels": {
        'information': ['rules'],
        'announcements':['server-announcements'],
        'community':['general', 'bot-commands'],
        'server-administration':['admin-information', 'admin-announcements', 'admin-chat', 'admin-commands'],
        
        },
    "roles": ['owner', 'server-administrator', 'bot','member']
}
medium_roblox_server = {
    "categories-and-channels": {
        'information': ['rules', 'faq', 'information'],
        'announcements':['server-announcements', 'dev-updates','polls'],
        'engagement':['giveaways','game-nights'],
        'community':['general', 'bot-commands', 'media','memes', 'q&a', 'bug-reports', 'suggestions'],
        'voice-channels':['general-voice', 'game-voice'],
        'game-developers':['developer-information','developer-announcements', 'developer-chat', 'developer-commands', 'developer-suggestions'],
        'administration':['admin-information', 'admin-announcements', 'admin-chat', 'admin-commands'],
        
        },
    "roles": ['owner', 'server-administrator', 'game-developer', 'bot', 'supporter', 'noted-member', 'member']                 
}

# Set up the bot
intents = discord.Intents.default()
intents.message_content = True  # Enable privileged intent for message content
bot = commands.Bot(command_prefix="!", intents=intents)

async def send_embed(channel, title, description, color):
    try:
        embed = discord.Embed(
            title=title,
            description=description,
            color=color
        )
        await channel.send(embed=embed)
    except Exception as e:
        print(f"Failed to send embed message: {e}")
async def send_message(channel, message):
    try:
        embed = discord.Embed(
            title="Bot Status",
            description=message,
            color=discord.Color.green()
        )
        await channel.send(embed=embed)
    except Exception as e:
        print(f"Failed to send message: {e}")

async def send_error_message(channel, message):
    try:
        embed = discord.Embed(
                        title="Bot Error",
                        description=f"An error has occurred:\n {message}",
                        color=discord.Color.red()
                    )
        await channel.send(embed=embed)
    except Exception as e:
        print(f"Failed to send error message: {e}")

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands.")
        # Send a message to the first channel in the guild
        guild = discord.utils.get(bot.guilds)
        print("Current guilds:")
        for guild in bot.guilds:
            print(f"- {guild.name} (ID: {guild.id})")
         
    except Exception as e:
        print(f"Error syncing commands: {e}")

# Event: Bot is added to a server
@bot.event
async def on_guild_join(guild):
    print(f"Bot added to server: {guild.name}")
    try:
        # Send a message to the first channel in the guild
        for i in guild.text_channels:
            if i.permissions_for(guild.me).send_messages:
                embed = discord.Embed(
                    title="Roblox Setup",
                    description="Thank you for adding me!\nRun '/commands' to see available commands.",
                    color=discord.Color.blue()
                )
                await i.send(embed=embed)
                break
    except Exception as e:
        print(f"Error sending message on guild join: {e}")
# Event: Bot is removed from a server
@bot.event
async def on_guild_remove(guild):
    print(f"Bot removed from server: {guild.name}")
    try:
        # Send a message to the first channel in the guild
        for i in guild.text_channels:
            if i.permissions_for(guild.me).send_messages:
                embed = discord.Embed(
                    title="Roblox Setup",
                    description="Thank you for using!",
                    color=discord.Color.blue()
                )
                await i.send(embed=embed)
                break
    except Exception as e:
        print(f"Error sending message on guild remove: {e}")
# Slash command: commands
@bot.tree.command(name="commands", description="Describe available commands")
async def tutorial(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Commands",
        description="""
        # Set up a Discord server according to several templates in a matter of minutes.\n
        ##  Available commands:\n
        1. **'/commands'** : List all available commands.\n
        2. **'/delete_everything'** : Delete all channels, messages, roles and categories.\n
        3. **'/roblox_small'** : Setup channels and roles. Ideal for a small community with upto 200 members.\n
        4. **'/roblox_medium'** : Setup channels and roles. Ideal for a medium sized community with upto 1000 members.\n
        5. **'/roblox_large'** : Setup channels and roles. Ideal for a large community with upto 10000 members.\n
        6. **'/ptfs_airline'** : Setup channels and roles. Ideal for a PTFS airline community.\n
        7. **'/roblox_aviation'** : Setup channels and roles. Ideal for a Roblox aviation roleplay community.\n
        8. **'/roblox_staff'** : Setup channels and roles. Ideal staff server for a Roblox group.\n
        9. **'/roblox-roleplay'** : Setup channels and roles. Synchronises roles with a Roblox group. Ideal for a roleplay experience community.\n
        10. **'/basic'** : Setup channels and roles. Basic server with channels and roles.\n
        11. **'/bot-invite'** : Generate a bot invite link.\n
        """,

        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed, ephemeral=False)
    # Removed unused import

# Slash command: delete everything
@bot.tree.command(name="delete_everything", description="Delete all channels, messages, roles, and categories.")
async def delete_everything(interaction: discord.Interaction):
    guild = interaction.guild
    if not guild:
        await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
        return

    # Create a confirmation button
    class ConfirmDelete(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=30)  # Timeout after 30 seconds
            self.value = None

        @discord.ui.button(label="Confirm", style=discord.ButtonStyle.danger)
        async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.value = True
            self.stop()

        @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
        async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.value = False
            self.stop()

    view = ConfirmDelete()
    await interaction.response.send_message(
        "Are you sure you want to delete all channels, roles, and categories? This action is irreversible.",
        view=view,
        ephemeral=True
    )

    # Wait for user interaction
    await view.wait()

    if view.value is None:
        await interaction.followup.send("Confirmation timed out. Command canceled.", ephemeral=True)
        return
    elif not view.value:
        await interaction.followup.send("Command canceled.", ephemeral=True)
        return

    deleted_channels = 0
    deleted_roles = 0
    deleted_categories = 0

    try:
        # Create a temporary role above all roles
        temp_role = await guild.create_role(name="TempRoleForBot", permissions=discord.Permissions(administrator=True))
        bot_member = guild.get_member(bot.user.id)
        if bot_member:
            await bot_member.add_roles(temp_role)

        # Delete all channels
        for channel in guild.channels:
            await channel.delete()
            if isinstance(channel, discord.TextChannel) or isinstance(channel, discord.VoiceChannel):
                deleted_channels += 1
            elif isinstance(channel, discord.CategoryChannel):
                deleted_categories += 1

        # Delete all roles (except @everyone and the temporary role)
        for role in guild.roles:
            if role != guild.default_role and role != temp_role:  # Skip @everyone and temporary role
                try:
                    await role.delete()
                    deleted_roles += 1
                except discord.Forbidden:
                    print(f"Insufficient permissions to delete role '{role.name}'.")
                except Exception as e:
                    print(f"Failed to delete role '{role.name}': {e}")

        # Remove and delete the temporary role
        if bot_member:
            await bot_member.remove_roles(temp_role)
        await temp_role.delete()

        # Create new category and channel
        admin_category = await guild.create_category("administration")
        admin_channel = await admin_category.create_text_channel("admin-commands")

        # Send embed with summary
        embed = discord.Embed(
            title="Server Reset Complete",
            description=f"""
            All channels, roles, and categories have been deleted.\n
            **Summary:**
            - Deleted Channels: {deleted_channels}
            - Deleted Categories: {deleted_categories}
            - Deleted Roles: {deleted_roles}
            """,
            color=discord.Color.green()
        )
        await admin_channel.send(embed=embed)

        await interaction.followup.send("Server reset complete. Summary sent to 'admin-commands'.", ephemeral=False)

    except Exception as e:
        await send_error_message(interaction.channel, f"An error occurred: {e}")


# Slash command: Bot invite generator
@bot.tree.command(name="bot-invite", description="Generate a bot invite link.")
async def bot_invite(interaction: discord.Interaction):
    bot_user = bot.user
    if bot_user:
        invite_link = discord.utils.oauth_url(bot_user.id, permissions=discord.Permissions.all())
        embed = discord.Embed(
            title="Bot Invite Link",
            description=f"[Click here to invite the bot]({invite_link})",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed, ephemeral=False)
    else:
        await interaction.response.send_message("Bot user not found.", ephemeral=False)

# Slash command: basic
@bot.tree.command(name="basic", description="Setup a basic server.")
async def setup_basic(interaction: discord.Interaction):
    guild = interaction.guild
    if not guild:
        await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
    await interaction.response.defer()  # Acknowledge the interaction before proceeding

    try:
        # Create categories and channels
        for category, channels in basic["categories-and-channels"].items():
            cat = await guild.create_category(category)
            for channel in channels:
                await cat.create_text_channel(channel)

        # Create roles
        for role in basic["roles"]:
            await guild.create_role(name=role)
        
        # Setup role colours
        role_colors = {
            "owner": discord.Color.red(),
            "server-administrator": discord.Color.blue(),
            "bot": discord.Color.green(),
            "member": discord.Color.default()
        }
        for role in basic["roles"]:
            role_obj = discord.utils.get(guild.roles, name=role)
            if role_obj and role in role_colors:
                await role_obj.edit(color=role_colors[role])
        
        # Setup permissions for owner role
        owner_role = discord.utils.get(guild.roles, name="owner")
        if owner_role:
            for channel in guild.channels:
                await channel.set_permissions(owner_role, read_messages=True, send_messages=True, manage_channels=True)
                # Give administrator permission to owner role
                await owner_role.edit(permissions=discord.Permissions(administrator=True))
        # Setup permissions for server-administrator role
        admin_role = discord.utils.get(guild.roles, name="server-administrator")
        if admin_role:
            for channel in guild.channels:
                await channel.set_permissions(admin_role, read_messages=True, send_messages=True, manage_channels=True)
                # Give administrator permission to server-administrator role
                await admin_role.edit(permissions=discord.Permissions(administrator=True))

        # Setup permissions for bot role
        bot_role = discord.utils.get(guild.roles, name="bot")
        if bot_role:
            for channel in guild.channels:
                await channel.set_permissions(bot_role, read_messages=True, send_messages=True, manage_channels=True)
                # Give administrator permission to bot role
                await bot_role.edit(permissions=discord.Permissions(administrator=True))

        # Setup permissions for member role
        member_role = discord.utils.get(guild.roles, name="member")
        if member_role:
            for channel in guild.channels:
                # Prevent members from accessing admin channels
                if channel.name in ["admin-information", "admin-announcements", "admin-chat", "admin-commands"]:
                    await channel.set_permissions(member_role, read_messages=False, send_messages=False)
                elif channel.name in ["rules", "server-announcements"]:
                    await channel.set_permissions(member_role, read_messages=True, send_messages=False)
                elif channel.name in ["general", "bot-commands"]:
                    await channel.set_permissions(member_role, read_messages=True, send_messages=True)
                else:
                    await channel.set_permissions(member_role, read_messages=False, send_messages=False)
        # Setup permissions for everyone role
        everyone_role = guild.default_role
        for channel in guild.channels:
            await channel.set_permissions(everyone_role, read_messages=False, send_messages=False)

        # Assign roles to owner
        owner = guild.owner
        if owner:
            await owner.add_roles(owner_role)
        # Assign member role to all members
        for member in guild.members:
            if member != guild.owner and not member.bot:
                await member.add_roles(member_role)
        # Assign bot role to the bot
        bot_member = guild.get_member(bot.user.id)
        if bot_member:
            await bot_member.add_roles(bot_role)

        # Send an embed with rules
        rules_channel = discord.utils.get(guild.text_channels, name="rules")
        if rules_channel:
            embed = discord.Embed(
                title="Server Rules",
                description="""_ _ 
** **
**1️⃣ HARASSMENT** Warning, Mute, Ban \n Everyone has the right to feel safe and welcomed within this community. Harassment of any form based on race, sex, religion, sexual preference, or sexual orientation of any kind is not permitted.\n\n**2️⃣ USE CHANNELS FOR INTENDED PURPOSE** Warning  \nA majority of the channels within the server have channel topics to abide by. Use the correct channels for the correct discussions, reports, or events.\n\n**3️⃣ ADVERTISING** Ban\nDon't advertise irrelevant media, servers or roblox groups/servers. This includes direct messaging users from the server.\n\n**4️⃣ SPAMMING AND/OR RAIDING** Mute, Ban  \nSpamming large chunks of text, media, and expressions in our channels is prohibited.\n\n**5️⃣ HATE SPEECH/TOXICITY** Mute, Kick, Ban \nAerborne Airport does not tolerate opinions and views that could cause harm and degrade another person within the server. Ignorance and/or immaturity is not an excuse to this rule.\n\n**6️⃣ UNNECESSARY ARGUMENTS** Mute  \nMove any arguments to direct messages and keep them out of the server. If you have any issues with something happening in the server, you're encouraged to ping an administrator.\n\n**7️⃣ DISCUSSION OF SERIOUS/UNWELCOMED TOPICS** Warning, Mute  \nDiscussions of depression, political views, self-harm/suicide, not safe for work material, sensitive real world events, etc are prohibited. Think before you speak and remain courteous of all members in the community.\n\n**8️⃣ THREATS AND/OR INTIMIDATION** Kick, Ban  \nThreatening, intimidating, or leaking personal information about a user is prohibited regardless of how you know the user.\n\n**9️⃣ NSFW OR MALICIUS CONTENT** Unappealable Ban\nDo not post NSFW or harmful content. This includes malware, viruses, or phishing attempts.\n\n**🔟 DISCUSSION OF PUNISHMENTS** Mute\nOpenly discussing your punishments (discord or game-based) is prohibited, you are able to open a support ticket and discuss there with our staff members.
_ _""",
                color=discord.Color.blue()
            )
            await rules_channel.send(embed=embed)
        

        # Send confirmation message
        embed = discord.Embed(
            title="Server Setup Complete",
            description="Basic server setup is complete.",
            color=discord.Color.green()
        )
        await interaction.followup.send(embed=embed, ephemeral=False)

    except Exception as e:
        await send_error_message(interaction.channel, f"An error occurred: {e}")

# Slash command: roblox_roleplay
@bot.tree.command(name="roblox_roleplay", description="Setup a Roblox roleplay server with group rank synchronization.")
async def roblox_roleplay(interaction: discord.Interaction, group_id: int):
    guild = interaction.guild
    if not guild:
        await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
        return

    await interaction.response.defer()  # Acknowledge the interaction before proceeding

    try:
        # Fetch group ranks from Roblox API
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://groups.roblox.com/v1/groups/{group_id}/roles") as response:
                if response.status != 200:
                    await interaction.followup.send("Failed to fetch group ranks. Please check the group ID.", ephemeral=True)
                    return
                data = await response.json()

        group_roles = [role["name"] for role in data.get("roles", [])]

        # Display fetched group ranks and ask for confirmation
        embed = discord.Embed(
            title="Fetched Group Ranks",
            description="\n".join(group_roles),
            color=discord.Color.blue()
        )
        embed.set_footer(text="Do you want to proceed with the server setup?")
        
        # Create a confirmation button
        class ConfirmSetup(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=30)  # Timeout after 30 seconds
                self.value = None

            @discord.ui.button(label="Confirm", style=discord.ButtonStyle.success)
            async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
                self.value = True
                self.stop()

            @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger)
            async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
                self.value = False
                self.stop()

        view = ConfirmSetup()
        await interaction.followup.send(embed=embed, view=view, ephemeral=True)

        # Wait for user interaction
        await view.wait()

        if view.value is None:
            await interaction.followup.send("Confirmation timed out. Command canceled.", ephemeral=True)
            return
        elif not view.value:
            await interaction.followup.send("Command canceled.", ephemeral=True)
            return

        # Create categories and channels using the roblox_medium template
        for category, channels in medium_roblox_server["categories-and-channels"].items():
            cat = await guild.create_category(category)
            for channel in channels:
                await cat.create_text_channel(channel)

        # Create roles based on fetched group ranks
        for role in group_roles:
            await guild.create_role(name=role)

        # Setup permissions for roles
        for role_name in group_roles:
            role_obj = discord.utils.get(guild.roles, name=role_name)
            if role_obj:
                for channel in guild.channels:
                    if "admin" in channel.name.lower():
                        await channel.set_permissions(role_obj, read_messages=False, send_messages=False)
                    else:
                        await channel.set_permissions(role_obj, read_messages=True, send_messages=True)

        # Setup permissions for everyone role
        everyone_role = guild.default_role
        for channel in guild.channels:
            await channel.set_permissions(everyone_role, read_messages=False, send_messages=False)

        # Send confirmation message
        embed = discord.Embed(
            title="Server Setup Complete",
            description=f"Roblox roleplay server setup is complete for group ID {group_id}.",
            color=discord.Color.green()
        )
        await interaction.followup.send(embed=embed, ephemeral=False)

    except Exception as e:
        await send_error_message(interaction.channel, f"An error occurred: {e}")



if __name__ == "__main__":
    TOKEN = "MTM1MjQ3Njk2NDAyMzE3NzMyNg.GbHy5R.lWXmkGntwE2DC8tPQZsSaNokYKSEiXIachRBlU"  
    
    bot.run(TOKEN)
    
    