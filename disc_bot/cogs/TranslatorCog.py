from discord.ext import commands

import logging
logger = logging.getLogger('translator')



class Translation_Commands(commands.Cog):

    def __init__(self, bot, translator):
        self.bot = bot
        self.translator = translator

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author != self.bot.user:
            logger.info(f'User {message.author} sent "{message.clean_content}"')
            translated = self.translator.translate(message.content)
            if translated and translated != message.content:
                logger.debug(
                        f'Bot {self.bot.user} translated "{message.content}" -> {translated}'
                        )
                await message.channel.send(translated)

    def repr(self):
        return f"{self.__class__.__name__}"
