import os
import logging
from transformers import pipeline, AutoProcessor
from PIL import Image

# Set up verbose logging
logging.basicConfig(level=logging.INFO)

# Define the model ID and load the pipeline and processor
model_id = "llava-hf/llava-1.5-13b-hf"
logging.info(f"Loading model {model_id}")
pipe = pipeline("image-to-text", model=model_id)
processor = AutoProcessor.from_pretrained(model_id)

# Define the image directory and the output directory
image_dir = './civitai_images'
output_dir = './civitai_images_descriptions'
os.makedirs(output_dir, exist_ok=True)

# Get a list of image files in the directory
image_files = [
    f for f in os.listdir(image_dir)
    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))
]

# Process each image
for image_file in image_files:
    image_path = os.path.join(image_dir, image_file)
    logging.info(f"Processing image {image_path}")
    image = Image.open(image_path)

    # Create a conversation prompt
    conversation = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Please describe this image in detail."},
                {"type": "image"},
            ],
        },
    ]
    prompt = processor.apply_chat_template(
        conversation, add_generation_prompt=True)
    logging.info(f"Generated prompt: {prompt}")

    # Generate the description using the pipeline
    outputs = pipe(image, prompt=prompt, generate_kwargs={
                   "max_new_tokens": 300})
    logging.info(f"Pipeline outputs: {outputs}")

    # Extract the generated text
    if isinstance(outputs, list):
        outputs = outputs[0]
    generated_text = outputs.get("generated_text", "")

    # Save the description to a text file with the same base name
    base_name = os.path.splitext(image_file)[0]
    output_file = os.path.join(output_dir, f"{base_name}.txt")
    with open(output_file, 'w') as f:
        f.write(generated_text.strip())
    logging.info(f"Saved description to {output_file}")
