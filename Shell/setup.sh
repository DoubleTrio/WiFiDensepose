if [ -z "$1" ]
  then
    echo "No destination supplied"
    exit 1
fi

# ==== STEP 0 DOWNLOAD ALL NECESSARY LIBRARIES
sudo apt update
sudo apt install build-essential clang flex bison g++ gawk gcc-multilib g++-multilib \
gettext git libncurses-dev libssl-dev python3-distutils rsync unzip zlib1g-dev \
file wget

# ==== STEP 1 DOWNLOAD SOURCE FROM OPENWRT ====
# Download and update the sources  
git clone https://git.openwrt.org/openwrt/openwrt.git  
cd openwrt  
git pull  
# Select a specific code revision  
git branch -a  
git tag  
git checkout v22.03.5

# Update the feeds  
./scripts/feeds update -a  
./scripts/feeds install -a  

# Configure the firmware image and the kernel  
make menuconfig  
make -j$(nproc) kernel_menuconfig  

# Build the firmware image  
make -j$(nproc) defconfig download clean world

# ==== STEP 2 SET PATH ====
# Note: toolchain-mips_24kc_gcc-11.2.0_musl can be different depending on what version of 
# OpenWrt and toolchain you use

export PATH=$PATH:$(pwd)/staging_dir/toolchain-mips_24kc_gcc-11.2.0_musl/bin
export TOOLCHAIN_DIR=$(pwd)/staging_dir/toolchain-mips_24kc_gcc-11.2.0_musl

# ==== STEP 3 COMPILE ATHEROS TOOL ====
cd ../
git clone https://github.com/DoubleTrio/Atheros_CSI_tool_OpenWRT_UserSpaceApp_src
cd Atheros_CSI_tool_OpenWRT_UserSpaceApp_src
cd sendData 
make
cd ../
cd recvCSI
make

read -p "Connect to the router and press enter to continue"

# ==== STEP 4 SEND THE PROGRAM TO THE ROUTERS ====
scp recvSCI $1
cd ../
cd sendData
scp sendData $1