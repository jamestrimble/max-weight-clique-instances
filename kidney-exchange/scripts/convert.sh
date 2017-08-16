mkdir -p kidney_converted
mkdir -p kidney_json
mkdir -p kidney_mwc

unzip kidney.zip -d kidney

for i in $(seq -w 1 100); do
    echo $i
    cat kidney/MD-00001-00000$i.wmd | python convert.py > kidney_converted/$i.input_and_ndds
    cat kidney_converted/$i.input_and_ndds | python to_json.py > kidney_json/$i.json
done

for i in $(seq -w 1 100); do
    echo $i
    gzip -c <(python kep_h/kep_h.py -f kidney_json/$i.json \
	-c effective:size:inverse3way:backarc -s 12:12:12 -e 3 -n 2 -i) \
	> kidney_mwc/$i.wclq.gz
done
