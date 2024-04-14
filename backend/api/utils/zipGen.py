import zipfile
from io import BytesIO
import os


# generate the byte zip file from the list of participants
def generateZip(participants):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for participant in participants:
            # imagePaths.append(participant.certificate.path)
            image_name = os.path.basename(participant.certificate.path)
            zip_file.write(participant.certificate.path, image_name)
    zip_buffer.seek(0)
    print(zip_buffer)
    return zip_buffer
