import discord
from discord.ext import commands
import json
import os
import asyncio

DB_FILE = "player_flights.json"

# Helper functions to handle JSON loading and saving
def load_flights():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({}, f)
        return {}
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_flights(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

class FlightSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Option 1: Quick 1-line prefix command
    # Usage: .flight-plan BKP102 | VTBS | VTSP | A320 | FL320
    @commands.command(name="flight-plan")
    async def flight_plan(self, ctx: commands.Context, *, args: str = None):
        user_id = str(ctx.author.id)

        # If no arguments are provided, start interactive Q&A mode
        if not args:
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                await ctx.send("✈️ **Enter Callsign** (e.g. `BKP102`):")
                callsign = (await self.bot.wait_for("message", check=check, timeout=30.0)).content

                await ctx.send("🛫 **Enter Departure Airport** (e.g. `VTBS`):")
                departure = (await self.bot.wait_for("message", check=check, timeout=30.0)).content

                await ctx.send("🛬 **Enter Arrival Airport** (e.g. `VTSP`):")
                arrival = (await self.bot.wait_for("message", check=check, timeout=30.0)).content

                await ctx.send("🛩️ **Enter Aircraft Type** (e.g. `A320`):")
                aircraft = (await self.bot.wait_for("message", check=check, timeout=30.0)).content

                await ctx.send("📊 **Enter Cruising Altitude** (e.g. `FL320`):")
                altitude = (await self.bot.wait_for("message", check=check, timeout=30.0)).content

            except asyncio.TimeoutError:
                await ctx.send("❌ Flight plan creation timed out. Please try again.")
                return
        else:
            # Parse one-line input split by '|'
            parts = [p.strip() for p in args.split("|")]
            if len(parts) < 5:
                await ctx.send("❌ **Invalid format!**\nUse: `.flight-plan Callsign | Departure | Arrival | Aircraft | Altitude`\nOr type `.flight-plan` alone for guided setup.")
                return
            callsign, departure, arrival, aircraft, altitude = parts[:5]

        flight_info = {
            "callsign": callsign.upper(),
            "departure": departure.upper(),
            "arrival": arrival.upper(),
            "aircraft": aircraft.upper(),
            "altitude": altitude.upper(),
            "passengers": []
        }

        flights = load_flights()
        if user_id not in flights:
            flights[user_id] = []

        flights[user_id].append(flight_info)
        save_flights(flights)

        await ctx.send(
            f"✅ **Flight Plan Filed Successfully!**\n"
            f"• **Callsign:** `{flight_info['callsign']}`\n"
            f"• **Route:** `{flight_info['departure']}` ➔ `{flight_info['arrival']}`\n"
            f"• **Aircraft:** `{flight_info['aircraft']}`\n"
            f"• **Altitude:** `{flight_info['altitude']}`"
        )

    # View flight plans: .myflights or .myflights @User
    @commands.command(name="myflights")
    async def myflights(self, ctx: commands.Context, member: discord.Member = None):
        target = member or ctx.author
        user_id = str(target.id)
        flights = load_flights()

        user_flights = flights.get(user_id, [])

        if not user_flights:
            await ctx.send(f"❌ {target.mention} has no active flight plans filed.")
            return

        msg = f"✈️ **Flight Plans for {target.name}:**\n\n"
        for idx, f in enumerate(user_flights, 1):
            pax_count = len(f.get("passengers", []))
            msg += (
                f"**[{idx}] Callsign:** `{f['callsign']}`\n"
                f"• Route: `{f['departure']}` ➔ `{f['arrival']}`\n"
                f"• Aircraft: `{f['aircraft']}` | Alt: `{f['altitude']}`\n"
                f"• Passengers: {pax_count}\n\n"
            )

        await ctx.send(msg)

    # Cancel flight plan: .cancel BKP102 or .cancel 1
    @commands.command(name="cancel")
    async def cancel_flight(self, ctx: commands.Context, callsign_or_num: str):
        user_id = str(ctx.author.id)
        flights = load_flights()

        user_flights = flights.get(user_id, [])

        if not user_flights:
            await ctx.send("❌ You have no active flight plans to cancel.")
            return

        removed = None

        if callsign_or_num.isdigit():
            idx = int(callsign_or_num) - 1
            if 0 <= idx < len(user_flights):
                removed = user_flights.pop(idx)
        else:
            for f in user_flights:
                if f["callsign"] == callsign_or_num.upper():
                    removed = f
                    user_flights.remove(f)
                    break

        if removed:
            flights[user_id] = user_flights
            save_flights(flights)
            await ctx.send(f"🗑️ Flight plan **`{removed['callsign']}`** (`{removed['departure']}` ➔ `{removed['arrival']}`) has been canceled.")
        else:
            await ctx.send(f"❌ Could not find a flight plan matching `{callsign_or_num}`.")

    # Board passenger: .board @Pilot @Passenger
    @commands.command(name="board")
    async def board_passenger(self, ctx: commands.Context, pilot: discord.Member, passenger: discord.Member):
        pilot_id = str(pilot.id)
        flights = load_flights()

        pilot_flights = flights.get(pilot_id, [])

        if not pilot_flights:
            await ctx.send(f"❌ {pilot.mention} has no active flight plans.")
            return

        latest_flight = pilot_flights[-1]
        pax_list = latest_flight.get("passengers", [])

        if passenger.id in pax_list:
            await ctx.send(f"⚠️ {passenger.mention} is already on flight `{latest_flight['callsign']}`.")
            return

        pax_list.append(passenger.id)
        latest_flight["passengers"] = pax_list
        save_flights(flights)

        await ctx.send(f"🎟️ {passenger.mention} boarded **`{latest_flight['callsign']}`** (`{latest_flight['departure']}` ➔ `{latest_flight['arrival']}`).")

    # View passengers: .passengers or .passengers @Pilot
    @commands.command(name="passengers")
    async def passengers(self, ctx: commands.Context, pilot: discord.Member = None):
        target = pilot or ctx.author
        pilot_id = str(target.id)
        flights = load_flights()

        pilot_flights = flights.get(pilot_id, [])

        if not pilot_flights:
            await ctx.send(f"❌ {target.mention} has no active flight plans.")
            return

        latest_flight = pilot_flights[-1]
        pax_ids = latest_flight.get("passengers", [])

        if not pax_ids:
            await ctx.send(f"✈️ Flight **`{latest_flight['callsign']}`** currently has no passengers onboard.")
            return

        pax_mentions = [f"<@{p_id}>" for p_id in pax_ids]
        await ctx.send(
            f"📋 **Passenger Manifest for `{latest_flight['callsign']}`:**\n" +
            "\n".join([f"• {m}" for m in pax_mentions])
        )

async def setup(bot):
    await bot.add_cog(FlightSystem(bot))
