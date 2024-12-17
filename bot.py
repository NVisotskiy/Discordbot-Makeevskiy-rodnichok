import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import time

# Завантажуємо токен із файлу .env
load_dotenv("token.env")
TOKEN = os.getenv("DISCORD_TOKEN")

print("🚀 Запускаємо бота...")  # Відладочне повідомлення

# Налаштування бота
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Подія: бот готовий до роботи
@bot.event
async def on_member_join(member):
    print(f"👋 Новий учасник приєднався: {member.name}")  # Відладка
    welcome_message = (
        f"Йо, {member.mention}! 🎉 Шо, заблукав чи чого сюди залетів? "
        f"Зазирни до каналу з правилами, щоб не наламати дров! 😉"
    )
    general_channel = discord.utils.get(member.guild.text_channels, name="new-members")
    if general_channel:
        time.sleep(5) # Sleep for 5 seconds
        await general_channel.send(welcome_message)
        print(f"📨 Відправлено привітальне повідомлення для {member.name}")  # Відладка
    else:
        print("⚠️ Канал 'new-members' не знайдено. Перевірте назву каналу.")  # Відладка


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands globally.")
    except Exception as e:
        print(e)

# Команда: !ping
@bot.command()
async def ping(ctx):
    print(f"🏓 Отримано команду !ping від {ctx.author}")  # Відладка
    await ctx.send("Понг! 🏓 Бот на зв'язку.") 

@bot.tree.command(name="hello", description="Say hello to the bot!")
async def hello(interaction: discord.Interaction):
    """Slash command to respond in all chats."""
    await interaction.response.send_message("Hello! This slash command works in all servers!")

# Перевірка токену та запуск бота
if TOKEN:
    print("🔑 Токен завантажено. Підключаємося до Discord...")
    bot.run(TOKEN)
else:
    print("❌ Токен не знайдено! Перевірте файл .env.")
