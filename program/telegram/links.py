class tg_links:
    def __init__(self):
        return None

    @staticmethod
    def get_hash(link):
        if link is None:
            return ''
        return (str(link)
                .replace('https://t.me/joinchat', '')
                .replace('https://t.me/', '')
                .replace('+', '')
                .replace('/', '')
                .replace(':', '')
                .replace('@', '')
                .strip())

    @staticmethod
    def _correct(link):
        if link is None:
            return ''
        return str(link).replace('+', 'joinchat/').replace('@', '').strip()

    @staticmethod
    def _correct_private(link):
        if link is None:
            return ''
        link = str(link)
        if 'https://t.me/joinchat' in link:
            return link.replace(' ', '').strip()
        if 'https://t.me/+' in link:
            return link.replace('https://t.me/+', 'https://t.me/joinchat/').strip()
        return link.replace('https://t.me/', '').replace('@', '').strip()

    @staticmethod
    def message_link_id_username(link):
        try:
            data = (str(link)
                    .replace('https://t.me/', '')
                    .replace('http://t.me/', '')
                    .replace('https://telegram.me/', '')
                    .replace('http://telegram.me/', ''))
            parts = [part for part in data.split('/') if part]
            if len(parts) < 2:
                return False
            username = parts[0]
            message_id = int(parts[1])
            group_id = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0
            return {'group_id': group_id, 'username': username, 'mess_id': message_id}
        except Exception as exc:
            print('message_link_id_username: ', exc)
            return False

    @staticmethod
    def get_data(link):
        data = tg_links.message_link_id_username(link)
        return data if data else {}

    @staticmethod
    def standart(link):
        link = str(link).strip().replace('http:', 'https:')
        if 'joinchat' in link or '+' in link:
            return link.replace('https://t.me/+', 'https://t.me/joinchat/')
        if '@' in link:
            return 'https://t.me/' + link.replace('@', '').strip()
        if 'telegram.me' in link:
            return link.replace('telegram.me', 't.me')
        if 't.me' in link:
            return link
        return 'https://t.me/' + link

    @staticmethod
    def phones(phone):
        return ''.join(ch for ch in str(phone) if ch.isdigit())

    @staticmethod
    def contacts_phone_or_username(data):
        text = str(data)
        for item in ('https://t.me/', 'http://t.me/', 'https://telegram.me/', 'http://telegram.me/', '@', '+', '-', '.', ',', '(', ')', '/', ':', ' '):
            text = text.replace(item, '')
        if text.isdigit():
            return {'phone': int(text), 'username': None}
        return {'phone': None, 'username': text}

    @staticmethod
    def clear_username(username):
        return str(username).replace('@', '').replace('https://t.me/', '').replace('http://t.me/', '').strip()
