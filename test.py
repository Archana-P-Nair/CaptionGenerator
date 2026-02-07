from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.applications.xception import Xception
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Input, Dense, LSTM, Embedding, Dropout, add
from pickle import load
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import argparse
import os
import tensorflow as tf

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image Path")
ap.add_argument('-m', '--model', type=int, default=9,
                help="Model number to use (0-9, default: 9 - last model)")
args = vars(ap.parse_args())
img_path = args['image']
model_num = args['model']


def extract_features(filename, model):
    try:
        print(f"Opening image: {filename}")
        if not os.path.exists(filename):
            print(f"ERROR: File does not exist: {filename}")
            # Try to find the image in the Flicker8k_Dataset folder
            alt_path = os.path.join("Flicker8k_Dataset", os.path.basename(filename))
            if os.path.exists(alt_path):
                print(f"Found image at: {alt_path}")
                filename = alt_path
            else:
                # List available images
                print("\nAvailable images in Flicker8k_Dataset:")
                if os.path.exists("Flicker8k_Dataset"):
                    images = os.listdir("Flicker8k_Dataset")[:10]
                    for img in images:
                        print(f"  - {img}")
                return None

        image = Image.open(filename)
        print(f"Image opened successfully. Size: {image.size}, Mode: {image.mode}")

    except Exception as e:
        print(f"ERROR opening image: {e}")
        return None

    try:
        image = image.resize((299, 299))
        image = np.array(image)
        print(f"Image converted to array. Shape: {image.shape}")

        # Convert RGBA to RGB if needed
        if len(image.shape) == 3 and image.shape[2] == 4:
            print("Converting RGBA to RGB...")
            image = image[..., :3]

        image = np.expand_dims(image, axis=0)
        image = image / 127.5
        image = image - 1.0
        print("Extracting features...")
        feature = model.predict(image, verbose=0)
        print(f"Features extracted. Shape: {feature.shape}")
        return feature
    except Exception as e:
        print(f"ERROR processing image: {e}")
        return None


def word_for_id(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None


def generate_desc(model, tokenizer, photo, max_length):
    in_text = 'start'
    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        pred = model.predict([photo, sequence], verbose=0)
        pred = np.argmax(pred)
        word = word_for_id(pred, tokenizer)
        if word is None:
            break
        in_text += ' ' + word
        if word == 'end':
            break
    return in_text


def define_model(vocab_size, max_length):
    """Define the exact same model architecture as in training"""
    # NOTE: max_length should be 34, not 32
    max_length = 34  # Fixed based on your training output

    # features from the CNN model squeezed from 2048 to 256 nodes
    inputs1 = Input(shape=(2048,), name='input_1')
    fe1 = Dropout(0.5)(inputs1)
    fe2 = Dense(256, activation='relu')(fe1)

    # LSTM sequence model
    inputs2 = Input(shape=(max_length,), name='input_2')
    se1 = Embedding(vocab_size, 256, mask_zero=True)(inputs2)
    se2 = Dropout(0.5)(se1)
    se3 = LSTM(256)(se2)

    # Merging both models
    decoder1 = add([fe2, se3])
    decoder2 = Dense(256, activation='relu')(decoder1)
    outputs = Dense(vocab_size, activation='softmax')(decoder2)

    # tie it together [image, seq] [word]
    model = Model(inputs=[inputs1, inputs2], outputs=outputs)
    model.compile(loss='categorical_crossentropy', optimizer='adam')

    return model


# Load tokenizer and set parameters
print("Loading tokenizer...")
tokenizer = load(open("tokenizer.p", "rb"))
vocab_size = len(tokenizer.word_index) + 1
max_length = 34  # From your training output

# Define and load model
print(f"Loading model_{model_num}.h5...")
model_path = f"models/model_{model_num}.h5"

if not os.path.exists(model_path):
    print(f"ERROR: Model file {model_path} not found!")
    print("Available models:")
    for i in range(10):
        if os.path.exists(f"models/model_{i}.h5"):
            print(f"  model_{i}.h5")
    exit(1)

# Define the model architecture first
print("Defining model architecture...")
model = define_model(vocab_size, max_length)

# Load the weights
try:
    model.load_weights(model_path)
    print(f"✓ Successfully loaded weights from model_{model_num}.h5")
except Exception as e:
    print(f"ERROR loading weights: {e}")
    # Try alternative: load the full model without custom objects
    try:
        model = load_model(model_path, compile=False)
        print(f"✓ Loaded model without compilation")
    except Exception as e2:
        print(f"ERROR: {e2}")
        exit(1)

# Load Xception for feature extraction
print("\nLoading Xception model for feature extraction...")
xception_model = Xception(include_top=False, pooling="avg")

# Process image - fix the path
print(f"\nProcessing image...")
# Check if path needs adjustment
if not os.path.exists(img_path):
    # Try to find the image
    possible_paths = [
        img_path,
        os.path.join("Flicker8k_Dataset", os.path.basename(img_path)),
        os.path.join("Flickr8k_Dataset", "Flicker8k_Dataset", os.path.basename(img_path)),
        os.path.basename(img_path)  # Just the filename
    ]

    for path in possible_paths:
        if os.path.exists(path):
            img_path = path
            print(f"Found image at: {img_path}")
            break
    else:
        print(f"ERROR: Could not find image. Tried:")
        for path in possible_paths:
            print(f"  - {path}")
        exit(1)

photo = extract_features(img_path, xception_model)

if photo is not None:
    # Generate description
    print("\nGenerating caption...")
    description = generate_desc(model, tokenizer, photo, max_length)

    # Clean up the description
    description = description.replace('start ', '').replace(' end', '')

    print("\n" + "=" * 60)
    print(f"📸 IMAGE: {os.path.basename(img_path)}")
    print(f"🤖 MODEL: model_{model_num}.h5")
    print(f"💬 CAPTION: {description}")
    print("=" * 60)

    # Show image
    img = Image.open(img_path)
    plt.figure(figsize=(10, 8))
    plt.imshow(img)
    plt.title(f"Caption: {description}\n(Model: model_{model_num}.h5)", fontsize=12)
    plt.axis('off')
    plt.tight_layout()
    plt.show()
else:
    print("Failed to process image")