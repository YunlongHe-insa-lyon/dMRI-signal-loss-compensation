import os.path
import random
from data.base_dataset import BaseDataset, get_params, get_transform
import torchvision.transforms as transforms
from data.image_folder import make_dataset
#from PIL import Image
from scipy.io import loadmat

class SimRealDeconvDataset(BaseDataset):
    """A dataset class for paired image dataset.

    It assumes that the directory '/path/to/data/train' contains image pairs in the form of {A,B}.
    During test time, you need to prepare a directory '/path/to/data/test'.
    """

    def __init__(self, opt):
        """Initialize this dataset class.

        Parameters:
            opt (Option class) -- stores all the experiment flags; needs to be a subclass of BaseOptions
        """
        BaseDataset.__init__(self, opt)
        self.dir_AB = os.path.join(opt.dataroot, opt.phase)  # get the image directory
        self.AB_paths = sorted(make_dataset(self.dir_AB, opt.max_dataset_size))  # get image paths
        assert(self.opt.load_size >= self.opt.crop_size)   # crop_size should be smaller than the size of loaded image
        self.input_nc = self.opt.output_nc if self.opt.direction == 'BtoA' else self.opt.input_nc
        self.output_nc = self.opt.input_nc if self.opt.direction == 'BtoA' else self.opt.output_nc

    def __getitem__(self, index):
        """Return a data point and its metadata information.

        Parameters:
            index - - a random integer for data indexing

        Returns a dictionary that contains A, B, A_paths and B_paths
            A (tensor) - - an image in the input domain
            B (tensor) - - its corresponding image in the target domain
            A_paths (str) - - image paths
            B_paths (str) - - image paths (same as A_paths)
        """
        # read a image given a random integer index
        AB_path = self.AB_paths[index]
#        AB = Image.open(AB_path).convert('RGB')
        Mu = loadmat(AB_path)
        AB = Mu['Opt_to_Target']
#        print('type of AB %s' % dir(AB))
        w,h,l = AB.shape
#        print('w %d, h %d, l %d' %(w, h, l))
        h2 = int(h / 2)    
#        print('midstep-h2 %d' % h2)
        A = AB[:,:,:self.input_nc] # same dimension setting as in MATLAB, i.e. the 3rd dimension is channels: first 5 bins for Mu_l; the others 50 bins for Mu_h
        B = AB[:,:,self.input_nc:]
        A = A.transpose(2,0,1) # transpose dimension due to the demand of pythorch <batch, channel, W, H>
        B = B.transpose(2,0,1)
#        randomly crop image for train
#        w_offset = random.randint(0, max(0, w - self.opt.fineSize - 1))
#        h_offset = random.randint(0, max(0, h - self.opt.fineSize - 1))
        
        
        
        # split AB image into A and B
#        w, h = AB.size


        
#        A = AB.crop((0, 0, w2, h))
#        B = AB.crop((w2, 0, w, h))


        # apply the same transform to both A and B
#        transform_params = get_params(self.opt, A.shape)
#        A_transform = get_transform(self.opt, transform_params, grayscale=(self.input_nc == 1))
#        B_transform = get_transform(self.opt, transform_params, grayscale=(self.output_nc == 1))
#
#        A = A_transform(A)
#        B = B_transform(B)
        
        return {'A': A, 'B': B, 'A_paths': AB_path, 'B_paths': AB_path}

    def __len__(self):
        """Return the total number of images in the dataset."""
        return len(self.AB_paths)

