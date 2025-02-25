from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import torch.optim as optim
import torch
from torchvision import models
import torch.optim as optim
import os
from tqdm import tqdm

dataset_path = r"/Users/matijasukovic/Documents/dataset_oil_estimation"

# Define transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Load datasets
train_dataset = datasets.ImageFolder(os.path.join(dataset_path, 'train'), transform=transform)
val_dataset = datasets.ImageFolder(os.path.join(dataset_path, 'val'), transform=transform)

# Create data loaders
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

# Load pre-trained ResNet-50 model
model = models.resnet50(pretrained=True)

# Freeze early layers (optional)
for param in model.parameters():
    param.requires_grad = False

# Modify the final fully connected layer
num_classes = len(train_dataset.classes)
model.fc = torch.nn.Linear(model.fc.in_features, num_classes)

criterion = torch.nn.CrossEntropyLoss()
optimizer = optim.Adam(model.fc.parameters(), lr=0.001)

if torch.backends.mps.is_available():
    device = torch.device("mps")
    print('metal')
elif torch.cuda.is_available():
    device = torch.device("cuda")
    print('cuda')
else:
    device = torch.device("cpu")
    print('cpu')

model.to(device)

num_epochs = 10

for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    
    progress_bar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{num_epochs}")
    
    for inputs, labels in progress_bar:
        inputs, labels = inputs.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        progress_bar.set_postfix(loss=loss.item())
    
    print(f"Epoch [{epoch+1}/{num_epochs}] Completed, Avg Loss: {running_loss / len(train_loader):.4f}")


model.eval()
correct = 0
total = 0
with torch.no_grad():
    for inputs, labels in val_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        outputs = model(inputs)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print(f'Validation Accuracy: {100 * correct / total:.2f}%')