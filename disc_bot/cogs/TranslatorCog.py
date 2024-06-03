from discord.ext import commands

import logging
from ..cog_helpers.translator import Translator
logger = logging.getLogger('translator')



class Translation_Commands(commands.Cog):

    def __init__(self, bot, translator=None):
        self.bot = bot
        self.translator = ( translator 
                          if translator is not None 
                          else Translator(auto_translate = True))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author != self.bot.user:
            logger.info(f'User {message.author} sent "{message.clean_content}"')
            translated = self.translator.translate(message.content)
            if translated and translated != message.content:
                logger.debug(
                    f'BOT TRANSLATION EVENT::' 
                    + f'"{message.content}" -> {translated}'
                )
                await message.channel.send(translated)

    @commands.command()
    async def set_language(self, ctx, language: str):
        self.translator.set_language(language)
        await ctx.send(f"Changed default language to {language}")

    @commands.command()
    async def print_language(self, ctx):
        await ctx.send(self.translator.curr_lang)

    @commands.command()
    async def possible_languages(self, ctx):
        await ctx.send(self.translator.format_possible_languages())

    def repr(self):
        return f"{self.__class__.__name__}"

    def str(self):
        return repr(self)
