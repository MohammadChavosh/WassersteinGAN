import subprocess

from fingerprints_dataset import get_fingerprint_images_list


bashCommand = "/home/chavosh/NBIS/bin/mindtct {} /home/chavosh/NBIS_out/{}"
images = get_fingerprint_images_list('/home/sadegh/Fingerprint_files/sd09/', load_cropped=True)
for idx, image in enumerate(images):
    if not image.endswith('_cropped.png'):
        print(image)
        continue
    process = subprocess.Popen(bashCommand.format(image, image.split('/')[-1][:-4]).split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if idx % 1000 == 0:
        print("{}/{} processed".format(idx + 1, len(images)))
