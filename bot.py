import asyncio, uuid
import discord, Auto, requests
from discord_components.interaction import Interaction, InteractionType
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_components import DiscordComponents, Button, ActionRow
from database import database as db
import random, string
TOKEN = ""

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
ban = {}
headers = {
    "Authorization": "Bot "+TOKEN
}
charge_limit = {}
slash = SlashCommand(bot)
async def NoRegisterException(ctx): 
    embed = discord.Embed()
    embed.title = "❌ 가입이 되어있지 않습니다."
    embed.description = "/가입 명령어로 가입을 시도해 주세요."
    await ctx.send(embed=embed)
    


@bot.event
async def on_ready():
    print("Ready!")
    print(f"https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot%20applications.commands")
    DiscordComponents(bot)
    while True:
        await bot.change_presence(activity=discord.Game(f"SlashVend | {len(bot.guilds)}서버 사용중 | https://discord.gg/DISCORDSERVER"),status=discord.Status.online)
        await asyncio.sleep(5)
@slash.slash(name="버튼설정")
async def _btnsetting(ctx: SlashContext):
    if not ctx.author.guild_permissions.administrator:
        embed = discord.Embed()
        embed.title = "❌ 관리자만 사용 가능합니다."
        embed.description = "관리자 권한이 필요합니다."
        await ctx.send(embed=embed)
        return 
    embed = discord.Embed()
    embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
    embed.title = "ButtonVend by. ULTRA"
    embed.description = "원하시는 버튼을 누르세요.."
    await ctx.send("Success!")
    await ctx.channel.send(
        embed=embed,
        components = [
            ActionRow(
                Button(label = "가입"),
                Button(label = "구매"),
                Button(label = "잔액"),
                Button(label = "제품목록"),
                Button(label = "충전")
            )
        ]
    )
    return

