iters=100


echo "===============RAM==============="

echo "===============netCDF==============="
python3 netCDF.py $iters

echo "===============hdf==============="
python3 hdf.py $iters

echo "===============CDF==============="
python3 CDF.py $iters

echo "===============ascii==============="
python3 ascii.py $iters


echo "===============HDD==============="

echo "===============netCDF==============="
python3 netCDF.py $iters

echo "===============hdf==============="
python3 hdf.py $iters

echo "===============CDF==============="
python3 CDF.py $iters

echo "===============ascii==============="
python3 ascii.py $iters
