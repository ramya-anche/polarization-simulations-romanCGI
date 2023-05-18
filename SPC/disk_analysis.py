import numpy as np
import matplotlib.pyplot as plt
#import resample2D
from astropy.io import fits
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from scipy.ndimage import rotate
from scipy.ndimage import zoom

def spcprocess(data,ID,diskfile=None,mode=None):
    
    

    vmin = 0
    vmax = 1e3

    if ID == 0:
        mind = 0
        mand = 45

    elif ID == 100:
        mind = 45
        mand = 144

    elif ID == 101:
        mind = 144
        mand = 243

    elif ID == 102:
        mind = 243
        mand = 342

    elif ID == 103:
        mind = 342
        mand = 441

    elif ID == 1:
        mind = 441
        mand = 480

    elif ID == 104:
        mind = 480
        mand = 579

    elif ID == 105:
        mind = 579
        mand = 678

    elif ID == 106:
        mind = 678
        mand = 777

    elif ID == 107:
        mind = 777
        mand = 876

    elif ID == 2:
        mind = 876
        mand = 915

    elif ID == 3:
        mind = 915
        mand = 960

    elif ID == 108:
        mind = 960
        mand = 1059

    elif ID == 109:
        mind = 1059
        mand = 1158

    elif ID == 110:
        mind = 1158
        mand = 1257

    elif ID == 111:
        mind = 1257
        mand = 1356

    elif ID == 4:
        mind = 1356
        mand = 1395

    elif ID == 112:
        mind = 1395
        mand = 1494
        
    elif ID == 113:
        mind = 1494
        mand = 1593
     
    elif ID == 114:
        mind = 1593
        mand = 1692
    
    elif ID == 115:
        mind = 1692
        mand = 1791
        
    elif ID == 5:
        mind = 1791
        mand = 1830
        
    x = np.linspace(-1,1,len(data[0,:,:]))
    y = np.linspace(-1,1,len(data[0,:,:]))
    x,y = np.meshgrid(x,y)
    r = np.sqrt(x**2 + y**2)

    maskarray = (r<=0.75) & (r>= 0.2)

    if diskfile is not None:
        # Add debris disks
        disk = fits.getdata(diskfile).astype(float)
        print('disk array shape = ',disk.shape)
    
        
        #Resample the disk to fit the HLC resolution - Noisy
        box = np.zeros([181,181,len(disk[0,0,:])])
        box[int(181/2)-64:int(181/2)+64,int(181/2)-64:int(181/2)+64] = disk
        

        scalar = 1
        
        if ID in [101,103,104,106,109,111,112,114]:
        
            rotdisk = rotate(scalar*box,-26,reshape=False)
            rotdisk[rotdisk == np.NaN] = 1e-12
            rotdisk[rotdisk <= 0] = 1e-12
            
            for dlen in range(mand-mind):
                choice = np.random.randint(low=0,high=49)
                data[mind+dlen,:,:] += rotdisk[:,:,choice]

        # Case for -11
        elif ID in [100,102,105,107,108,110,113,115]:
        
            
            for dlen in range(mand-mind):
                choice = np.random.randint(low=0,high=49)
                data[mind+dlen,:,:] += scalar*box[:,:,choice]


    if ID in [100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115]:

        
            if mode == 'Analog':
            
                data_c = np.sum(data[mind:mand,:,:],axis=0)
                data_c = data_c/(1*5000*(mand-mind))#data[mind:mand]/(1*6000) # photon/pix*sec
                data_c -= np.mean(data_c[0:5,0:5])

            plt.figure()
            plt.title('{} Data'.format(mode))
            plt.imshow(data_c,vmin=vmin)
            plt.colorbar()
            plt.show()

    # Case for Reference
    elif ID in [1,2,3,4,5]:
        
        data_c = data[mind:mand]/(14*100)
        data_c -= np.mean(data_c[:,0:5,0:5])

        data_c[data_c <= 0] = 1e-20
        data_c[data_c == np.nan] = 1e-20
        

    return data_c


