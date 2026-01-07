# 🎮 Gangs Lord of Ciara - Anti-Scam Bot

Bot Discord tự động cảnh báo người chơi về scam và lừa đảo trong game.

## ✨ Tính năng

- ⏰ Tự động gửi cảnh báo mỗi 1 tiếng
- 🎨 Embed đẹp với GIF động
- 📢 Thông báo tùy chỉnh qua lệnh
- 🚨 Cảnh báo khẩn cấp với @everyone
- ⏰ Hẹn giờ gửi thông báo

## 🛠️ Các lệnh

| Lệnh | Mô tả |
|------|-------|
| `!thongbao <nội dung>` | Gửi thông báo thông thường |
| `!khancap <nội dung>` | Gửi cảnh báo khẩn cấp |
| `!hentgio <phút> <nội dung>` | Gửi thông báo có hẹn giờ |
| `!ping` | Kiểm tra trạng thái bot |
| `!help_bot` | Xem hướng dẫn |

## 🚀 Deploy trên Railway

1. Push code lên GitHub
2. Đăng nhập Railway.app
3. New Project → Deploy from GitHub
4. Chọn repository
5. Thêm Environment Variables:
   - `DISCORD_TOKEN`: Token bot của bạn
   - `CHANNEL_ID`: ID channel nhận thông báo

## 📝 Cách lấy thông tin

### Lấy Discord Bot Token:
1. Vào https://discord.com/developers/applications
2. Chọn application của bạn → Bot
3. Reset Token → Copy token

### Lấy Channel ID:
1. Discord → Settings → Advanced → Enable Developer Mode
2. Click phải vào channel → Copy ID

### Mời Bot vào Server:
1. Discord Developer Portal → OAuth2 → URL Generator
2. Chọn scope: `bot`
3. Chọn permissions: `Send Messages`, `Embed Links`, `Mention Everyone`
4. Copy link và mở trong browser

## ⚙️ Yêu cầu

- Python 3.11+
- discord.py 2.3.2+
- Railway account (free tier)

## 📞 Hỗ trợ

Nếu gặp vấn đề, vui lòng tạo issue trên GitHub.

---

Made with ❤️ for Gangs Lord of Ciara Community
