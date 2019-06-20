import subprocess
import os

from fingerprints_dataset import get_fingerprint_images_list


def get_generated_images_list(base_path):
    images = []
    for f in os.listdir(base_path):
        images.append(os.path.join(base_path, f))
    return images


dataset_id = 1
bashCommand = "/home/chavosh/NBIS/bin/mindtct {} /home/chavosh/extracted_minutiaes/{}/{}"
# images = get_fingerprint_images_list('/home/sadegh/Fingerprint_files/sd09/', load_cropped=True)
images = get_generated_images_list('/home/chavosh/sr_path/results/RRDB_PSNR_x4/{}'.format(dataset_id))
for idx, image in enumerate(images):
    # if not image.endswith('_cropped.png'):
    #     print(image)
    #     continue
    process = subprocess.Popen(bashCommand.format(image, dataset_id, image.split('/')[-1][:-4]).split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if idx % 1000 == 0:
        print("{}/{} processed".format(idx + 1, len(images)))
