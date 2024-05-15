# from django.shortcuts import render
# from django.conf import settings
# from django.core.files.storage import FileSystemStorage
# from rembg import remove
# from PIL import Image
# import io

# def remove_background(request):
#     if request.method == 'POST' and request.FILES['image']:
#         uploaded_image = request.FILES['image']

#         # Save the uploaded image to a temporary file
#         fs = FileSystemStorage()
#         filename = fs.save(uploaded_image.name, uploaded_image)
#         input_image_path = fs.path(filename)

#         # Open the uploaded image
#         with Image.open(input_image_path) as image:
#             # Remove the background
#             output_image = remove(image)

#             # Save the processed image to a temporary file
#             output_io = io.BytesIO()
#             output_image.save(output_io, format='PNG')
#             output_io.seek(0)

#             # Create a URL for the processed image
#             output_url = fs.url(fs.save(f"{uploaded_image.name}_nobg.png", output_io))

#         # Remove the temporary files
#         fs.delete(filename)
#         fs.delete(f"{uploaded_image.name}_nobg.png")

#         return render(request, 'result.html', {'output_image': output_url})

#     return render(request, 'upload.html')




from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rembg import remove
from PIL import Image
import io
import os

def remove_background(request):
    if request.method == 'POST' and request.FILES['image']:
        uploaded_image = request.FILES['image']

        # Save the uploaded image to a temporary file
        fs = FileSystemStorage()
        filename = fs.save(uploaded_image.name, uploaded_image)
        input_image_path = fs.path(filename)

        # Open the uploaded image
        with Image.open(input_image_path) as image:
            # Remove the background
            output_image = remove(image)

            # Save the processed image to a temporary file
            output_io = io.BytesIO()
            output_image.save(output_io, format='PNG')
            output_io.seek(0)

            # Save the processed image to the media directory
            output_filename = os.path.splitext(filename)[0] + ".png"
            output_image_path = os.path.join(settings.MEDIA_ROOT, output_filename)
            with open(output_image_path, 'wb') as output_file:
                output_file.write(output_io.getvalue())

            # Remove the temporary files
            fs.delete(filename)

            # Serve the file for download
            with open(output_image_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type='image/png')
                response['Content-Disposition'] = f'attachment; filename="{output_filename}"'
                return response

    return render(request, 'upload.html')
