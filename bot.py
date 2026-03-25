import discord
import json
import os

intents = discord.Intents.all()
client = discord.Client(intents=intents)

# データ読み込み
try:
    with open("counts.json", "r") as f:
        data = json.load(f)
except:
    data = {}

@client.event
async def on_ready():
    print("起動成功:", client.user)

@client.event
async def on_message(message):
    if message.author.bot:
        return

    print("受信:", message.content)

    user_id = str(message.author.id)

    # 👇 好きなワードに変えてOK
    if "うお" in message.content or "しね" in message.content:

        if user_id not in data:
            data[user_id] = 0

        data[user_id] += 1

        with open("counts.json", "w") as f:
            json.dump(data, f)

        await message.channel.send(
            f"{message.author.mention} さん {data[user_id]} 回目の冷笑です！おめでとう！"
        )

    # 👇 ランキングコマンド
    if message.content == "!rank":

        if not data:
            await message.channel.send("まだデータがないよ")
            return

        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)

        msg = "🏆 ランキング\n"

        for i, (user_id, count) in enumerate(sorted_data[:10], start=1):
            try:
                user = await client.fetch_user(int(user_id))
                name = user.name
            except:
                name = "不明ユーザー"

            msg += f"{i}位: {name} - {count}回\n"

        await message.channel.send(msg)

TOKEN = os.getenv("TOKEN")

from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive"

def run_web():
    app.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_web).start()

client.run(TOKEN)
