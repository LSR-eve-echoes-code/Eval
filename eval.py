from discord.ext import commands, tasks
import traceback
import discord
import re
import math


class eval_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pattern = re.compile(r"`\.eval (.+)$`")

    @commands.command()
    async def eval(self, ctx, *args):
        args = " ".join(args)
        ret = self._eval(args)
        if ret[0]:
            await self.bot.send(ctx, f'result: {ret[1]}')
        else:
            await self.bot.send(ctx, ret[1])

    def _eval(self, args):
        if args[0] == '`':
            args = args[1:]
        if args[-1] == '`':
            args = args[:-1]
        a = set(args)
        b = set('1234567890*/()+- ,.')
        chk = a - b
        if len(chk) > 0:
            return (False, f'illegal symbols: {chk}')
        else:
            return (True, eval(args))

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.author.bot:
                return

            content = message.content
            msg = content
            slices = msg.split('`.eval ')
            if len(slices) < 2:
                return
            ret = slices[0]
            for i in slices[1:]:
                s, tail = i.split('`')
                n = self._eval(s)
                if n[0]:
                    ret += str(n[1]) 
                else:
                    ret += '`' + n[1] + '`'
                ret += ' ' + tail

            await message.channel.send(ret)
        except:
            traceback.print_exc()

async def setup(bot):
    l = eval_cog(bot)
    await bot.add_cog(l)
    print('eval cog loaded')


