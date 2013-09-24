
#usage: source allinone.sh
srcs="constants.py canvas.py  chartMatrixCanvas.py seqChart.py"
dest="seqChartAllInOne.py" 
echo "###" > $dest 
for src in $srcs; do
	cat $src >> $dest 
done