@bot.event
# @commands.cooldown(1, 30, commands.BucketType.user)
async def on_button_click(ctx: Interaction):
    global ban
    if ctx.component.label == "가입":
        query = db.select("users", guild_id=ctx.guild.id, user_id=ctx.author.id)
        embed = discord.Embed()
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        if query:
            embed.title = "❌ 이미 가입되어 있습니다."
            embed.description = "이미 가입되어 있습니다.\n모든 자판기의 기능을 사용하실 수 있습니다."
        else:
            embed.title = "⭕ 성공적으로 가입 되었습니다."
            embed.description = "모든 자판기의 기능을 사용하실 수 있습니다."
            db.insert("users", guild_id=ctx.guild.id, user_id=ctx.author.id)

        await ctx.respond(embed=embed)
        return
    elif ctx.component.label == "제품목록":
        query = db.select("users", guild_id=ctx.guild.id, user_id=ctx.author.id)
        embed = discord.Embed()
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        if not query:
            await NoRegisterException(ctx)
            return
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        query = db.select("product", guild_id=ctx.guild.id)
        for i in query:
            stock_query = db.select("stock", product_id=i[1], guild_id=ctx.guild.id)
            embed.add_field(name=i[2], value=f"가격: `{i[3]}원`\n재고: `{len(stock_query)}개`", inline=True)
        await ctx.respond(embed=embed)
        return
    elif ctx.component.label == "잔액":
        query = db.select("users", guild_id=ctx.guild.id, user_id=ctx.author.id)
        embed = discord.Embed()
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        if not query:
            await NoRegisterException(ctx)
            return
        user_amount = int(query[0][2])
        embed.title = "⭕ 성공적으로 잔액을 불어왔습니다."
        embed.description = f"잔액: `{user_amount}원`"
        await ctx.respond(embed=embed)
        return
    elif ctx.component.label == "충전":
        if charge_limit.get(str(ctx.author.id), 0):
            msg = '이 버튼은 사용제한되었습니다. {}.00초 후에 다시 시도해 주세요.'.format(charge_limit.get(str(ctx.author.id)))
            await ctx.respond(content=msg)
            return
        charge_limit[str(ctx.author.id)] = 180
        embed = discord.Embed()
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        query = db.select("users", guild_id=ctx.guild.id, user_id=ctx.author.id)
        if not query:
            await NoRegisterException(ctx)
            return
        if query[0][4] == "true":
            embed.title = "❌ 충전에 실패했습니다."
            embed.description = f"{ctx.author.mention}님은 자동충전이 차단되었습니다."
            await ctx.send(embed=embed)
            return
        embed.title = "⭕ 성공적으로 요청했습니다."
        embed.description = "문화상품권 코드를 입력해 주세요."
        코드 = ""
        comp = [
            Button(label="1", id="1"),
            Button(label="2", id="2"),
            Button(label="3", id="3"),
            Button(label="4", id="4"),
            Button(label="5", id="5"),
        ]
        comp2 = [
            Button(label="6", id="6"),
            Button(label="7", id="7"),
            Button(label="8", id="8"),
            Button(label="9", id="9"),
            Button(label="0", id="0"),
        ]
        comp3 = [
            Button(label="#", id="#"),
        ]
        embed.title = "⭕ 성공적으로 요청했습니다."
        embed.description = "문상코드를 입력해 주세요. \n다 입력하셨다면 #를 입력해 주세요."
        # await interaction.respond(
        #     embed=embed,
        #     components=comp
        # )
        # await ctx.author.send(
        #     embed=embed ,
        #     components=comp
        # )
        # embed.title = ""
        # embed.description = ""
        # await ctx.author.send(
        #     embed=embed, 
        #     components=comp2
        # )
        # await ctx.author.send(
        #     embed=embed,
        #     components=comp3
        # )

        await ctx.respond(
            content=ctx.author.mention,
            embed=embed,
            components=[
                ActionRow(*comp),
                ActionRow(*comp2),
                ActionRow(*comp3)
            ]
        )
        def check(_btn: Interaction):
            if _btn.component.id in list("0123456789#"):
                if _btn.author.id == ctx.author.id:
                    return True    
            return False
        res = None
        while True:
            interaction = await bot.wait_for("button_click", check=check)
            if interaction.component.id == "#":
                if len(코드) == 19:
                    await interaction.respond(content=코드)
                    break   
            코드 += interaction.component.id   
            print(코드, len(코드))
            if len(코드) == 4 or len(코드) == 9 or len(코드) == 14:
                코드 += "-"
            if len(코드) == 21:
                await interaction.respond(content=코드)
                break
            await interaction.respond(type=InteractionType.DeferredUpdateMessage, content="asdf")
            # res = await interaction.respond(content=코드)

        query = db.select("users", guild_id=ctx.guild.id, user_id=ctx.author.id)
        embed = discord.Embed()
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        if not query:
            await NoRegisterException(ctx)
            return
        user_amount = int(query[0][2])
        query = db.select("culture", guild_id=ctx.guild.id)
        if not query:
            embed.title = "❌ 충전에 실패했습니다."
            embed.description = f"컬쳐랜드 계정이 설정되어 있지 않습니다."
            await ctx.author.send(embed=embed)
            return
        token = query[0][1]
        amount, message = Auto.CulturelandAutoCharge(token,코드)
        query = db.select("webhook", guild_id=ctx.guild.id)
        if query:
            requests.post(query[0][2], data={"content": f"{ctx.author.mention} \n충전된 금액: {amount} \n{message}"})
        if amount:
            embed.title = "⭕ 성공적으로 충전되었습니다."
            embed.description = message
            db.update("users", "amount", str(user_amount + amount), guild_id=ctx.guild.id, user_id=ctx.author.id)
            
        else:
            embed.title = "❌ 충전에 실패했습니다."
            stt = f"{ctx.guild.id}-{ctx.author.id}"
            ban[stt] = str(int(ban.get(stt, 0)) + 1)
            if ban[stt] == "2": db.update("users", "ban", "true", guild_id=ctx.guild.id, user_id=ctx.author.id)
            embed.description = message
        await ctx.author.send(embed=embed)
        for i in range(charge_limit[str(ctx.author.id)]):
            charge_limit[str(ctx.author.id)] -= 1
            await asyncio.sleep(1)
        
        return
    elif ctx.component.label == "구매":
        embed = discord.Embed()
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        query = db.select("users", guild_id=ctx.guild.id, user_id=ctx.author.id)
        if not query:
            await NoRegisterException(ctx)
            return
        embed.title = "⭕ 성공적으로 요청했습니다."
        embed.description = "구매하실 상품을 선택해 주세요."
        query = db.select("product", guild_id=ctx.guild.id)
        comp = []
        c = {}
        for i in query:
            st = "".join(random.choice(string.digits) for _ in range(4))
            c[st] = i[2]
            comp.append(Button(label = i[2], id=st))
        s = []
        for i in range(5):
            ss = []
            for j in range(5):
                try:
                    k = int(i+1)  * int(j+1)
                    if i == 0:
                        k = j
                    if j == 0:
                        k == i
                    ss.append(comp[k])
                except:
                    break
            if len(ss):
                s.append(ActionRow(*ss))
        res = await ctx.respond(
            embed=embed,
            components=s
        )
        def check(_btn: Interaction):
            if _btn.component.id in c.keys():
                if _btn.author.id == ctx.author.id:
                    return True    
            return False
        interaction = await bot.wait_for("button_click", check=check)
        상품명 = c[interaction.component.id]
        
        개수 = ""
        comp = [
            
            Button(label="1", id="1"),
            Button(label="2", id="2"),
            Button(label="3", id="3"),
            Button(label="4", id="4"),
            Button(label="5", id="5"),
        ]
        comp2 = [
            Button(label="6", id="6"),
            Button(label="7", id="7"),
            Button(label="8", id="8"),
            Button(label="9", id="9"),
            Button(label="0", id="0"),
        ]
        comp3 = [
            Button(label="#", id="#"),
        ]
        embed.title = "⭕ 성공적으로 요청했습니다."
        embed.description = "구매하실 갯수를 입력해 주세요. \n다 입력하셨다면 #를 입력해 주세요."
        # await interaction.respond(
        #     embed=embed,
        #     components=comp
        # )
        
        await interaction.respond(
            content=ctx.author.mention,
            embed=embed,
            components=[
                ActionRow(*comp),
                ActionRow(*comp2),
                ActionRow(*comp3),
            ]
        )
        def check(_btn: Interaction):
            if _btn.component.id in list("0123456789#"):
                if _btn.author.id == ctx.author.id:
                    return True    
            return False
            
        while True:
            interaction = await bot.wait_for("button_click", check=check)
            if interaction.component.id == "#":
                await interaction.respond(content=f"{개수}개")
                break   
            개수 += interaction.component.id   
            await interaction.respond(type=InteractionType.DeferredUpdateMessage, content="asdf")
        개수 = int(개수)
        embed = discord.Embed()
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        query = db.select("users", guild_id=ctx.guild.id, user_id=ctx.author.id)
        if 개수 <= 0:
            embed.title = "❌ 구매 실패"
            embed.description = "개수는 1 이상이여야 됩니다."
            await ctx.author.send(embed=embed)
            return
        if not query:
            await NoRegisterException(ctx)
            return
        user_amount = int(query[0][2])
        query = db.select("product", guild_id=ctx.guild.id, name=상품명)
        if query:
            stock_query = db.select("stock", product_id=query[0][1], guild_id=ctx.guild.id)
            if len(stock_query) < 개수:
                embed.title = "❌ 구매 실패"
                embed.description = "재고가 부족합니다."
                await ctx.author.send(embed=embed)
                return
            price = int(query[0][3]) * 개수
            if price > user_amount:
                embed.title = "❌ 구매 실패"
                embed.description = "잔액이 부족합니다."
                await ctx.author.send(embed=embed)
                return
            
            embed.title = "⭕ 구매 성공"
            embed.description = "성공적으로 구매했습니다."
            db.update("users", "amount", str(user_amount - price), guild_id=ctx.guild.id, user_id=ctx.author.id)
            stock_query = db.select("stock", product_id=query[0][1], guild_id=ctx.guild.id)
            st = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
            for i in range(개수):
                stock = stock_query[i]
                db.insert("raw", id=st, value=stock[2])
                db.delete("stock", guild_id=ctx.guild.id, product_id=query[0][1], value=stock[2])
            await ctx.author.send(embed=embed)
            embed = discord.Embed()
            embed.title = "상품이 구매되었습니다."
            embed.description = f"https://vend.ultra0221.me/raw/{st} \n상품이름: {상품명} \n개수: {개수}"
            query = db.select("role", guild_id=ctx.guild.id)
            if query:
                role = ctx.guild.get_role(int(query[0][1]))
                await ctx.author.add_roles(role)
            query = db.select("role", guild_id=ctx.guild.id)
            if query:
                role = ctx.guild.get_role(int(query[0][1]))
                await ctx.author.add_roles(role)
            query = db.select("webhook", guild_id=ctx.guild.id)
            if query:
                requests.post(query[0][1], data={"content": f"{ctx.author.mention} 님! `{상품명}` `{개수}개` 구매 감사합니다."})
                requests.post(query[0][2], data={"content": f"{ctx.author.mention} \nhttps://vend.ultra0221.me/raw/{st} \n상품이름: {상품명} \n개수: {개수}"})
                
                await ctx.author.add_roles(role)
            await ctx.author.send(embed=embed)
        else:
            embed.title = "❌ 구매 실패"
            embed.description = "알 수 없는 상품 입니다."
            await ctx.author.send(embed=embed)
            return
    


