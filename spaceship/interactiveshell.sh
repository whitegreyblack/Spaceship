read -n 1 key
case "$key" in
     '^[[C') echo "right";;
     *) echo "else";;
esac