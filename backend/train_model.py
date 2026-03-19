import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam

print("TensorFlow version:", tf.__version__)

# ============================================================
# SETTINGS - Update paths if needed
# ============================================================
TRAIN_DIR   = r'C:\Users\TANISH GOYAL\Desktop\VantageSoilApp\dataset\train'
TEST_DIR    = r'C:\Users\TANISH GOYAL\Desktop\VantageSoilApp\dataset\test'
MODEL_PATH  = 'model/soil_model.h5'
IMG_SIZE    = 224
BATCH_SIZE  = 16  # smaller batch for CPU
EPOCHS      = 20

# ============================================================
# DATA LOADING
# ============================================================
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    brightness_range=[0.7, 1.3],
    fill_mode='nearest'
)

test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=True
)

test_generator = test_datagen.flow_from_directory(
    TEST_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False
)

print("\nClass indices:", train_generator.class_indices)
print("Training samples:", train_generator.samples)
print("Testing samples:", test_generator.samples)

# ============================================================
# BUILD MODEL
# ============================================================
base_model = MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,
    weights='imagenet'
)
base_model.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = BatchNormalization()(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.4)(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.3)(x)
predictions = Dense(train_generator.num_classes, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("\nModel built successfully!")

# ============================================================
# PHASE 1 - Train top layers
# ============================================================
callbacks1 = [
    ModelCheckpoint(MODEL_PATH, monitor='val_accuracy', save_best_only=True, verbose=1),
    EarlyStopping(monitor='val_accuracy', patience=4, restore_best_weights=True, verbose=1)
]

print("\nPhase 1: Training top layers...")
history1 = model.fit(
    train_generator,
    epochs=10,
    validation_data=test_generator,
    callbacks=callbacks1,
    verbose=1
)

print(f"\nPhase 1 best accuracy: {max(history1.history['val_accuracy'])*100:.2f}%")

# ============================================================
# PHASE 2 - Fine tune last 30 layers
# ============================================================
base_model.trainable = True
for layer in base_model.layers[:-30]:
    layer.trainable = False

model.compile(
    optimizer=Adam(learning_rate=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

callbacks2 = [
    ModelCheckpoint(MODEL_PATH, monitor='val_accuracy', save_best_only=True, verbose=1),
    EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True, verbose=1),
    ReduceLROnPlateau(monitor='val_accuracy', factor=0.5, patience=3, verbose=1)
]

print("\nPhase 2: Fine tuning...")
history2 = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=test_generator,
    callbacks=callbacks2,
    verbose=1
)

print(f"\nPhase 2 best accuracy: {max(history2.history['val_accuracy'])*100:.2f}%")

# ============================================================
# FINAL RESULT
# ============================================================
sorted_classes = sorted(train_generator.class_indices, key=train_generator.class_indices.get)
print("\n✅ Model saved at:", MODEL_PATH)
print("\n⚠️  Copy this into your views.py:")
print(f"classes = {sorted_classes}")