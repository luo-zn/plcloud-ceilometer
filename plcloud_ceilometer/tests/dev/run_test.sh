#! /bin/bash
# Author: Zhennan.luo(Jenner)


main(){
if [[ "$#" == "0" ]];then
    python -m unittest discover -p ${DEV_TEST_PATH}/test*.py
else
    python -m unittest discover "$@"
fi
}
main "$@"
