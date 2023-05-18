import numpy as np
import matplotlib.pyplot as plt
#import resample2D
from astropy.io import fits
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from scipy.ndimage import rotate
from scipy.ndimage import zoom

def processcube(data,ID,diskfile=None,mode=None):
    
    

    vmin = 0
    vmax = 1e3

    if ID == 1:
        mind = 0
        mand = 59

    elif ID == 2:
        mind = 60
        mand = 1079

    elif ID == 3:
        mind = 1080
        mand = 2339

    elif ID == 4:
        mind = 2340
        mand = 3601

    elif ID == 5:
        mind = 3602
        mand = 4860

    elif ID == 6:
        mind = 4861
        mand = 4925

    elif ID == 7:
        mind = 4926
        mand = 4985

    elif ID == 8:
        mind = 4986
        mand = 6005

    elif ID == 9:
        mind = 6006
        mand = 7265

    elif ID == 10:
        mind = 7626
        mand = 8525

    elif ID == 11:
        mind = 8526
        mand = 9785

    elif ID == 12:
        mind = 9786
        mand = 9850

    elif ID == 13:
        mind = 9851
        mand = 9910

    elif ID == 14:
        mind = 9911
        mand = 10930

    elif ID == 15:
        mind = 10931
        mand = 12190

    elif ID == 16:
        mind = 12191
        mand = 13450

    elif ID == 17:
        mind = 13451
        mand = 14710

    elif ID == 18:
        mind = 14711
        mand = 14735
        
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
        box = np.zeros([67,67,len(disk[0,0,:])])
        box[int(67/2)-24:int(67/2)+24,int(67/2)-24:int(67/2)+24] = disk
        

        scalar = 1.0#4e13  #threshold 130 (0.09 earlier value)
        
        if ID in [3,5,8,10,15,17]:
            
            rotdisk = rotate(scalar*box,-22,reshape=False)
            rotdisk[rotdisk == np.NaN] = 1e-12
            rotdisk[rotdisk <= 0] = 1e-12
            
            for dlen in range(mand-mind):
                choice = np.random.randint(low=0,high=len(disk)+1)
                data[mind+dlen,:,:] += rotdisk[:,:,choice]

        # Case for -11
        elif ID in [2,4,9,11,14,16]:
            
            for dlen in range(mand-mind):
                choice = np.random.randint(low=0,high=len(disk)+1)
                data[mind+dlen,:,:] += scalar*box[:,:,choice]

        # Case for +11
        # Case for +11
        #if ID in [3,5,8,10,15,17]:
            
            #rotdisk = rotate(scalar*box,+11,reshape=False)
            #rotdisk[rotdisk == np.NaN] = 1e-12
            #rotdisk[rotdisk <= 0] = 1e-12
            
            #for dlen in range(mand-mind):
                #choice = np.random.randint(low=0,high=len(disk)+1)
                #data[mind+dlen,:,:]=0.03*data[mind+dlen,:,:]
                #data[mind+dlen,:,:] += rotdisk[:,:,choice]

        # Case for -11
        #elif ID in [2,4,9,11,14,16]:
            
            #rotdisk = rotate(scalar*box,-11,reshape=False)
            #rotdisk[rotdisk == np.NaN] = 1e-12
            #rotdisk[rotdisk <= 0] = 1e-12
            
            #for dlen in range(mand-mind):
                #choice = np.random.randint(low=0,high=len(disk)+1)
                #data[mind+dlen,:,:]=0.03*data[mind+dlen,:,:]
                #data[mind+dlen,:,:] += rotdisk[:,:,choice]

    if ID in [2,3,4,5,8,9,10,11,14,15,16,17]:

        
            if mode == 'Analog':
            
                data_c = np.sum(data[mind:mand,:,:],axis=0)
                data_c = data_c/(5*5000*(mand-mind))#data[mind:mand]/(1*6000) # photon/pix*sec
                data_c -= np.mean(data_c[0:5,0:5])

            plt.figure()
            plt.title('{} Data'.format(mode))
            plt.imshow(data_c,vmin=vmin)
            plt.colorbar()
            plt.show()

    # Case for Reference
    elif ID in [1,6,7,12,13,18]:
        
        data_c = data[mind:mand]/(60*100)
        data_c -= np.mean(data_c[:,0:5,0:5])

        data_c[data_c <= 0] = 1e-20
        data_c[data_c == np.nan] = 1e-20
        

    return data_c