@slash.slash(name="패널")
async def _panel(ctx: SlashContext):
    if not ctx.author.guild_permissions.administrator:
        embed = discord.Embed()
        embed.title = "❌ 관리자만 사용 가능합니다."
        embed.description = "관리자 권한이 필요합니다."
        await ctx.send(embed=embed)
        return 
    query = db.select("panel", guild_id=ctx.guild.id)
    embed = discord.Embed()
    embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
    embed.title = "⭕ DM을 확인해 주세요."
    embed.description = "관리자 패널 정보를 DM으로 전송해 드렸습니다."
    if query:
        passwd = query[0][1]
    else:
        passwd = "".join(random.choice(string.ascii_letters + string.digits + "!@#$") for _ in range(20))
        db.insert("panel", guild_id=ctx.guild.id, password=passwd)
    await ctx.send(embed=embed)


    embed = discord.Embed()
    embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
    embed.title = "⭕ 관리자 패널 정보 입니다."
    embed.description = f"ID: `{ctx.guild.id}`\nPW: `{passwd}`\nSITE: `https://vend.ultra0221.me`"
    await ctx.author.send(embed=embed)
    return
@slash.slash(name="구매")
async def _pur(ctx: SlashContext, 상품명: str, 개수: int):
    embed = discord.Embed()
    embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
    query = db.select("users", guild_id=ctx.guild.id, user_id=ctx.author.id)
    if 개수 <= 0:
        embed.title = "❌ 구매 실패"
        embed.description = "개수는 1 이상이여야 됩니다."
        await ctx.send(embed=embed)
        return
    if not query:
        await NoRegisterException(ctx)
        return
    user_amount = int(query[0][2])
    query = db.select("product", guild_id=ctx.guild.id, name=상품명)
    if query:
        stock_query = db.select("stock", product_id=query[0][1], guild_id=ctx.guild.id)
        if len(stock_query) < 개수:
            embed.title = "❌ 구매 실패"
            embed.description = "재고가 부족합니다."
            await ctx.send(embed=embed)
            return
        price = int(query[0][3]) * 개수
        if price > user_amount:
            embed.title = "❌ 구매 실패"
            embed.description = "잔액이 부족합니다."
            await ctx.send(embed=embed)
            return
        
        embed.title = "⭕ 구매 성공"
        embed.description = "성공적으로 구매했습니다."
        db.update("users", "amount", str(user_amount - price), guild_id=ctx.guild.id, user_id=ctx.author.id)
        stock_query = db.select("stock", product_id=query[0][1], guild_id=ctx.guild.id)
        st = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
        for i in range(개수):
            stock = stock_query[i]
            db.insert("raw", id=st, value=stock[2])
            db.delete("stock", guild_id=ctx.guild.id, product_id=query[0][1], value=stock[2])
        await ctx.send(embed=embed)
        embed = discord.Embed()
        embed.title = "상품이 구매되었습니다."
        embed.description = f"https://vend.ultra0221.me/raw/{st} \n상품이름: {상품명} \n개수: {개수}"
        query = db.select("role", guild_id=ctx.guild.id)
        if query:
            role = ctx.guild.get_role(int(query[0][1]))
            await ctx.author.add_roles(role)
        query = db.select("role", guild_id=ctx.guild.id)
        if query:
            role = ctx.guild.get_role(int(query[0][1]))
            await ctx.author.add_roles(role)
        query = db.select("webhook", guild_id=ctx.guild.id)
        if query:
            requests.post(query[0][1], data={"content": f"{ctx.author.mention} 님! `{상품명}` `{개수}개` 구매 감사합니다."})
            requests.post(query[0][2], data={"content": f"{ctx.author.mention} \nhttps://vend.ultra0221.me/raw/{st} \n상품이름: {상품명} \n개수: {개수}"})
            
            await ctx.author.add_roles(role)
        await ctx.author.send(embed=embed)
    else:
        embed.title = "❌ 구매 실패"
        embed.description = "알 수 없는 상품 입니다."
        await ctx.send(embed=embed)
        return
    # await ctx.send(embed=embed)
