import os


def search_multion(multion, description, image_url=None):
    # Use MultiOn API to search for the object

    if image_url:
        url = "https://images.google.com/"
        cmd = f"Go to this url: https://images.google.com/. Click on the search by image button. In the paste image link here box, input the url: {image_url}. Please find the best matching image url and site url based on the initial given image (left half of the page when you load the results. DO NOT OUTPUT THE GIVEN URL) and it's price. Output a SINGLE tuple (url, image_url) and no other text or commentary. If at any time you are redirected to the main google search page, please restart the process. DO NOT PASTE THE URL INTO THE SEARCH BAR."
    else:
        url = "https://www.google.com/"
        cmd = f"Please find the best matching image url and site url based on the following description and it's price. Output a SINGLE tuple (url, image_url) and no other text or commentary. Description: {description}"

    response = multion.browse(
        cmd=cmd,
        url=url,
        local=True,
    )
    return response
