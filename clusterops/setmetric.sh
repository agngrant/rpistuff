NODES="$(< $1)"
for X in $NODES;
do
   echo "set metric $X to $2"
   ssh "pi@$X" "cd rpistuff/;echo '$2' > metric.txt"
done
