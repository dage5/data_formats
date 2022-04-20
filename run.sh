iters=1 #1000
smallFiles=60 #60000
#smallFiles=50
passwd=developer

#echo -n "Enter sudo password "
#read passwd

# nohup bash run.sh > test_10_50 &

echo $passwd | sudo -S mkdir /mnt/tmp

echo $passwd | sudo -S mount -t tmpfs -o size=1500M tmpfs /mnt/tmp

cp ./netCDF.py /mnt/tmp/netCDF.py
cp ./hdf.py /mnt/tmp/hdf.py
cp ./CDF.py /mnt/tmp/CDF.py
cp ./ascii.py /mnt/tmp/ascii.py
cp ./common.py /mnt/tmp/common.py
cp ./outfil_0 /mnt/tmp/outfil_0

echo "===============RAM==============="
cd /mnt/tmp/

echo "===============ascii==============="
python3 /mnt/tmp/ascii.py $iters $smallFiles $passwd

echo "===============netCDF==============="
python3 /mnt/tmp/netCDF.py $iters $smallFiles $passwd

echo "===============hdf==============="
python3 /mnt/tmp/hdf.py $iters $smallFiles $passwd

echo "===============CDF==============="
python3 /mnt/tmp/CDF.py $iters $smallFiles $passwd

#exit 0

cd /home/

echo $passwd | sudo -S umount -f /mnt/tmp
echo $passwd | sudo -S rm -r /mnt/tmp/


echo "===============HDD==============="
cd /home/developer/Documents/data_formats/

echo "===============ascii==============="
python3 ascii.py $iters $smallFiles $passwd

echo "===============netCDF==============="
python3 netCDF.py $iters $smallFiles $passwd

echo "===============hdf==============="
python3 hdf.py $iters $smallFiles $passwd

echo "===============CDF==============="
python3 CDF.py $iters $smallFiles $passwd
