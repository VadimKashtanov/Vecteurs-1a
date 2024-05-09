#valgrind --track-origins=yes --leak-check=full --show-leak-kinds=all ./main
#cuda-gdb
#compute-sanitizer --tool memcheck
rm *.o
clear
printf "[\033[93m***\033[0m] \033[103mCompilation ...\033[0m \n"

#echo "!!! -G -g !!!";A="-Idef -diag-suppress 2464 -G -g -O0 -lm -lcublas_static -lcublasLt_static -lculibos -Xcompiler -fopenmp -Xcompiler -O0"
#echo "!!! -g !!!";A="-Idef -diag-suppress 2464 -g -O0 -lm -lcublas_static -lcublasLt_static -lculibos -Xcompiler -fopenmp -Xcompiler -O3"
A="-Idef -diag-suppress 2464 -O3 -lm -lcublas_static -lcublasLt_static -lculibos -Xcompiler -fopenmp -Xcompiler -O3"

# les 3 lignes au dessus : debbug cuda, debbug, optimiser

################################################################

#	/etc
nvcc -c impl/etc/etc.cu     ${A} &
nvcc -c impl/etc/espace.cu  ${A} &
nvcc -c impl/etc/btcusdt.cu ${A} &
#	/insts
nvcc -c impl/insts/insts.cu     ${A} &
#	/mdl
nvcc -c impl/mdl/mdl.cu ${A} &
#
#	Attente de terminaison des differents fils de compilation
#
wait

################################################################

#	Programme : "principale"
nvcc     -c impl/main.cu ${A}
nvcc *.o -o      main    ${A}
#
#	Attente de terminaison des differents fils de compilation
#
wait

################################################################

#	Verification d'erreure
if [ $? -eq 1 ]
then
	printf "\n[\033[91m***\033[0m] \033[101m [!] Erreure. Pas d'execution. [!]\033[0m\n"
	exit
else
	printf "[\033[92m***\033[0m] \033[102m========= Execution du programme =========\033[0m\n"
fi

#	Executer si Aucune erreur
time ./main
if [ $? -ne 0 ]
then
	printf "[\033[91m***\033[0m] \033[101m /!\ Erreur durant l'execution. /!\ \033[0m\n"
	exit
else
	printf "[\033[92m***\033[0m] \033[102mAucune erreure durant l'execution.\033[0m\n"
fi

rm *.o