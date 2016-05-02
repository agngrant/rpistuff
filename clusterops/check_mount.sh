NODES="$(< $1)"
for X in $NODES;
do
   echo "Checking Mount Status of $X"
   ssh "pi@$X" 'sudo mount weedoorman:/home/shared_dir /home/shared_dir'
done
