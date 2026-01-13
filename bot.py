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
ADMIN_ROLE_NAME = "Admin"
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
            description="⚠️ **KHÔNG GIAO DỊCH VỚI NGƯỜI LẠ** ⚠️",
            color=0xFF0000,
            timestamp=datetime.now()
        )

        embed.add_field(
            name="❌ TUYỆT ĐỐI KHÔNG",
            value=(
                "• Giao dịch riêng\n"
                "• Cho mượn đồ\n"
                "• Tin lời hứa miệng\n"
                "• Cho mượn ae Ingame / OTT / tài sản\n"
            ),
            inline=False
        )

        embed.add_field(
            name="🚫 SCAM QUỸ / CHIẾM ĐOẠT QUỸ CREW",
            value=(
                "**➡️ BAN ACC VĨNH VIỄN – KHÔNG XÉT LÝ DO**\n"
                "**➡️ MUA GÌ TỰ CỐNG TIỀN VÀO MUA ĐÚNG SỐ TIỀN CỦA MÌNH**\n"
                "**➡️ TIỀN TRONG QUỸ (QUỸ CĐ) TUYỆT ĐỐI KHÔNG ĐƯỢC HEAL ( chỉ heal đúng số tiền mình cống hiến vào**"
            ),
            inline=False
        )

        embed.add_field(
            name="✅ LUÔN GHI NHỚ",
            value=(
                "• Giao dịch qua Ban Quản Trị / Quản lý Crew\n"
                "• Chụp lại đầy đủ bằng chứng\n"
                "• Báo ngay khi có dấu hiệu nghi ngờ"
            ),
            inline=False
        )

        embed.set_footer(
            text="Crew Lord of Ciara | Biệt đội tiêu diệt scammer  | Tự ý giao dịch bị scam BQT không chịu trách nhiệm"
        )

        await channel.send(
            content="⚠️ **THÔNG BÁO QUAN TRỌNG**",
            embed=embed
        )

        print("✅ Đã gửi thông báo tự động")

    except Exception as e:
        print(f"❌ Lỗi hourly_notification: {e}")
        traceback.print_exc()

@hourly_notification.before_loop
async def before_hourly():
    await bot.wait_until_ready()
    print("🔔 Task thông báo mỗi 1 tiếng đã sẵn sàng")

# ==================== SLASH COMMANDS ====================
@bot.tree.command(
    name="thongbao",
    description="Gửi thông báo tự viết (in hoa, chữ to, đẹp, tag everyone)"
)
@app_commands.describe(noidung="Nội dung thông báo")
async def thongbao(interaction: discord.Interaction, noidung: str):
    if not is_admin(interaction.user):
        await interaction.response.send_message(
            "❌ Bạn không có quyền dùng lệnh này",
            ephemeral=True
        )
        return

    # Chuyển toàn bộ nội dung sang IN HOA
    text_upper = noidung.upper()

    embed = discord.Embed(
        title="📢 THÔNG BÁO TỪ BAN QUẢN TRỊ",
        description=f"**{text_upper}**",
        color=0xFFD700,
        timestamp=datetime.now()
    )

    embed.set_footer(
        text="Crew Lord of Ciara | Thông báo chính thức"
    )

    # Gửi thông báo + tag @everyone
    await interaction.channel.send(
        content="@everyone",
        embed=embed,
        allowed_mentions=discord.AllowedMentions(everyone=True)
    )

    await interaction.response.send_message(
        "✅ Đã gửi thông báo thành công",
        ephemeral=True
    )

@bot.tree.command(name="on", description="Bật thông báo tự động")
async def on_notify(interaction: discord.Interaction):
    global notification_enabled
    if not is_admin(interaction.user):
        await interaction.response.send_message("❌ Bạn không có quyền", ephemeral=True)
        return
    notification_enabled = True
    await interaction.response.send_message("✅ Đã bật thông báo", ephemeral=True)

@bot.tree.command(name="off", description="Tắt thông báo tự động")
async def off_notify(interaction: discord.Interaction):
    global notification_enabled
    if not is_admin(interaction.user):
        await interaction.response.send_message("❌ Bạn không có quyền", ephemeral=True)
        return
    notification_enabled = False
    await interaction.response.send_message("⛔ Đã tắt thông báo", ephemeral=True)

@bot.tree.command(name="status", description="Kiểm tra trạng thái")
async def status(interaction: discord.Interaction):
    state = "🟢 BẬT" if notification_enabled else "🔴 TẮT"
    await interaction.response.send_message(f"📊 Trạng thái: {state}", ephemeral=True)

# ==================== START ====================
if __name__ == "__main__":
    bot.run(TOKEN)
