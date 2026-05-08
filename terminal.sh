#!/usr/bin/env bash 



# x=5
# y=3
# z=$x+$y
# echo $((z))




# x=5
# y=3
# z=$x-$y
# echo $((z))



# x=5
# y=3
# z="$x*$y"
# echo $((z))


# x=5
# y=3
# z=$x/$y
# echo $((z))


# x=5
# y=3
# z="$x%$y"
# echo $((z))



# greet(){
#     echo "$2" 
# }


# greet "$4" "$1 extra"


# echo arg count and all args $# "$@"


# while [ $# -gt 0 ]; do
#     echo "$1"
#     shift
# done



# if [ "$1" -gt 60 ]; then
#     echo "invalid seconds"
#     exit 1

# elif [ "$1" -le 60 ]; then
# echo 'valid seconds'
#      exit 0

# fi


# count=0 

# while [ $# -gt 0 ]; do
#     echo "$1" "$4"
#     shift
#     count=$((count+1))
#     echo "-----"
# done

# echo $count


# -m 10 
# -s 10
# -h 10



help_message(){
    echo "Help message placeholder"
    return 0

}



get_seconds(){
    result=0
    while [ $# -gt 0 ]; do
        if [ "$1" != --help ] &&  [ -z "$2" ];then
                echo "Missing arg -h -m -s"
                return 1
        fi
        case "$1" in
            -s) 
                result=$((result+$2))
                ;;
            -m) 
                result=$((result+($2*60)))
                ;;
            -h) 
                result=$((result+($2*60*60)))
                ;;
            -d)
                result=$((result+($2*24*60*60)))
                ;;
            --help)
                help_message
                return 0
                ;;
            *) 
                echo "invalid" 
                help_message
                return 1
       
        esac
             
        shift 2
    done
    echo "$result"
    return 0
}

get_seconds "$@"