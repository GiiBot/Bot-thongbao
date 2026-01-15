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

    from datetime import datetime
    import discord

embed = discord.Embed(
    title="🚨 CẢNH BÁO - LORD OF CIARA - 🚨",
    description="⚠️ **KHÔNG GIAO DỊCH VỚI NGƯỜI LẠ – KHÔNG CÓ NGOẠI LỆ VỚI NGƯỜI TRONG CREW ** ⚠️",
    color=0xFF0000,
    timestamp=datetime.now()
)

# ================= TUYỆT ĐỐI KHÔNG =================
embed.add_field(
    name="❌ TUYỆT ĐỐI KHÔNG",
    value=(
        "• Giao dịch riêng với người ngoài\n"
        "• Cho mượn tiền / đồ / tài sản trong game (ngoài)\n"
        "• Tin lời hứa miệng – không bằng chứng\n"
        "• Cho mượn acc, tiền Ingame / OTT / thời trang\n"
    ),
    inline=False
)

# ================= SCAM QUỸ =================
embed.add_field(
    name="🚫 SCAM QUỸ / CHIẾM ĐOẠT QUỸ CHIẾM ĐÓNG",
    value=(
        "🔥 **BAN ACC VĨNH VIỄN – KHÔNG XÉT LÝ DO**\n"
        "🔥 **KHÔNG HỖ TRỢ – KHÔNG GIẢI TRÌNH**\n"
        "💰 **MUA GÌ → TỰ CỐNG TIỀN CỦA MÌNH → MUA ĐÚNG GIÁ TRỊ TIỀN CỐNG VÀO**\n"
        "🏦 **TIỀN TRONG QUỸ (QUỸ CĐ) TUYỆT ĐỐI KHÔNG ĐƯỢC HEAL**\n"
        "⚠️ **CHỈ ĐƯỢC HEAL ĐÚNG SỐ TIỀN CÁ NHÂN ĐÃ CỐNG HIẾN**"
    ),
    inline=False
)

# ================= LUÔN GHI NHỚ =================
embed.add_field(
    name="✅ LUÔN GHI NHỚ",
    value=(
        "• Mọi giao dịch phải thông qua @Ban Quản Trị Crew\n"
        "• Chụp lại đầy đủ bằng chứng (ảnh, clip,...)\n"
        "• Báo ngay khi có dấu hiệu nghi ngờ\n"
        "• Tự ý giao dịch → tự chịu trách nhiệm"
    ),
    inline=False
)

# ================= ROLE CREW =================
embed.add_field(
    name="🏷️ HỆ THỐNG CHỨC VỤ & XẾP HẠNG – LORD OF CIARA",
    value=(
        "👑 **@Nhà sáng lập & Điều hành**\n"
        "🛡️ **@Ban quản trị** – Quản lý CREW, xử lý vi phạm\n"
        "💰 **@Tài chính** – Quản lý quỹ, thu chi\n"
        "👥 **@Nhân sự** – Tuyển thành viên\n"
        "📌 **@Quản lí** – Điều hành hoạt động crew\n"
        "💎 **@Nhà tài trợ** – Hỗ trợ tài chính / tài nguyên\n"
        "🎁 **@Donate** – Thành viên đóng góp tự nguyện\n"
        "🏦 **@Lũ quỹ Ciara** – Những con quỹ của Ciara\n"
        "🛠️ **@Outfix Ciara** – Sở hữu outfix\n"
        "🔥 **@Thành viên tâm huyết** – Hoạt động tích cực , chơi ở crew lâu năm\n"
        "✅ **@Chính thức** – Thành viên chính thức\n"
        "🧪 **@Thực tập** – Giai đoạn thử việc"
    ),
    inline=False
)

# ================= FOOTER =================
embed.set_footer(
    text="Crew LORD OF CIARA | Nói không với scam | Tự ý giao dịch bị scam – BQT không chịu trách nhiệm"
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
class ThongBaoModal(discord.ui.Modal, title="🔔 GHI THÔNG BÁO CIARA"):
    noidung = discord.ui.TextInput(
        label="NỘI DUNG THÔNG BÁO",
        style=discord.TextStyle.paragraph,
        placeholder="Nhập nội dung thông báo tại đây...",
        required=True,
        max_length=4000
    )

    async def on_submit(self, interaction: discord.Interaction):
        text_upper = self.noidung.value.upper()

        embed = discord.Embed(
            title="📢 THÔNG BÁO TỪ BAN QUẢN TRỊ",
            description=f"**{text_upper}**",
            color=0xFFD700,
            timestamp=datetime.now()
        )

        embed.set_footer(
            text="Crew Lord of Ciara | Thông báo chính thức"
        )

        await interaction.channel.send(
            content="@everyone",
            embed=embed,
            allowed_mentions=discord.AllowedMentions(everyone=True)
        )

        await interaction.response.send_message(
            "✅ Đã gửi thông báo thành công",
            ephemeral=True
        )
@bot.tree.command(
    name="thongbao",
    description="Mở bảng nhập thông báo (form)"
)
async def thongbao(interaction: discord.Interaction):
    if not is_admin(interaction.user):
        await interaction.response.send_message(
            "❌ Bạn không có quyền dùng lệnh này",
            ephemeral=True
        )
        return

    await interaction.response.send_modal(ThongBaoModal())


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
