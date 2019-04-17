import os
import numpy as np
from PIL import Image
from skimage import exposure

import torch.utils.data as data
from torchvision.transforms.functional import crop as torch_crop


def tensor2numpy(x):
    return x.data.numpy()


def pil2numpy(x):
    return np.array(x).astype(np.float32)


def numpy2pil(x):
    mode = 'RGB' if x.ndim == 3 else 'L'
    return Image.fromarray(x, mode=mode)


# TODO: use grayscale images!
class FingerprintsDataset(data.Dataset):
    def __init__(self, images, transforms):
        self.images = images
        self.transforms = transforms
        self.crop_dict = {}

    def load_and_crop_fingerprint_part(self, path):
        pil_img = Image.open(path)
        if path not in self.crop_dict:
            img = pil2numpy(pil_img)
            img = exposure.equalize_hist(img)
            img[img <= 0.3] = 0
            img[img > 0.3] = 1
            rows, cols = img.shape

            col_sum = np.sum(img, axis=0)
            col_sum[col_sum <= 3 * rows / 4] = 0
            col_sum[col_sum > 3 * rows / 4] = 1
            selected_col_range = None
            start = None
            for col in range(cols):
                if col_sum[col] or (not col_sum[col] and col == cols - 1):
                    if start and (not selected_col_range or col - start > selected_col_range[1]):
                        selected_col_range = (start, col - start)
                    start = None
                    continue
                if not start:
                    start = col

            row_sum = np.sum(img, axis=1)
            row_sum[row_sum <= 3 * cols / 4] = 0
            row_sum[row_sum > 3 * cols / 4] = 1
            selected_row_range = None
            start = None
            for row in range(rows):
                if row_sum[row] or (not row_sum[row] and row == rows - 1):
                    if start and (not selected_row_range or row - start > selected_row_range[1]):
                        selected_row_range = (start, row - start)
                    start = None
                    continue
                if not start:
                    start = row

            self.crop_dict[path] = (selected_row_range, selected_col_range, rows, cols)

        selected_row_range, selected_col_range, rows, cols = self.crop_dict[path]
        if not selected_row_range or not selected_col_range:
            print(path)
        cropped = torch_crop(pil_img, max(selected_row_range[0] - rows / 10, 0),
                             max(selected_col_range[0] - cols / 10, 0),
                             selected_row_range[1] + max(0, min(rows / 5, 11 * rows / 10 - sum(selected_row_range))),
                             selected_col_range[1] + max(0, min(cols / 5, 11 * cols / 10 - sum(selected_col_range))))
        return cropped

    def __getitem__(self, index):
        img = self.load_and_crop_fingerprint_part(self.images[index]).convert("RGB")
        img = self.transforms(img)

        return img, 1  # Random label :D

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
