# General Image-based MultiOn Shopping

## Overview

This project presents an AI agent that can shop for you using images or descriptions of items. By utilizing state-of-the-art models like LLaVA, CLIP, Faster R-CNN, and integrating with the MultiOn API, this tool aims to provide an efficient, generalized shopping assistant. The tool is designed to identify and find the best match for the items you are interested in, and in future iterations, it will expand to include food items.

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Architecture](#architecture)
5. [Future Work](#future-work)
6. [Contributing](#contributing)
7. [License](#license)

## Features

- **Image-based Shopping**: Upload an image of an item, and the AI will find the best match online.
- **Text-based Search**: Describe the item you need, and the AI will find similar products.
- **Multi-model Integration**: Utilizes a combination of LLaVA, CLIP, and Faster R-CNN for comprehensive item identification and comparison.
- **Single Pipeline**: A unified approach that handles multiple item types and actions seamlessly.

## Installation

To use this application, you need to have Python and the necessary packages installed. You can set up the environment by following these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/multion-shopping.git
    cd multion-shopping
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the FastAPI application:
    ```bash
    uvicorn app.main:app --reload
    ```

## Usage

1. **Start the Application**: Open your browser and navigate to `http://127.0.0.1:8000`.
2. **Upload an Image**: Use the provided interface to upload an image of the item you want to search for.
3. **Describe the Item**: State what you would like. Alternatively, you could describe the item you want instead of uploading an image.
4. **View Results**: The application will process the input and display the best-matched items along with their details.

## Architecture

The project integrates several AI models and APIs to create a robust shopping assistant:
- **LLaVA**: Used for understanding and processing natural language inputs.
- **CLIP**: Utilized for matching text descriptions with images, aiding in item recognition.
- **Faster R-CNN**: Applied for object detection within images to identify specific items.
- **MultiOn API**: Facilitates the search and retrieval of items from online sources based on the inputs provided by the other models.

### Workflow

1. **Input Processing**:
   - **Text & Image Input**: Processed using LLaVA to generate a structured query of what the user wants.
   
2. **Object Detection**:
   - **Image Analysis**: Faster R-CNN is used to identify objects within the uploaded image.
   - **Object Extraction**: The identified objects are extracted and used for further processing.
     - **Object Matching**: The extracted objects are matched with those from Step 1.
     - **Object Cropping**: Each object is cropped from the image for better identification.

3. **Image-Searching**:
   - **MultiOn API Integration**: The cropped images are sent to the MultiOn API for item search.
     - **Alternatively**: If text input was provided, the query is sent directly to the MultiOn API.
   - **Feedback Loop**: CLIP is used to provide feedback on the search results and refine the search query.
   - **Result Display**: The best-matched items are displayed to the user for selection.

## Future Work

- **Food Item Search**: Expand the capabilities to include searching for food items and recipes.
- **Enhanced Matching Algorithms**: Improve the matching algorithms to provide more accurate results.
- **Integration with More APIs**: Extend the API integration to include more shopping platforms.
- **User Feedback Loop**: Implement a feedback mechanism to learn from user interactions and improve search accuracy over time.

## Contributing

We welcome contributions to enhance the project. Please fork the repository and submit a pull request with your proposed changes. Ensure that your code is well-documented and adheres to the existing coding standards.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
