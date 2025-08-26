import qrcode


def generate_qr_code():
    qr_codes = {
        "QR1": "https://t.me/karban_assistant_bot?start=bronstain",
        "QR2": "https://t.me/karban_assistant_bot?start=code2",
        "QR3": "https://t.me/karban_assistant_bot?start=code3"
    }

    for name, url in qr_codes.items():
        qr = qrcode.make(url)
        qr.save(f"{name}.png")


def parse_callback(callback: str):
    id = callback.split("_")[1]
    return id if id else None


generate_qr_code()