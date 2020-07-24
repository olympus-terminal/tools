 #!/bin/bash
    counter=1
    while [ $counter -le 1000000 ];
    do
    echo $counter;
    ls -ltr;
    sleep 10s;
    ((counter++));
    done
    echo All done
