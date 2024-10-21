import logging

from discord.ext import commands

from ..cog_helpers.translator import Translator


class Translation_Commands(commands.Cog):
    def __init__(self, bot, translator=None):
        self.bot = bot
        self.logger = logging.getLogger(self.__class__.__name__)
        self.translator = translator if translator is not None else Translator(auto_translate=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        checker = self.bot.get_cog("Checks")
        if checker.is_blacklisted(message.guild.id, message.channel.id):
            return
        elif message.author != self.bot.user:
            self.logger.info(f'User {message.author} sent "{message.clean_content}"')
            translated = self.translator.translate(message.content)
            if translated and translated != message.content:
                self.logger.debug(f"BOT TRANSLATION EVENT::'{message.content} -> {translated}'")
                await message.channel.send(translated)

    @commands.command()
    async def set_language(self, ctx, language: str):
        "Set the language to be translated into"
        self.translator.set_language(language)
        await ctx.send(f"Changed default language to {language}")

    @commands.command()
    async def print_language(self, ctx):
        "Print the current set language"
        await ctx.send(self.translator.curr_lang)

    @commands.command()
    async def possible_languages(self, ctx):
        "Print possible languages to be set to"
        await ctx.send(self.translator.format_possible_languages())

    def repr(self):
        return f"{self.__class__.__name__}"

    def str(self):
        return repr(self)


async def setup(bot):
    await bot.add_cog(Translation_Commands(bot))
