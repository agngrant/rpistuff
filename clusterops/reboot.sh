NODES="$(< $1)"
for X in $NODES;
do
   echo "Check Mount Status of $X"
   ssh "pi@$X" 'sudo reboot'
done
