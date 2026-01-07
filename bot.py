# ==================== bot.py ====================
import discord
from discord.ext import commands, tasks
from datetime import datetime
import asyncio
import os

# Cấu hình bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Lấy config từ environment variables
TOKEN = os.getenv('DISCORD_TOKEN')
NOTIFICATION_CHANNEL_ID = int(os.getenv('CHANNEL_ID', '0'))

@bot.event
async def on_ready():
    print(f'✅ Bot đã đăng nhập: {bot.user.name}')
    print(f'🆔 Bot ID: {bot.user.id}')
    print(f'📢 Channel ID: {NOTIFICATION_CHANNEL_ID}')
    print(f'🎮 Gangs Lord of Ciara - Anti Scam Bot')
    print('='*50)
    # Bắt đầu task gửi thông báo mỗi 1 tiếng
    hourly_notification.start()

# Task gửi thông báo định kỳ mỗi 1 tiếng
@tasks.loop(hours=1)
async def hourly_notification():
    """Gửi thông báo cảnh báo scam mỗi 1 tiếng"""
    channel = bot.get_channel(NOTIFICATION_CHANNEL_ID)
    if channel:
        now = datetime.now()
        
        # Tạo embed đẹp với màu đỏ cảnh báo
        embed = discord.Embed(
            title="🚨 CẢNH BÁO QUAN TRỌNG - GANGS LORD OF CIARA 🚨",
            description="**⚠️ TRÁNH LỪA ĐẢO - BẢO VỆ TÀI SẢN CỦA BẠN ⚠️**",
            color=0xFF0000,  # Màu đỏ
            timestamp=now
        )
        
        # Thumbnail - logo cảnh báo
        embed.set_thumbnail(url="https://media.tenor.com/images/c6d8a726d477650f9f3d03f9ab3e9f8a/tenor.gif")
        
        # GIF cảnh báo lớn
        embed.set_image(url="https://media.tenor.com/VQBOFXjguZAAAAAC/warning-alerts.gif")
        
        # Nội dung cảnh báo
        embed.add_field(
            name="❌ TUYỆT ĐỐI KHÔNG",
            value=(
                "```diff\n"
                "- ❌ Giao dịch trực tiếp với người chơi\n"
                "- ❌ Cho mượn đồ/vật phẩm ingame\n"
                "- ❌ Đưa đồ trước khi nhận tiền\n"
                "- ❌ Tin tưởng lời hứa hẹn bằng miệng\n"
                "- ❌ Giao dịch qua Zalo/Facebook cá nhân\n"
                "```"
            ),
            inline=False
        )
        
        embed.add_field(
            name="✅ LUÔN GHI NHỚ",
            value=(
                "```fix\n"
                "+ ✅ Giao dịch QUA BAN QUẢN TRỊ\n"
                "+ ✅ Sử dụng hệ thống Trade chính thức\n"
                "+ ✅ Chụp ảnh bằng chứng mọi giao dịch\n"
                "+ ✅ Báo ngay cho Admin khi có nghi ngờ\n"
                "+ ✅ Kiểm tra kỹ trước khi xác nhận\n"
                "```"
            ),
            inline=False
        )
        
        embed.add_field(
            name="🛡️ BẢO VỆ TÀI KHOẢN",
            value=(
                "• Không chia sẻ mật khẩu với BẤT KỲ AI\n"
                "• Không click vào link lạ\n"
                "• Bật xác thực 2 bước nếu có\n"
                "• Đổi mật khẩu thường xuyên"
            ),
            inline=False
        )
        
        embed.add_field(
            name="📞 LIÊN HỆ KHI CẦN TRỢ GIÚP",
            value=(
                "🔹 Tag **@Admin** hoặc **@Moderator**\n"
                "🔹 Tạo ticket trong kênh hỗ trợ\n"
                "🔹 **KHÔNG** giao dịch khi Admin offline"
            ),
            inline=False
        )
        
        # Footer
        embed.set_footer(
            text="🎮 Gangs Lord of Ciara | Chơi game an toàn - Tránh xa lừa đảo",
            icon_url="https://cdn-icons-png.flaticon.com/512/2235/2235683.png"
        )
        
        # Gửi thông báo
        await channel.send(
            content="⚠️ **@everyone - THÔNG BÁO QUAN TRỌNG** ⚠️",
            embed=embed
        )
        print(f"✅ Đã gửi thông báo tự động lúc {now.strftime('%H:%M:%S')}")

@hourly_notification.before_loop
async def before_hourly_notification():
    """Đợi bot sẵn sàng trước khi bắt đầu loop"""
    await bot.wait_until_ready()
    print("🔔 Đã khởi động thông báo tự động mỗi 1 tiếng!")

