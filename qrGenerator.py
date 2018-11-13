import qrcode

def generateQrCode(art_id, weight, pallet_size):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    data = "Art id: " + art_id + " Weight: " + str(weight) + " Pallet_size: " + str(pallet_size)

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image()
    return img