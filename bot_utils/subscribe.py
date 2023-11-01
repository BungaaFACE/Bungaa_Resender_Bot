from telethon import events, types, functions
from global_data import global_data, PROVIDER_TOKEN, CURRENCY, ONE_MONTH_PRICE
import datetime


resender_bot = global_data.resender_bot
"""
Provider token can be obtained via @BotFather. more info at https://core.telegram.org/bots/payments#getting-a-token

If you are using test token, set test=True in generate_invoice function,
If you are using real token, set test=False
"""
provider_token = PROVIDER_TOKEN


# That event is handled when customer enters his card/etc, on final pre-checkout
# If we don't `SetBotPrecheckoutResultsRequest`, money won't be charged from buyer, and nothing will happen next.
@resender_bot.on(events.Raw(types.UpdateBotPrecheckoutQuery))
async def payment_pre_checkout_handler(event: types.UpdateBotPrecheckoutQuery):
    if event.payload.decode('UTF-8') == 'one_month':
        # so we have to confirm payment
        await resender_bot(
            functions.messages.SetBotPrecheckoutResultsRequest(
                query_id=event.query_id,
                success=True,
                error=None
            )
        )
    else:
        # for example, something went wrong (whatever reason). We can tell customer about that:
        await resender_bot(
            functions.messages.SetBotPrecheckoutResultsRequest(
                query_id=event.query_id,
                success=False,
                error='Something went wrong'
            )
        )

    raise events.StopPropagation


# That event is handled at the end, when customer payed.
@resender_bot.on(events.Raw(types.UpdateNewMessage))
async def payment_received_handler(event):
    if isinstance(event.message.action, types.MessageActionPaymentSentMe):
        payment: types.MessageActionPaymentSentMe = event.message.action
        user_id = event.message.peer_id.user_id
        # do something after payment was received
        if payment.payload.decode('UTF-8') == 'one_month':
            one_month_delta = datetime.timedelta(days=30)

            if_subscribed_sql = f"SELECT expired_date IN subscribers WHERE subscriber_id = '{user_id}';"
            expired_date = global_data.custom_command(
                if_subscribed_sql, to_list=True)

            # Если уже подписан, то просто меняем ему дату окончания подписки
            if expired_date:
                expired_date = datetime.datetime.strptime(
                    expired_date, "%d-%m-%Y")

                new_end_date = (
                    current_date + one_month_delta).strftime("%d-%m-%Y")

                change_subscriber_date_sql = f"UPDATE subscribers SET expired_date='{new_end_date}' WHERE subscriber_id={user_id}"
                global_data.custom_command(change_subscriber_date_sql)
                global_data.update_subscribers()
                await resender_bot.send_message(user_id, f'Спасибо за покупку! Ваша подписка продлена до {new_end_date}. Данные о подписке обновятся в течение пары минут!')

            else:
                current_date = datetime.datetime.now()
                end_date = (current_date +
                            one_month_delta).strftime("%d-%m-%Y")

                add_subscriber_sql = f"INSERT INTO subscribers(subscriber_id, expired_date) VALUES ({user_id}, {end_date})"
                add_subscriber_preferences_sql = f"INSERT INTO sub_preferences(subscriber_id) VALUES ({user_id})"
                global_data.custom_command(add_subscriber_sql)
                global_data.custom_command(add_subscriber_preferences_sql)
                global_data.update_subscribers()
                await resender_bot.send_message(user_id, f'Спасибо за покупку! Ваша подписка установлена до {end_date}. Данные о подписке обновятся в течение пары минут!')
        raise events.StopPropagation


# let's put it in one function for more easier way
def generate_invoice(price_label: str, price_amount: int, currency: str, title: str,
                     description: str, payload: str, start_param: str) -> types.InputMediaInvoice:
    # label - just a text, amount=10000 means 100.00
    price = types.LabeledPrice(label=price_label, amount=price_amount)
    invoice = types.Invoice(
        currency=currency,  # currency like USD
        prices=[price],  # there could be a couple of prices.
        test=True,  # if you're working with test token, else set test=False.
        # More info at https://core.telegram.org/bots/payments

        # params for requesting specific fields
        name_requested=False,
        phone_requested=False,
        email_requested=False,
        shipping_address_requested=False,

        # if price changes depending on shipping
        flexible=False,

        # send data to provider
        phone_to_provider=False,
        email_to_provider=False
    )
    return types.InputMediaInvoice(
        title=title,
        description=description,
        invoice=invoice,
        # payload, which will be sent to next 2 handlers
        payload=payload.encode('UTF-8'),
        provider=provider_token,

        provider_data=types.DataJSON('{}'),
        # data about the invoice, which will be shared with the payment provider. A detailed description of
        # required fields should be provided by the payment provider.

        start_param=start_param,
        # Unique deep-linking parameter. May also be used in UpdateBotPrecheckoutQuery
        # see: https://core.telegram.org/bots#deep-linking
        # it may be the empty string if not needed

    )


@resender_bot.on(events.NewMessage(pattern='/subscribe'))
async def start_handler(event: events.NewMessage.Event):
    await resender_bot.send_message(
        event.chat_id, 'Подписка на 30 дней',
        file=generate_invoice(
            price_label='Оплатить', price_amount=ONE_MONTH_PRICE*100, currency=CURRENCY, title='Один месяц подписки', description='Один месяц подписки на рассылку новостей с каналов /sources',
            payload='one_month', start_param=''
        )
    )
    # price_label - надпись на кнопке для оплаты
    # price_amount - цена продукта. Умножаем на 100, т.к. price_amount=10000 означает 100.00 rub/usd etc
    # currency - валюта
    # title - название продукта
    # description - описание продукта
    # payload - грубо говоря id продукта, с которым мы будем работать
    # start_param - хз, не обязательно использовать

# https://habr.com/ru/articles/558924/
