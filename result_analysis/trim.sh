fnames=("0_0_uncompressed_fps.png" "1_1_lossy_uncompressed_rps.png"
"0_1_lossy_uncompressed_fps.png" "1_2_compressed_rps.png"
"0_2_compressed_fps.png" "1_3_lossy_compressed_rps.png"
"0_3_lossy_compressed_fps.png" "2_compressed_ssd_to_ram.png"
"1_0_uncompressed_rps.png" "2_uncompressed_ssd_to_ram.png")


for i in "${fnames[@]}"
do
	convert $i -trim $i
done
