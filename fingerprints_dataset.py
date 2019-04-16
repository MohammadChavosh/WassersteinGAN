import os
import numpy as np
from PIL import Image

import torch
import torch.utils.data as data


def rgb_preproc(img):
    img = (2. * img[:, :, :3] / 255. - 1).astype(np.float32)
    return img


def numpy2tensor(x):
    if x.ndim == 3:
        x = np.transpose(x, (2, 0, 1))
    elif x.ndim == 4:
        x = np.transpose(x, (3, 0, 1, 2))
    return torch.from_numpy(x)


def tensor2numpy(x):
    return x.data.numpy()


def pil2numpy(x):
    return np.array(x).astype(np.float32)


def numpy2pil(x):
    mode = 'RGB' if x.ndim == 3 else 'L'
    return Image.fromarray(x, mode=mode)


def pil_loader(path):
    return Image.open(path)


class FingerprintsDataset(data.Dataset):
    def __init__(self, images, transforms):
        self.images = images
        self.transforms = transforms

    def __getitem__(self, index):
        img = pil_loader(self.images[index])
        img = self.transforms(img)
        # img = rgb_preproc(pil2numpy(img))
        # img = numpy2tensor(img)

        return img

    def __len__(self):
        return len(self.images)


def get_dataset(base_path, transforms):
    images = []
    for f in os.listdir(base_path):
        vol_path = os.path.join(base_path, f, 'sd09', f)
        for person_folder in os.listdir(vol_path):
            for i in range(1, 11):
                images.append(os.path.join(vol_path, person_folder, '{}_{:02d}.png'.format(person_folder, i)))

    dataset = FingerprintsDataset(images, transforms)
    return dataset
