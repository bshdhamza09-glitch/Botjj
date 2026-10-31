# Gmail alias Telegram bot

This bot generates Gmail plus-address aliases, **not new Google accounts**. They all deliver to one existing Gmail inbox and use its existing login. A receiving service may reject or normalize aliases.

## Railway
1. Create a Telegram bot with @BotFather and obtain your numeric Telegram user ID.
2. Upload these files to a private GitHub repository, then create a Railway project from the repository.
3. Add environment variables: `BOT_TOKEN`, `ADMIN_ID`, `BASE_GMAIL` (your existing gmail address), and `DB_PATH=/data/aliases.db`.
4. Add a Railway persistent volume mounted at `/data` (check Railway plan and volume availability).
5. Set the start command to `python main.py` and deploy a worker service.
6. Message your bot `/start`.

Railway hosting may incur charges. No Google password or verification code is required by this bot. This bot does not create 4Party accounts or guarantee account country, acceptance, or permanence.
