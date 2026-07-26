# How to Install The Bot

1. Clone the Repository
``` bash
# Windows
git clone https://github.com/private09773/bangkok-bot

# Linux
git clone https://github.com/private09773/bangkok-bot
```

2. Check Directory for .env.example
``` bash
# Windows
cd C:\Users\YourName\bangkok-bot\.env.example

# Linux
cd /storage/emulated/0/bangkok-bot/.env.example
```

3. Rename .env.example to .env
``` bash
# Windows
mv .env.example .env

# Linux
mv .env.example .env
```

4. Set your values
``` env
# DISCORD TOKEN (DO NOT SHARE YOUR TOKEN).
DISCORD_TOKEN="your_bot_token_here"

# GUILD ID
GUILD_ID="your_guild_id_here"

# OWNER ID
OWNER_ID="owner_1_id"
```

5. Run the requirements.txt file
``` bash
# Windows
pip install -r requirements.txt

# Linux
pip3 install -r requirements.txt
```

6. After it is done installing, run this and the bot will go online
``` bash
# Windows
python main.py

# Linux
python3 main.py
```