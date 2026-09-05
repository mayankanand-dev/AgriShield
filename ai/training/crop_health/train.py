
"""
Crop Health Model Training — EfficientNet-B0 Transfer Learning
=============================================================
Usage:
    cd e:/VS code/AgriShield/ai
    python -m training.crop_health.train

Expects PlantVillage dataset at:
    ai/data/crop_health/PlantVillage/<ClassName>/image.jpg

Saves trained model to:
    ai/models/crop_health/model.pt
    ai/models/crop_health/class_names.json
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, models, transforms

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR    = Path(__file__).resolve().parents[2]           # ai/
DATA_DIR    = BASE_DIR / "data" / "crop_health" / "PlantVillage"
MODEL_DIR   = BASE_DIR / "models" / "crop_health"
MODEL_PATH  = MODEL_DIR / "model.pt"
LABELS_PATH = MODEL_DIR / "class_names.json"

MODEL_DIR.mkdir(parents=True, exist_ok=True)

# ── Hyper-parameters ──────────────────────────────────────────────────────────
IMG_SIZE   = 224
BATCH_SIZE = 32
EPOCHS     = 10
LR         = 1e-4
VAL_SPLIT  = 0.15
DEVICE     = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def get_transforms():
    train_tf = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    val_tf = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    return train_tf, val_tf


def build_model(num_classes: int) -> nn.Module:
    """Load pre-trained EfficientNet-B0, replace final classifier head."""
    model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.IMAGENET1K_V1)
    # Freeze all backbone layers
    for param in model.parameters():
        param.requires_grad = False
    # Replace classifier: only this head gets trained in the first pass
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, num_classes)
    return model.to(DEVICE)


def train_one_epoch(model, loader, criterion, optimizer):
    model.train()
    total_loss, correct, total = 0.0, 0, 0
    for imgs, labels in loader:
        imgs, labels = imgs.to(DEVICE), labels.to(DEVICE)
        optimizer.zero_grad()
        outputs = model(imgs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * imgs.size(0)
        _, preds = outputs.max(1)
        correct += preds.eq(labels).sum().item()
        total += imgs.size(0)
    return total_loss / total, correct / total


@torch.no_grad()
def validate(model, loader, criterion):
    model.eval()
    total_loss, correct, total = 0.0, 0, 0
    for imgs, labels in loader:
        imgs, labels = imgs.to(DEVICE), labels.to(DEVICE)
        outputs = model(imgs)
        loss = criterion(outputs, labels)
        total_loss += loss.item() * imgs.size(0)
        _, preds = outputs.max(1)
        correct += preds.eq(labels).sum().item()
        total += imgs.size(0)
    return total_loss / total, correct / total


def main():
    print(f"[INFO] Using device: {DEVICE}")
    print(f"[INFO] Loading dataset from: {DATA_DIR}")

    if not DATA_DIR.exists():
        raise FileNotFoundError(
            f"Dataset not found at {DATA_DIR}\n"
            "Please place the PlantVillage dataset at ai/data/crop_health/PlantVillage/"
        )

    train_tf, val_tf = get_transforms()

    # Load full dataset with train transforms first (we'll reassign val subset below)
    full_dataset = datasets.ImageFolder(str(DATA_DIR), transform=train_tf)
    class_names  = full_dataset.classes
    num_classes  = len(class_names)

    print(f"[INFO] Found {num_classes} classes: {class_names}")
    print(f"[INFO] Total images: {len(full_dataset)}")

    # Train / val split
    val_size   = int(len(full_dataset) * VAL_SPLIT)
    train_size = len(full_dataset) - val_size
    train_ds, val_ds = random_split(full_dataset, [train_size, val_size])

    # Apply val transform to the val subset
    val_ds.dataset = datasets.ImageFolder(str(DATA_DIR), transform=val_tf)

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True,  num_workers=0)
    val_loader   = DataLoader(val_ds,   batch_size=BATCH_SIZE, shuffle=False, num_workers=0)

    model     = build_model(num_classes)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.classifier.parameters(), lr=LR)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=4, gamma=0.5)

    best_val_acc = 0.0
    print(f"\n[INFO] Starting training for {EPOCHS} epochs...\n")

    for epoch in range(1, EPOCHS + 1):
        t0 = time.time()
        tr_loss, tr_acc = train_one_epoch(model, train_loader, criterion, optimizer)
        vl_loss, vl_acc = validate(model, val_loader, criterion)
        scheduler.step()
        elapsed = time.time() - t0

        print(
            f"Epoch {epoch:02d}/{EPOCHS}  "
            f"Train Loss: {tr_loss:.4f}  Train Acc: {tr_acc:.4f}  "
            f"Val Loss: {vl_loss:.4f}  Val Acc: {vl_acc:.4f}  "
            f"({elapsed:.1f}s)"
        )

        if vl_acc > best_val_acc:
            best_val_acc = vl_acc
            torch.save(model.state_dict(), MODEL_PATH)
            print(f"  ✅ Saved best model (val_acc={best_val_acc:.4f}) → {MODEL_PATH}")

    # Save class labels so the inference pipeline can decode outputs
    with open(LABELS_PATH, "w") as f:
        json.dump(class_names, f, indent=2)
    print(f"\n[INFO] Class labels saved → {LABELS_PATH}")
    print(f"[DONE] Best validation accuracy: {best_val_acc:.4f}")


if __name__ == "__main__":
    main()