python parse_bib.py pubs.bib all > indexlist.html
python parse_bib.py pubs.bib spectroscopy > spectroscopy/indexlist.html
python parse_bib.py pubs.bib photosynthesis > photosynthesis/indexlist.html
python parse_bib.py pubs.bib theory > theory/indexlist.html


DIRS=( "./" "photosynthesis" "spectroscopy" "theory" )

for dir in ${DIRS[@]}
do
	cat ${dir}/indexhead.html ${dir}/indexlist.html > ${dir}/index.html
done
