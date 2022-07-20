# import cv2
# import qrcode


# def generate_qrcode(data, file_path):
#     """Generate qr code for data.

#     Parameters
#     ----------
#     data : str
#         data to be encoded in qr code.
#     file_path : str
#         path to file
#     """
#     img = qrcode.make(data)
#     img.save(file_path)


# def read_qrcode(file_path):
#     """read the image and return the data.

#         Parameters
#         ----------
#         file_path : str
#             path to file

#     #     Returns
#     #     -------
#     #     _data: str
#     #         detect the qr code from img and return the data.
#     #"""

#     img = cv2.imread(file_path)
#     detector = cv2.QRCodeDetector()
#     data, bbox, straight_qrcode = detector.detectAndDecode(img)
#     return data
"""file contains utility functions for the project."""


def get_human_readable_date_time(data):
    """Get human readable date time."""
    return data.strftime("%Y-%m-%d %H:%M %p")
