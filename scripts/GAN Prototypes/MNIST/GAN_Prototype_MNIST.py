from sklearn.model_selection import train_test_split
from models.CGAN_mnist import CGAN
from scripts.Utils.utils import *
from scripts.Utils.data_loading import *
from PytorchDatasets.MNIST_Dataset import MNIST_Dataset
from torch.utils import data
import matplotlib.pyplot as plt
import random

# Set random seem for reproducibility
manualSeed = 999
print("Random Seed: ", manualSeed)
random.seed(manualSeed)
torch.manual_seed(manualSeed)

# Import data
# Desired Train/Validation/Test split
splits = [0.15, 0.05, 0.80]

# Load data and split
mnist = load_dataset('mnist')
x_comb, y_comb = torch.cat((mnist[0].data, mnist[1].data), 0).numpy(), torch.cat((mnist[0].targets, mnist[1].targets), 0).numpy()
x_train, y_train, x_val, y_val, x_test, y_test = train_val_test_split(x_comb, y_comb, splits, manualSeed)

# Print resulting sizes
print("Train:", x_train.shape)
print("Validate: ", x_val.shape)
print("Test: ", x_test.shape)

# Print an example image
print(y_train[0])
plt.imshow(x_train[0], cmap='gray')

# Define parameters
training_params = {'batch_size': 64,
                   'shuffle': True,
                   'num_workers': 6}

CGAN_params = {'device': torch.device("cuda:0" if (torch.cuda.is_available()) else "cpu"),  # GPU if exists, else CPU
               'nz': 64,  # Size of noise vector
               'num_channels': 1,  # Number of channels in image
               'ngf': 32,  # Number of generator feature maps
               'ndf': 32,  # Number of discriminator feature maps
               'x_dim': (x_train.shape[1], x_train.shape[2]),  # Dimensions of input images
               'nc': 10,  # Number of output classes
               'lr': 2e-4,  # Learning rate for adam optimizer
               'beta1': 0.5,  # Beta1 for adam optimizer
               'beta2': 0.999,  # Beta2 for adam optimizer
               'wd': 0}  # Weight decay for network (regularization)

# Define generators
training_set = MNIST_Dataset(x_train, y_train)
training_generator = data.DataLoader(training_set, **training_params)

validation_set = MNIST_Dataset(x_val, y_val)
validation_generator = data.DataLoader(validation_set, **training_params)

test_set = MNIST_Dataset(x_test, y_test)
test_generator = data.DataLoader(test_set, **training_params)

# Define GAN
CGAN = CGAN(training_generator, validation_generator, test_generator, **CGAN_params)

asdf = CGAN.netG(CGAN.netG.fixed_noise, CGAN.netG.fixed_labels)
CGAN.netD(asdf, CGAN.netG.fixed_labels)