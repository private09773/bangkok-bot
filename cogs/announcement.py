import discord
from discord.ext import commands

class Announcement(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot
        
    # Announcement (Prefix)
    @commands.command(name="announce")
    @commands.has_permissions(manage_messages=True)
    async def announce(self, ctx: commands.Context, channel: discord.TextChannel, *, message: str):
        # Will Send your message to the channel.
        await channel.send(
        f"**Announcement from Bangkok Airways Staff!**\n\n"
        f"{message}\n\n"
        f"-# Posted by {ctx.author.mention}.\n"
        )
        
        # Will confirm if it has been sent.
        await ctx.send("Sent to {ctx.channel.name}.")
        
async def setup(bot):
    await bot.add_cog(Announcement(bot))
