NODES="$(< $1)"
for X in $NODES;
do
   echo "Check Status of $X"
   ping -c 2 $X
done