# Lệnh gửi thông báo tùy chỉnh
@bot.command(name='thongbao')
async def send_notification(ctx, *, message):
    """Gửi thông báo tùy chỉnh với design đẹp"""
    channel = bot.get_channel(NOTIFICATION_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="📢 THÔNG BÁO QUAN TRỌNG",
            description=message,
            color=0x00ff00,
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url="https://media.tenor.com/iKaRCHu3uV0AAAAC/notification-bell.gif")
        embed.set_footer(
            text=f"Thông báo bởi {ctx.author.name}",
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None
        )
        await channel.send(embed=embed)
        await ctx.send("✅ Đã gửi thông báo!")
    else:
        await ctx.send("❌ Không tìm thấy channel!")

# Lệnh gửi thông báo khẩn cấp
@bot.command(name='khancap')
async def urgent_notification(ctx, *, message):
    """Gửi thông báo khẩn cấp với @everyone"""
    channel = bot.get_channel(NOTIFICATION_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="🚨 CẢNH BÁO KHẨN CẤP 🚨",
            description=message,
            color=0xFF0000,
            timestamp=datetime.now()
        )
        embed.set_image(url="https://media.tenor.com/VQBOFXjguZAAAAAC/warning-alerts.gif")
        embed.set_footer(
            text=f"Cảnh báo bởi {ctx.author.name}",
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None
        )
        await channel.send("@everyone ⚠️ **THÔNG BÁO KHẨN CẤP** ⚠️", embed=embed)
        await ctx.send("✅ Đã gửi thông báo khẩn cấp!")
    else:
        await ctx.send("❌ Không tìm thấy channel!")

# Lệnh gửi thông báo với delay
@bot.command(name='hentgio')
async def delayed_notification(ctx, minutes: int, *, message):
    """Gửi thông báo sau một khoảng thời gian
    
    Cách dùng: !hentgio 30 Nội dung thông báo
    """
    if minutes <= 0 or minutes > 1440:  # Giới hạn tối đa 24 giờ
        await ctx.send("❌ Thời gian phải từ 1-1440 phút (tối đa 24 giờ)!")
        return
        
    await ctx.send(f"⏰ Sẽ gửi thông báo sau {minutes} phút")
    await asyncio.sleep(minutes * 60)
    
    channel = bot.get_channel(NOTIFICATION_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="⏰ NHẮC NHỞ",
            description=message,
            color=0xFFA500,
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url="https://media.tenor.com/7VKLTb9RkhcAAAAC/alarm-clock.gif")
        embed.set_footer(
            text=f"Đặt lịch bởi {ctx.author.name}",
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None
        )
        await channel.send(embed=embed)

# Lệnh kiểm tra bot
@bot.command(name='ping')
async def ping(ctx):
    """Kiểm tra bot có hoạt động không"""
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Bot đang hoạt động bình thường\nĐộ trễ: **{latency}ms**",
        color=0x00ff00
    )
    await ctx.send(embed=embed)

# Lệnh help tùy chỉnh
@bot.command(name='help_bot')
async def help_command(ctx):
    """Hiển thị hướng dẫn sử dụng bot"""
    embed = discord.Embed(
        title="📖 HƯỚNG DẪN SỬ DỤNG BOT",
        description="Bot thông báo và cảnh báo cho Gangs Lord of Ciara",
        color=0x3498db
    )
    
    embed.add_field(
        name="🔔 Thông báo tự động",
        value="Bot tự động gửi cảnh báo chống scam **mỗi 1 tiếng**",
        inline=False
    )
    
    embed.add_field(
        name="📢 !thongbao <nội dung>",
        value="Gửi thông báo thông thường\nVí dụ: `!thongbao Server maintenance lúc 20h`",
        inline=False
    )
    
    embed.add_field(
        name="🚨 !khancap <nội dung>",
        value="Gửi thông báo khẩn cấp với @everyone\nVí dụ: `!khancap Phát hiện scammer mới!`",
        inline=False
    )
    
    embed.add_field(
        name="⏰ !hentgio <phút> <nội dung>",
        value="Gửi thông báo sau một khoảng thời gian\nVí dụ: `!hentgio 30 Event bắt đầu sau 30 phút`",
        inline=False
    )
    
    embed.add_field(
        name="🏓 !ping",
        value="Kiểm tra bot có hoạt động không",
        inline=False
    )
    
    embed.set_footer(text="🎮 Gangs Lord of Ciara - Stay Safe!")
    await ctx.send(embed=embed)

# Error handler
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Lệnh không tồn tại! Dùng `!help_bot` để xem danh sách lệnh.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Thiếu tham số! Dùng `!help_bot` để xem cách dùng.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Tham số không hợp lệ! Vui lòng kiểm tra lại.")
    else:
        print(f"❌ Lỗi: {error}")

# Chạy bot
if __name__ == "__main__":
    if not TOKEN:
        print("❌ ERROR: DISCORD_TOKEN không được thiết lập!")
        print("Vui lòng thiết lập biến môi trường DISCORD_TOKEN")
    elif NOTIFICATION_CHANNEL_ID == 0:
        print("❌ ERROR: CHANNEL_ID không được thiết lập!")
        print("Vui lòng thiết lập biến môi trường CHANNEL_ID")
    else:
        try:
            bot.run(TOKEN)
        except Exception as e:
            print(f"❌ Lỗi khi chạy bot: {e}")
