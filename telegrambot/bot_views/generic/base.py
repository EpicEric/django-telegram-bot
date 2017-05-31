from telegrambot.bot_views.generic.responses import TextResponse, KeyboardResponse
from telegram import ParseMode
import sys
import traceback
import logging

logger = logging.getLogger(__name__)
PY3 = sys.version_info > (3,)


class NoResponseCommandView(object):
    def perform_action(self, bot, update, **kwargs):
        pass

    def handle(self, bot, update, **kwargs):
        self.perform_action(bot, update, **kwargs)

    @classmethod
    def as_command_view(cls, **initkwargs):
        def view(bot, update, **kwargs):
            self = cls(**initkwargs)
            return self.handle(bot, update, **kwargs)
        return view


class TemplateCommandView(NoResponseCommandView):
    template_text = None
    template_keyboard = None
    parse_mode = ParseMode.MARKDOWN
    disable_web_page_preview = False

    def get_context(self, bot, update, **kwargs):
        return None

    def handle(self, bot, update, **kwargs):
        try:
            ctx = self.get_context(bot, update, **kwargs)
            text = TextResponse(self.template_text, ctx).render()
            keyboard = KeyboardResponse(self.template_keyboard, ctx).render()
#             logger.debug("Text:" + str(text.encode('utf-8')))
#             logger.debug("Keyboard:" + str(keyboard))
            if text:
                if not PY3:
                    text = text.encode('utf-8')
                bot.send_message(chat_id=update.message.chat_id, text=text, reply_markup=keyboard, parse_mode=self.parse_mode, disable_web_page_preview=self.disable_web_page_preview)
            else:
                logger.info("No text response for update %s" % str(update))
        except:
            exc_info = sys.exc_info()
            traceback.print_exception(*exc_info)
            raise
