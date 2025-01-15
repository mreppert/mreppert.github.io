cat head.html > index.html
#sed -n 's/\(.*\)href="#\(.*\)?">\(.*\)/\2/p' MatPlotLib.html >> index.html

INFILES=('MatPlotLib.html' 'NumPy.html' 'Signals.html')
SUBJECTS=("Plots and Figures" "Matrices and Vectors" "Spectroscopy and Signal Processing")
for((n=0; n<${#INFILES[@]}; n++))
do
	infile=${INFILES[$n]}
	subject=${SUBJECTS[$n]}

	echo "<h2>$subject</h2>">> index.html
	for dat in `sed -n 's/.*h1.*\(.*\)href="#\(.*\)?">\(.*\)\/h1\(.*\)/\2/p' $infile`; 
	do
		text=`echo $dat | sed 's/-/ /g'`"?"
		echo $dat
		echo "<p><a href=\"/education/pyfaqs/$infile#$dat?\">$text</a></p>" >> index.html
	done
done
echo "</html>" >> index.html

