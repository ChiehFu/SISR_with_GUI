# CSCE636 Project

## Dependencies 
* Python 3.6
* PyTorch >= 1.0.0
* numpy
* skimage
* imageio
* matplotlib
* tqdm
* Tkinter
* Pillow

## GUI Demo
* Navigate to the project main directory ```<YOUR PROJECT FOLDER>```
* Run the script ```python demo.py```, and the main interface will show up.
* Click ```Open``` to upload the target image (there are some photos in the folder ```/testphotos/```).
* Select the desired scaling up factor(x2/x3/x4) to scale up.
* Click Upscale, after the process, a window pops up, choose the location to save the result image.
* The result image will show up after saving.

## Train / Test the model
### Dataset 
* Download the [DIV2K](https://drive.google.com/file/d/113H4VkUjtI5Cv9ZiFy3blnOEFqrEf7hD/view?usp=sharing) dataset, unzip it under the directory ```./EDSR/dataset```
* The directory structure should look like :
```
EDSR
    |-dataset
            |-DIV2K
```
### Train / Test
* Navigate to the directory ```/EDSR/src/```
* Run the scripts below:
```
# Test:
# Test the baseline model EDSR
python main.py --model edsr --scale 2 --n_resblocks 16 --test_only --dir_data ../dataset --pre_train ../models/edsr_x2.pt

# Test the model EDSR_ATT
python main.py --model edsr_att --scale 2 --n_resblocks 6 --n_resgroups 4 --test_only --dir_data ../dataset --pre_train ../models/edsr_att_x2.pt

# Test the model EDSR_ATT with self_ensemble
python main.py --model edsr_att --scale 2 --n_resblocks 6 --n_resgroups 4 --test_only --dir_data ../dataset --pre_train ../models/edsr_att_x2.pt --self_ensemble

# Train:
# Train the baseline model EDSRpython main.py --model edsr --scale 2 --n_resblocks 16 --dir_data ../dataset
python main.py --model edsr --scale 2 --n_resblocks 16 --dir_data ../dataset

# Train the model EDSR_ATT
python main.py --model edsr_att --scale 2 --n_resblocks 6 --n_resgroups 4 --dir_data ../dataset
```


## Reference
* [Image Super-Resolution Using Very Deep
Residual Channel Attention Networks - EDSR](https://github.com/thstkdgus35/EDSR-PyTorch)
* [Enhanced Deep Residual Networks for Single Image Super-Resolution - RCAN](https://github.com/yulunzhang/RCAN)
