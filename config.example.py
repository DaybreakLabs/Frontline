class Config:
    disable_ascii = False

    guild_id = 0
    sentry_dsn = "" # Replace this with your Sentry DSN

    server_id = (
        ""  # Type `!id`` in your server console & replace this with your account id
    )
    api_token = ""  # Type `!api reset`` in your server console
    token = "" # Discord Bot Token'
    port = 80

    # === Steam ID module ===
    steam_api_key = ""  # Steam API key
    redirect_uri = ""  # Redirect URI for Steam login
    realm = ""  # Realm for Steam login

    ticket_name = "" # The starting name of the ticket channel (ex: ticket-)