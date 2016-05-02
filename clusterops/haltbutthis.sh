NODES="$(< $1)"
for X in $NODES;
do
   echo "Halt $X"
   ssh "pi@$X" 'sudo halt'
done
