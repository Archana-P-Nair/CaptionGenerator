"""
Image captioning service: loads model/tokenizer and generates captions.
Paths are relative to project root (parent of backend/).
"""
import io
import os
from pickle import load
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.applications.xception import Xception
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Input, Dense, LSTM, Embedding, Dropout, add

# Project root (parent of backend/)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_NUM = 9
MAX_LENGTH = 34

_tokenizer = None
_model = None
_xception = None


def _word_for_id(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None


def _generate_desc(model, tokenizer, photo, max_len):
    in_text = "start"
    for _ in range(max_len):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_len)
        pred = model.predict([photo, sequence], verbose=0)
        pred = np.argmax(pred)
        word = _word_for_id(pred, tokenizer)
        if word is None:
            break
        in_text += " " + word
        if word == "end":
            break
    return in_text


def _define_model(vocab_size, max_len):
    max_len = 34
    inputs1 = Input(shape=(2048,), name="input_1")
    fe1 = Dropout(0.5)(inputs1)
    fe2 = Dense(256, activation="relu")(fe1)
    inputs2 = Input(shape=(max_len,), name="input_2")
    se1 = Embedding(vocab_size, 256, mask_zero=True)(inputs2)
    se2 = Dropout(0.5)(se1)
    se3 = LSTM(256)(se2)
    decoder1 = add([fe2, se3])
    decoder2 = Dense(256, activation="relu")(decoder1)
    outputs = Dense(vocab_size, activation="softmax")(decoder2)
    model = Model(inputs=[inputs1, inputs2], outputs=outputs)
    model.compile(loss="categorical_crossentropy", optimizer="adam")
    return model


def _load_models():
    global _tokenizer, _model, _xception
    if _model is not None:
        return

    tokenizer_path = os.path.join(ROOT, "tokenizer.p")
    model_path = os.path.join(ROOT, "models", f"model_{MODEL_NUM}.h5")

    if not os.path.exists(tokenizer_path):
        raise FileNotFoundError(f"Tokenizer not found: {tokenizer_path}")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found: {model_path}")

    _tokenizer = load(open(tokenizer_path, "rb"))
    vocab_size = len(_tokenizer.word_index) + 1
    _model = _define_model(vocab_size, MAX_LENGTH)
    _model.load_weights(model_path)
    _xception = Xception(include_top=False, pooling="avg")


def extract_features(image_bytes: bytes):
    """Load image from bytes, resize, normalize, extract Xception features."""
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((299, 299))
    image = np.array(image)
    image = np.expand_dims(image, axis=0)
    image = image / 127.5
    image = image - 1.0
    feature = _xception.predict(image, verbose=0)
    return feature


def generate_caption(image_bytes: bytes) -> str:
    """Generate caption for image bytes. Loads model on first call."""
    _load_models()
    photo = extract_features(image_bytes)
    description = _generate_desc(_model, _tokenizer, photo, MAX_LENGTH)
    description = description.replace("start ", "").replace(" end", "").strip()
    return description or "No caption generated"
