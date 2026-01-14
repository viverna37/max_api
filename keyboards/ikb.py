from maxapi.types import CallbackButton
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder


class IKB:
    class User:
        @staticmethod
        def get_verification_keyboard():
            builder = InlineKeyboardBuilder()
            builder.row(
                CallbackButton(text="Я человек", payload="im_human")
            )
            return builder.as_markup()

    class Admin:
        @staticmethod
        def get_admin_keyboard():
            builder = InlineKeyboardBuilder()
            builder.row(
                CallbackButton(text="Рассылки", payload="broadcast")
            )
            builder.row(
                CallbackButton(text="Изменить дефолт ссылку", payload="edit_link")
            )
            builder.row(
                CallbackButton(text="Изменить дефолт текст", payload="edit_message")
            )
            builder.row(
                CallbackButton(text="Создать кампанию", payload="create_campaign")
            )
            builder.row(
                CallbackButton(text="Мои кампании", payload="my_campaign")
            )
            return builder.as_markup()


        @staticmethod
        def broadcast_type_keyboard():
            builder = InlineKeyboardBuilder()
            builder.row(
                CallbackButton(text="Таргет рассылка", payload="broadcast_target")
            )
            builder.row(
                CallbackButton(text="Общая рассылка", payload="broadcast_all")
            )

            return builder.as_markup()

        @staticmethod
        def broadcast_keyboard(param: str):
            builder = InlineKeyboardBuilder()
            builder.row(
                CallbackButton(text="Рассылка текст", payload=f"broadcast_text_{param}")
            )
            builder.row(
                CallbackButton(text="Рассылка с фото", payload=f"broadcast_photo_{param}")
            )

            return builder.as_markup()