import os
from transformers import pipeline, AutoProcessor, AutoModelForPreTraining
from PIL import Image

# Load model directly
processor = AutoProcessor.from_pretrained("llava-hf/llava-1.5-13b-hf")
model = AutoModelForPreTraining.from_pretrained("llava-hf/llava-1.5-13b-hf")

# Initialize the image-to-text pipeline
model_id = "llava-hf/llava-1.5-13b-hf"
pipe = pipeline("image-to-text", model=model_id)

# Path to the directory containing images
image_dir = './civitai_images'

# Ensure the directory exists
if not os.path.exists(image_dir):
    raise ValueError(f"Directory {image_dir} does not exist")

# Loop through each image in the directory
for image_file in os.listdir(image_dir):
    if image_file.endswith(('.png', '.jpg', '.jpeg')):  # Add more extensions if needed
        # Load the image
        image_path = os.path.join(image_dir, image_file)
        image = Image.open(image_path)

        # Define a basic conversation template with a prompt
        conversation = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image in detail."},
                    {"type": "image"},
                ],
            },
        ]

        # Generate the prompt using the pipeline
        # Or use any custom prompt here
        prompt = {"text": "Describe this image in detail."}

        # Get the model output
        outputs = pipe(image, prompt=prompt, generate_kwargs={
                       "max_new_tokens": 200})
        generated_text = outputs[0]['generated_text']

        # Save the generated text to a .txt file with the same name as the image
        output_file = os.path.splitext(image_file)[0] + '.txt'
        output_path = os.path.join(image_dir, output_file)
        with open(output_path, 'w') as f:
            f.write(generated_text)

        print(f"Generated prompt for {image_file} saved as {output_file}")
