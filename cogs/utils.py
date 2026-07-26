import discord
from discord import app_commands
from discord.ext import commands

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # Ping Command (Prefix)
    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        await ctx.send("Pong!")
        
    # Server Info (Prefix)
    @commands.command(name="serverinfo")
    async def serverinfo(self, ctx: commands.Context):
        await ctx.send(
        f"**Server Owner**: {ctx.guild.owner}\n"
        f"**Server Name**: {ctx.guild.name}\n"
        f"**Server ID**: `{ctx.guild.id}`\n"
        f"**Server Members**: {ctx.guild.member_count}\n"
        f"**Server Created On**: <t:{int(ctx.guild.created_at.timestamp())}:F>\n"
        )
    
    # User Info (Prefix)
    @commands.command(name="userinfo")
    async def userinfo(self, ctx: commands.Context, member: discord.Member = None):
        target = member or ctx.author

        await ctx.send(
            f"**User Info for:** {target.mention}\n"
            f"**Username:** `{target.name}`\n"
            f"**Display Name:** {target.display_name}\n"
            f"**User ID:** `{target.id}`\n"
            f"**Account Created:** <t:{int(target.created_at.timestamp())}:F>\n"
            f"**Joined Server:** <t:{int(target.joined_at.timestamp())}:F>\n"
            f"**Highest Role:** {target.top_role.mention}"
        )
        
    # Avatar (Prefix)
    @commands.command(name="avatar")
    async def avatar(self, ctx: commands.Context, member: discord.Member = None):
        target = member or ctx.author
        
        await ctx.send(
            f"Take a look at {target.mention}(s) avatar!\n"
            f"Avatar: {target.avatar.url}"
        )

    
   

async def setup(bot):
    await bot.add_cog(Utils(bot))
