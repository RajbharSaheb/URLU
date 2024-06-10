HELP_BUTTONS =InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Mise", callback_data="mise"),
                        InlineKeyboardButton("imgedit", callback_data="imgeedit"),
                        InlineKeyboardButton("search", callback_data="search"),
                    ],
                    [
                        InlineKeyboardButton("paste", callback_data="paste"),
                        InlineKeyboardButton("extra", callback_data="extra"),
                    ],
                ]
)




async def fetch_proxies(proxy_type):
    url = f"https://www.proxy-list.download/api/v1/get?type={proxy_type}"
    response = requests.get(url)
    if response.status_code == 200:
        proxies = response.text.split("\n")
        proxies.sort()
        formatted_proxies = []
        for i, proxy in enumerate(proxies):
            if proxy.strip():
                formatted_proxies.append(("{}`**").format(proxy))

        if not formatted_proxies:
            formatted_proxies.append(("Nothing found froxy").format(em.gagal))

        return formatted_proxies[:10]
    else:
        return None


async def send_proxy(c: nlx, chat_id, proxy_type, proxies):
    em = Emojik()
    em.initialize()
    if proxies:
        teks = ("Nothing found froxy").format(proxy_type)
        teks += "\n".join(proxies)
        await c.send_message(chat_id, teks)
    else:
        await c.send_message(chat_id, (("There's no Proxy valid.").format(em.gagal)))


@ky.ubot("getproxy", sudo=True)
async def get_proxy_command(c: nlx, m):
    try:
        pros = await m.reply(("Being Processed").format(em.proses))
        command = m.text.split()[1].lower()
        if command not in ["http", "socks4", "socks5"]:
            await c.send_message(
                m.chat.id,
                (("<b>Commands not valid.\nExample commands {} [`http`|`socks4`|`socks5`]</b>").format(em.gagal, m.texy)),
            )
            return

        proxy_type = command
        proxies = await fetch_proxies(proxy_type)
        await send_proxy(c, m.chat.id, proxy_type, proxies)
        await pros.delete()
    except IndexError:
        await c.send_message(
            m.chat.id,
            (("<b>Commands not valid.\nExample commands `{}` [`http`|`socks4`|`socks5`]</b>").format(em.gagal, m.text)),
        )
        await pros.delete()
