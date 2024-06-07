# Function to encode the image to base64 for the MultiOn API
def encode_image_to_base64(image):
    # Save the image as cropped_object_1.jpg
    image.save("cropped_object1.jpg")

    # Open it to get the Binary IO
    return open("cropped_object1.jpg", "rb")


# Function to crop an object from the image
def crop_object(image, box):
    return image.crop((int(box[0]), int(box[1]), int(box[2]), int(box[3])))

