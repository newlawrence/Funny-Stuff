CFOR = gfortran
CCPP = g++
OBJECTS = semep.o semep_fw.o
MODULES = semep.mod
FLAGS = -lstdc++ -lm

semep: example.o $(OBJECTS) $(MODULES)
	$(CFOR) -o example example.o $(OBJECTS) $(FLAGS)
	
example.o: example.f95 $(MODULES)
	$(CFOR) -c example.f95 -O3
semep.o: semep.cpp semep.h
	$(CCPP) -c semep.cpp -O3
semep.mod: semep_fw.o
semep_fw.o: semep_fw.f95
	$(CFOR) -c semep_fw.f95 -O3

.PHONY: clean
clean:
	-rm *.o *.mod