@slash.slash(name="제품목록")
async def _productlist(ctx: SlashContext):
    query = db.select("users", guild_id=ctx.guild.id, user_id=ctx.author.id)
    embed = discord.Embed()
    embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
    if not query:
        await NoRegisterException(ctx)
        return
    embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
    query = db.select("product", guild_id=ctx.guild.id)
    for i in query:
        stock_query = db.select("stock", product_id=i[1], guild_id=ctx.guild.id)
        embed.add_field(name=i[2], value=f"가격: `{i[3]}원`\n재고: `{len(stock_query)}개`", inline=True)
    await ctx.send(embed=embed)
@slash.slash(name="가입")
async def _join(ctx: SlashContext):
    query = db.select("users", guild_id=ctx.guild.id, user_id=ctx.author.id)
    embed = discord.Embed()
    embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
    if query:
        embed.title = "❌ 이미 가입되어 있습니다."
        embed.description = "이미 가입되어 있습니다.\n모든 자판기의 기능을 사용하실 수 있습니다."
    else:
        embed.title = "⭕ 성공적으로 가입 되었습니다."
        embed.description = "모든 자판기의 기능을 사용하실 수 있습니다."
        db.insert("users", guild_id=ctx.guild.id, user_id=ctx.author.id)

    await ctx.send(embed=embed)
    return
