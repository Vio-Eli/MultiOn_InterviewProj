import json
import replicate


def get_user_intent(query, image):

    json_output = {
        'user_intent': {
            'action': "What the user wants to do. One word. (enum: 'buy', 'sell')",
        },
        'items': [
            {
                'name': 'Name of the item',
                'type': "Type of the item (enum: 'furniture', 'clothing', 'electronics', 'food', 'other')",
                'description': 'Extremely detailed description of the item. DO NOT relate the description to other objects.',
                'bounding_box': '(x1, y1, height, width)',
            },
            {
                'name': 'Name of the second item... and so on'
            },
        ],
    }

    input = {
        "image": image,
        "prompt": f"Please interpret the query to determine the users intent. Then, use the image to further determine what the user wants. If there is no image, then output solely based on the given text input. If the user is specific (asking for all items in the image is specific) or there is only one item in the image, please give as much separate detail about each item as possible. DO NOT include any other commentary. Please format your response in a json format: {json.dumps(json_output)}. Query: {query}",
    }

    output = replicate.run(
        "yorickvp/llava-v1.6-34b:41ecfbfb261e6c1adf3ad896c9066ca98346996d7c4045c5bc944a79d430f174",
        # "yorickvp/llava-13b:b5f6212d032508382d61ff00469ddda3e32fd8a0e75dc39d8a4191bb742157fb",
        input=input
    )
    output = "".join(output)
    # convert the output to a json object
    json_output = json.loads(output.strip().replace('\n', '').replace('`', '').replace('json{', '{'))
    return json_output


# Function to describe the object using LLaVA
# I wanted to use gpt, but I forgot that Images was deprecated
def describe_object(image_open):
    input = {
        "image": image_open.read(),
        "prompt": "Please describe the object in the image in as much detail as possible. DO NOT include any other commentary.",
    }

    output = replicate.run(
        "yorickvp/llava-v1.6-34b:41ecfbfb261e6c1adf3ad896c9066ca98346996d7c4045c5bc944a79d430f174",
        # "yorickvp/llava-v1.6-vicuna-13b:0603dec596080fa084e26f0ae6d605fc5788ed2b1a0358cd25010619487eae63",
        input=input
    )
    output = "".join(output)
    return str(output)