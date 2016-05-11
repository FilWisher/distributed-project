TEST_MODULES="icarus"
#get comma-separated file paths for module names
MOD_PATHS=""
for mod in `echo $TEST_MODULES`
do
    MOD_PATHS="$MOD_PATHS,`python -c \"import os, $mod; print os.path.dirname($mod.__file__)\"`/*"
done
#remove preceding comma
MOD_PATHS=`echo $MOD_PATHS|cut -c2-`

coverage run test.py
coverage report --include=$MOD_PATHS