@slash.slash(name="잔액")
async def _info(ctx: SlashContext):
    query = db.select("users", guild_id=ctx.guild.id, user_id=ctx.author.id)
    embed = discord.Embed()
    embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
    if not query:
        await NoRegisterException(ctx)
        return
    user_amount = int(query[0][2])
    embed.title = "⭕ 성공적으로 잔액을 불어왔습니다."
    embed.description = f"잔액: `{user_amount}원`"
    await ctx.send(embed=embed)
        
    return
@slash.slash(name="충전")
@commands.cooldown(1, 180, commands.BucketType.user)
async def _charge(ctx: SlashContext, 코드: str):
    query = db.select("users", guild_id=ctx.guild.id, user_id=ctx.author.id)
    embed = discord.Embed()
    embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
    if not query:
        await NoRegisterException(ctx)
        return
    if query[0][4] == "true":
        embed.title = "❌ 충전에 실패했습니다."
        embed.description = f"{ctx.author.mention}님은 자동충전이 차단되었습니다."
        await ctx.send(embed=embed)
        return
    user_amount = int(query[0][2])
    query = db.select("culture", guild_id=ctx.guild.id)
    # embed.title = "충전 신청되었습니다."
    # embed.description = f"컬쳐랜드 계정이 설정되어 있지 않습니다."
    # await ctx.send(embed=embed)
    if not query:
        embed.title = "❌ 충전에 실패했습니다."
        embed.description = f"컬쳐랜드 계정이 설정되어 있지 않습니다."
        await ctx.send(embed=embed)
        return
    token = query[0][1]
    amount, message = Auto.CulturelandAutoCharge(token,코드)
    query = db.select("webhook", guild_id=ctx.guild.id)
    if query:
        requests.post(query[0][2], data={"content": f"{ctx.author.mention} \n충전된 금액: {amount} \n{message}"})
    if amount:
        embed.title = "⭕ 성공적으로 충전되었습니다."
        embed.description = message
        db.update("users", "amount", str(user_amount + amount), guild_id=ctx.guild.id, user_id=ctx.author.id)
        
    else:
        stt = f"{ctx.guild.id}-{ctx.author.id}"
        ban[stt] = str(int(ban.get(stt, 0)) + 1)
        if ban[stt] == "2": db.update("users", "ban", "true", guild_id=ctx.guild.id, user_id=ctx.author.id)
        embed.title = "❌ 충전에 실패했습니다."
        embed.description = message
    await ctx.send(embed=embed)
    return
# @bot.listen()
# async def on_command_error(ctx, error):
#     pass
@bot.listen()
async def on_slash_command_error(ctx: SlashContext, error):
    print(error)

    if isinstance(error, commands.CommandOnCooldown):
        msg = '이 명령어는 사용제한되었습니다. {:.2f}초 후에 다시 시도해 주세요.'.format(error.retry_after)
        await ctx.send(msg)
        return
    raise error
    

if __name__ == "__main__":
    bot.run(TOKEN)
