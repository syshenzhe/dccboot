import discord
from discord.ext import commands
import asyncio
import time
import random

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

free_stock = {"steam": []}
premium_stock = {"steam": []}
last_used = {}

# Yalnızca bu ID'lerdeki kişiler admin yetkili
AUTHORIZED_ADMINS = [1284167857231364118, 1230072380467056710]  # <--- KENDİ ID'LERİNİ YAZ

# Free stok ekleme
@bot.command()
async def freegenekle(ctx, platform, *, hesap):
    if ctx.author.id not in AUTHORIZED_ADMINS:
        await ctx.send("❌ Bu komutu sadece yetkili adminler kullanabilir.")
        return
    free_stock.setdefault(platform, []).append(hesap)
    await ctx.send(f"✅ Free stock'a eklendi: {platform}")

# Premium stok ekleme
@bot.command()
async def premiumgenekle(ctx, platform, *, hesap):
    if ctx.author.id not in AUTHORIZED_ADMINS:
        await ctx.send("❌ Bu komutu sadece yetkili adminler kullanabilir.")
        return
    premium_stock.setdefault(platform, []).append(hesap)
    await ctx.send(f"✅ Premium stock'a eklendi: {platform}")

# Free stok temizleme
@bot.command()
async def freegensil(ctx, platform):
    if ctx.author.id not in AUTHORIZED_ADMINS:
        await ctx.send("❌ Bu komutu sadece yetkili adminler kullanabilir.")
        return
    free_stock[platform] = []
    await ctx.send(f"🗑️ Free stock temizlendi: {platform}")

# Premium stok temizleme
@bot.command()
async def premiumgensil(ctx, platform):
    if ctx.author.id not in AUTHORIZED_ADMINS:
        await ctx.send("❌ Bu komutu sadece yetkili adminler kullanabilir.")
        return
    premium_stock[platform] = []
    await ctx.send(f"🗑️ Premium stock temizlendi: {platform}")

# Free hesap alma (10 dk cooldown) - Silmeden rastgele verir
@bot.command()
async def freegen(ctx, platform):
    now = time.time()
    user_id = ctx.author.id
    if user_id in last_used and now - last_used[user_id] < 600:
        remaining = int(600 - (now - last_used[user_id]))
        await ctx.send(f"⏳ Lütfen {remaining} saniye bekle tekrar denemek için.")
        return

    if free_stock.get(platform):
        hesap = random.choice(free_stock[platform])
        await ctx.author.send(f"🔓 Free {platform} hesabın: `{hesap}`")
        await ctx.send("✅ Hesabın DM'den gönderildi.")
        last_used[user_id] = now
    else:
        await ctx.send("⚠️ Stokta hesap yok.")

# Premium hesap alma (sadece Premium rolü veya admin) - Silmeden rastgele verir
@bot.command()
async def premiumgen(ctx, platform):
    premium_role = discord.utils.get(ctx.guild.roles, name="Premium")
    if premium_role not in ctx.author.roles and not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Bu komutu sadece 'Premium' üyeler veya Adminler kullanabilir.")
        return

    if premium_stock.get(platform):
        hesap = random.choice(premium_stock[platform])
        await ctx.author.send(f"🔐 Premium {platform} hesabın: `{hesap}`")
        await ctx.send("✅ Hesabın DM'den gönderildi.")
    else:
        await ctx.send("⚠️ Premium stokta hesap yok.")

bot.run('MTM4MzUxMDU4OTE3MDUyMDIxNA.G4T6mT.xzWgx5eF97phT372V4MZ4PhK8a1cRiC8ZcP-gI')
