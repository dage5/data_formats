iters=3
smallFiles=60000
smallFiles=50

sudo mkdir /mnt/tmp

sudo mount -t tmpfs -o size=700M tmpfs /mnt/tmp

cp ./netCDF.py /mnt/tmp/netCDF.py
cp ./hdf.py /mnt/tmp/hdf.py
cp ./CDF.py /mnt/tmp/CDF.py
cp ./ascii.py /mnt/tmp/ascii.py
cp ./common.py /mnt/tmp/common.py
cp ./outfil_0 /mnt/tmp/outfil_0

echo "===============RAM==============="
cd /mnt/tmp/

echo "===============ascii==============="
python3 /mnt/tmp/ascii.py $iters $smallFiles

echo "===============netCDF==============="
python3 /mnt/tmp/netCDF.py $iters $smallFiles

echo "===============hdf==============="
python3 /mnt/tmp/hdf.py $iters $smallFiles

echo "===============CDF==============="
python3 /mnt/tmp/CDF.py $iters $smallFiles

cd /home/

sudo umount -f /mnt/tmp
sudo rm -r /mnt/tmp/


echo "===============HDD==============="
cd /home/developer/Documents/data_formats/

echo "===============ascii==============="
python3 ascii.py $iters $smallFiles

echo "===============netCDF==============="
python3 netCDF.py $iters $smallFiles

echo "===============hdf==============="
python3 hdf.py $iters $smallFiles

echo "===============CDF==============="
python3 CDF.py $iters $smallFiles
