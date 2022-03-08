# remove all rst files except index.rst and README.rst
ls *.rst | grep -v  index.rst | grep -v README.rst | xargs rm
rm -rf _build/html
sphinx-apidoc -f -o . ../imperfect_info_games
make html
cp -a _build/html/. .
