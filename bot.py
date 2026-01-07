# ==================== bot.py ====================
import discord
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime
import asyncio
import os
import traceback

# ==================== CONFIG ====================
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))

# Role được phép dùng lệnh /on /off (ĐỔI TÊN ROLE NẾU MUỐN)
ADMIN_ROLE_NAME = "Admin"

# Chống spam: mỗi user 1 lệnh / 10 giây
COOLDOWN_SECONDS = 10

# ==================== INTENTS ====================
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ==================== GLOBAL STATE ====================
notification_enabled = True
cooldowns = {}

# ==================== ERROR GLOBAL ====================
@bot.event
async def on_error(event, *args, **kwargs):
    print("❌ BOT ERROR:")
    traceback.print_exc()

# ==================== READY ====================
@bot.event
async def on_ready():
    print(f"🟢 Bot ONLINE: {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Đã sync {len(synced)} slash commands")
    except Exception as e:
        print(f"❌ Lỗi sync slash: {e}")

    if not hourly_notification.is_running():
        hourly_notification.start()

# ==================== HELPER ====================
def is_admin(member: discord.Member):
    return any(role.name == ADMIN_ROLE_NAME for role in member.roles)

def check_cooldown(user_id: int):
    now = datetime.now().timestamp()
    last = cooldowns.get(user_id, 0)
    if now - last < COOLDOWN_SECONDS:
        return False, int(COOLDOWN_SECONDS - (now - last))
    cooldowns[user_id] = now
    return True, 0

# ==================== TASK ====================
@tasks.loop(hours=1)
async def hourly_notification():
    global notification_enabled
    if not notification_enabled:
        return

    try:
        channel = await bot.fetch_channel(CHANNEL_ID)
        if not channel:
            return

        embed = discord.Embed(
            title="🚨 CẢNH BÁO SCAM - LORD OF CIARA 🚨",
            description="⚠️ **KHÔNG GIAO DỊCH NGOÀI HỆ THỐNG** ⚠️",
            color=0xFF0000,
            timestamp=datetime.now()
        )

        embed.add_field(
            name="❌ TUYỆT ĐỐI KHÔNG",
            value="• Giao dịch riêng\n• Cho mượn đồ\n• Tin lời hứa miệng",
            inline=False
        )

        embed.add_field(
            name="✅ LUÔN GHI NHỚ",
            value="• Giao dịch qua Admin\n• Chụp bằng chứng\n• Báo ngay khi nghi ngờ",
            inline=False
        )

        embed.set_footer(text="Gangs Lord of Ciara | Anti Scam")

        await channel.send(
            content="⚠️ **@everyone THÔNG BÁO QUAN TRỌNG**",
            embed=embed,
            allowed_mentions=discord.AllowedMentions(everyone=True)
        )

        print("✅ Đã gửi thông báo tự động")

    except Exception as e:
        print(f"❌ Lỗi hourly_notification: {e}")

@hourly_notification.before_loop
async def before_hourly():
    await bot.wait_until_ready()
    print("🔔 Task thông báo mỗi 1 tiếng đã sẵn sàng")

# ==================== SLASH COMMANDS ====================

@bot.tree.command(name="on", description="Bật thông báo tự động")
async def on_notify(interaction: discord.Interaction):
    global notification_enabled

    if not is_admin(interaction.user):
        await interaction.response.send_message(
            "❌ Bạn không có quyền dùng lệnh này",
            ephemeral=True
        )
        return

    ok, wait = check_cooldown(interaction.user.id)
    if not ok:
        await interaction.response.send_message(
            f"⏳ Đợi {wait}s rồi thử lại",
            ephemeral=True
        )
        return

    notification_enabled = True
    await interaction.response.send_message(
        "✅ Đã **BẬT** thông báo tự động",
        ephemeral=True
    )

@bot.tree.command(name="off", description="Tắt thông báo tự động")
async def off_notify(interaction: discord.Interaction):
    global notification_enabled

    if not is_admin(interaction.user):
        await interaction.response.send_message(
            "❌ Bạn không có quyền dùng lệnh này",
            ephemeral=True
        )
        return

    ok, wait = check_cooldown(interaction.user.id)
    if not ok:
        await interaction.response.send_message(
            f"⏳ Đợi {wait}s rồi thử lại",
            ephemeral=True
        )
        return

    notification_enabled = False
    await interaction.response.send_message(
        "⛔ Đã **TẮT** thông báo tự động",
        ephemeral=True
    )

@bot.tree.command(name="status", description="Kiểm tra trạng thái bot")
async def status(interaction: discord.Interaction):
    state = "🟢 ĐANG BẬT" if notification_enabled else "🔴 ĐANG TẮT"
    await interaction.response.send_message(
        f"📊 Trạng thái thông báo: **{state}**",
        ephemeral=True
    )

# ==================== START ====================
if __name__ == "__main__":
    if not TOKEN:
        print("❌ DISCORD_TOKEN chưa thiết lập")
    elif CHANNEL_ID == 0:
        print("❌ CHANNEL_ID chưa thiết lập")
    else:
        try:
            bot.run(TOKEN)
        except Exception as e:
            print(f"❌ Bot crash: {e}")
