#########################################################################
#                                                                       #
# Script that copies a zipped raspbian image to a sd card.              #
# First parameter should be the path of the zipped image                #
# Second parameter should be the device the image should be written on. #
#                                                                       #
# Author: Jan Wennrich (PCSG)                                           #
#                                                                       #
#########################################################################


# Device to copy the image to
DEVICE=$1

# The zipped image file
IMAGE_ZIP=$2

# Assumed location of the created boot partition
BOOT_PATH="/media/$USER/boot"


# Check if first parameter for the device was given
if [ -z "$DEVICE" ]; then
    echo "Please specify a device the image should be copied to, as the second argument."
    exit 1
fi

echo "Asking for sudo permissions to check if the device exists:"

# Check if the device exists
if sudo test ! -b $DEVICE; then
    echo "Selected device \"\033[0;32m$DEVICE\033[0m\" could not be found, aborting! (List your devices using \"fdisk -l\")"
    exit 1
fi

echo "Selected device: \"\033[0;32m$DEVICE\033[0m\""


# Check if second parameter for the zip file was given
if [ -z "$IMAGE_ZIP" ]; then
    # Parameter was not given, downloading latest version...
    IMAGE_ZIP="/tmp/raspian_lite_latest.zip"
    echo "No zip file given, downloading latest Raspbian Strecht Lite image..."
    wget -O $IMAGE_ZIP "https://downloads.raspberrypi.org/raspbian_lite_latest"
fi

# Check if zip file exists
if [ ! -f $IMAGE_ZIP ]; then
    echo "Zipped image \"\033[0;32m$IMAGE_ZIP\033[0m\" could not be found, aborting!"
    exit 1
fi

echo "Selected image: \"\033[0;32m$IMAGE_ZIP\033[0m\""

echo "The selected image will be copied to the selected device."

# Ask if the image should really been written
read -p "Do you really want to copy? (y/n): " CHOICE
case $CHOICE in
    n|N) 
	    echo "Image will not be copied, aborting!"
	    exit 0
	    ;;
    y|Y)
	    echo "Writing image \"\033[0;32m$IMAGE_ZIP\033[0m\" to \"\033[0;32m$DEVICE\033[0m\"..."
	    unzip -p $IMAGE_ZIP | sudo dd of=$DEVICE bs=4M status=progress conv=fsync
	    ;;
esac
    
    
# Check if assumed boot partition is found where expected  
if [ -d $BOOT_PATH ]; then
    # Ask if this is really the correct boot partition
    printf "Do you want to create the file \"\033[0;32m$BOOT_PATH/ssh\033[0m\" to enable SSH? (y/n): "
    read CHOICE
    case $CHOICE in
        n|N) 
	        echo "SSH file was not created, you should do this manually now to enable SSH."
	        exit 0
	        ;;
        y|Y)	        
            # Create ssh file on boot partition to enable SSH on boot
	        touch $BOOT_PATH/ssh
	        echo "File \"\033[0;32m$BOOT_PATH/ssh\033[0m\" was created to enable SSH."
	        echo "You can reach the device via SSH on \033[0;32mpi@raspberrypi.local\033[0m using the default password \"\033[0;32mraspberry\033[0m\"."
	        ;;
    esac
else
    # Assumed boot partition could not be found
    echo "Created boot partition could not be found. Please manually create a file named \"\033[0;32mssh\033[0m\" on it to enable SSH."       
fi
  

# Everything done
echo "Everything done, exiting."
exit 0
