<div align="right">

# Frontline 🌙
> 🔧 **Frontline of server management**:
> This project was developed for the Dream server.<br>
> Compatibility is not guaranteed, and we are not responsible for any issues that may arise.
</div>

## 🌟 Features

- ✨ Display server member count without any plugin
## 🪚 Working In Progress
- 🔒 Automatically send Steam ID when creating a ticket with linked steam account.

---

## 📖 Getting Started
### LICENSE
> [!IMPORTANT]  
> This project is licensed under a this license,<br>
> except for specific files (e.g., `utils/steam.py`), which are licensed under the GNU General Public License v2.0 (GPL-2.0).<br><br>
> When using this project outside of the Dream server, you must add a link to this project in the Discord bot's introduction section.<br>
> Additionally, if modifications occur, you must disclose the source code.<br><br>
> Files under GPL-2.0 (e.g., `utils/steam.py`) must comply with the terms of the GNU General Public License v2.0.
### Prerequisites

- 💻 Install  **Python**
- 🔧 Install **pip**

### Installation

```bash
# Clone this repository
git clone https://github.com/DaybreakLabs/Frontline.git

# Navigate to the project directory
cd Frontline

# Rename Config file & change config
mv config.example.py config.py

# Install dependencies
pip install discord.py orjson aiohttp asyncio sentry-sdk

# Run your bot
python main.py
```