#! /bin/bash
# Author: Zhennan.luo(Jenner)


main(){
if [[ "$#" == "0" ]];then
    /usr/bin/python ${DEV_TEST_PATH}/test*.py
else
    /usr/bin/python -m unittest discover "$@"
fi
}
main "$@"
