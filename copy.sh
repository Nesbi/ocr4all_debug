IMAGENAME=$1
NUMBER=$2
OUTPUT=$3

if [ ! -d "$OUTPUT" ]; then
	mkdir $OUTPUT
fi

for i in $(seq 1 $NUMBER)
do
	NAME=$(printf "%04d" $i)
	cp $IMAGENAME $OUTPUT/$NAME
done
