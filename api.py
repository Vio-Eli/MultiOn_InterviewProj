import io

import requests
from PIL import Image

from models.clip import verify_image_similarity, get_image_embedding, clip_processor
from models.llava import get_user_intent, describe_object
from models.multion import search_multion
from models.rcnn import weights, detect_objects
from utils import encode_image_to_base64, crop_object


def upload_image(image_path, image_name):
    url = "https://api.imgur.com/3/image"

    payload = {'type': 'image',
               'title': 'Simple upload',
               'description': 'This is a simple image upload in Imgur'}
    files = [
        ('image', (image_name, image_path, 'image/jpeg'))
    ]
    headers = {
        'Authorization': 'Client-ID {{clientId}}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    return response.json()['data']['link']


def feedback_loop(cropped_image, initial_results, feature_extractor, preprocess, max_retries=3):
    best_match = verify_image_similarity(cropped_image, initial_results)
    retries = 0
    print(f"Feedback (#{retries}: {best_match}")
    while best_match is None and retries < max_retries:
        retries += 1
        new_results = search_multion(describe_object(cropped_image))
        best_match = verify_image_similarity(cropped_image, new_results)
    return best_match


def process_query(query, image):
    if image:
        image_pil = Image.open(io.BytesIO(image))
        image_open = image.read()
    else:
        image_pil = None
        image_open = None

        upload_image(image_open, "some_name.jpg")

    print(f"Query: {query}")

    # Deciphering user intent
    json_output = get_user_intent(query, image_open)

    # Object Detection
    image, predictions = detect_objects(image_pil)
    predicted_boxes = predictions['boxes']
    predicted_labels = predictions['labels']
    decoded_labels = [weights.meta["categories"][label] for label in predicted_labels]
    predicted_scores = predictions['scores']

    # Processing the user intent
    user_intent = json_output['user_intent']['action']
    items = json_output['items']

    best_matches = []

    if user_intent == "buy":
        for item in items:
            print(f"Processing item: {item['name']}")

            # Find the corresponding box for the item
            item_box = None
            for box, label in zip(predicted_boxes, decoded_labels):
                if item['name'].lower() in label.lower():
                    item_box = box
                    break

            if item_box is not None:
                cropped_image = crop_object(image, item_box)
                description = describe_object(cropped_image)
                search_results = search_multion(description, cropped_image)


                search_res_imgs = [result.replace('(', '').replace(')', '').replace('\n', '')[1] for result in search_results.message.split(',') if result]

                if search_results:
                    best_match = feedback_loop(cropped_image, search_res_imgs, get_image_embedding, clip_processor)
                    if best_match:
                        print(f"Best match for {item['name']}: {best_match['link']}")
                        best_matches.append((item['name'], best_match))
                    else:
                        print(f"No suitable match found for {item['name']}")
                        best_matches.append((item['name'], 'No suitable match found'))
                else:
                    print(f"No search results found for {item['name']}")
                    best_matches.append((item['name'], 'No search results found'))
            else:
                print(f"No object found for {item['name']}")
                best_matches.append((item['name'], 'No object found'))

    return best_matches

