NODES="$(< $1)"
for X in $NODES;
do
   echo "Add remote and pull $X"
   ssh "pi@$X" "cd rpistuff/;git remote add shared /home/shared_dir/rpistuff;git pull shared master"
done
