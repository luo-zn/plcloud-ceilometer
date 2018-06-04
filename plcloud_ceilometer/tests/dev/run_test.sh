#! /bin/bash
# Author: Zhennan.luo(Jenner)


main(){
if [[ "$#" == "0" ]];then
    python ${DEV_TEST_PATH}/test*.py
else
    python -m unittest discover "$@"
fi
}
main "$@"
