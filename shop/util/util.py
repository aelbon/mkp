from django.http import HttpRequest
from django.core.files.uploadedfile import UploadedFile

from PIL import Image

ALLOWED_FORMATS = {'PNG', 'JPEG'}
MAX_FILE_SIZE_MB = 5

def validate_images(request: HttpRequest):
    """
    Validates a list of uploaded image files.
    :param request: Django HttpRequest object containing the uploaded files.
    :return: Tuple with, 
        -valid (bool): True if all images are valid, False otherwise.
        -results (list): A list of dictionaries containing validation results
        The validation results cotnain: "filename", "is_valid", and "error_message"
    """

    results = []
    valid = True

    files = request.FILES.getlist('images')
    if not files:
        return False, ['Images are required!'] # handle case when no images are uploaded

    for file in files:
        result = validate_image_file(file)
        if (result["is_valid"] == False):
            valid = False
            results.append(result["error_message"])

    return valid, results


def validate_image_file(file: UploadedFile):
    """
    Validates an individual uploaded file.
    :param file: Uploaded file object.
    :return: Dict with keys: "filename", "is_valid", and "error_message".
    """
    filename = file.name
    result = {"filename": filename, "is_valid": True, "error_message": None}
    try:
        # Check file size
        file_size_mb = file.file.__sizeof__() / (1024 * 1024)
        if file_size_mb > MAX_FILE_SIZE_MB:
            result["is_valid"] = False
            result["error_message"] = f"File size exceeds {MAX_FILE_SIZE_MB} MB."
            return result

        # Open the image and validate format. Could be optimized
        with Image.open(file.file) as image:
            if image.format not in ALLOWED_FORMATS:
                result["is_valid"] = False
                result["error_message"] = f"{filename} has an invalid image format: {image.format}. Only PNG and JPG are allowed."
        
    except Exception as e:
        # File is not an image
        result["is_valid"] = False
        result["error_message"] = f"Invalid image file: {filename}"

    # reset the file pointer
    file.file.seek(0)

    return result