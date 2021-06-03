import pickle

open_file = open('jobs_magneto_ingenierias_dllo_estadistica_rh_mercadeo.pickle', "rb")
loaded_list = pickle.load(open_file)
open_file.close()
#print(loaded_list)
print(len(loaded_list))

open_file = open('jobs_magneto_ventas.pickle', "rb")
loaded_list1 = pickle.load(open_file)
open_file.close()
#print(loaded_list1)
print(len(loaded_list1))

open_file = open('jobs_magneto_faltantes.pickle', "rb")
loaded_list2 = pickle.load(open_file)
open_file.close()
#print(loaded_list2)
print(len(loaded_list2))

jobs_magneto_totals = dict()

jobs_magneto_totals.update(loaded_list)
jobs_magneto_totals.update(loaded_list1)
jobs_magneto_totals.update(loaded_list2)

file_to_write = open("jobs_magneto_totals.pickle", "wb")
pickle.dump(jobs_magneto_totals, file_to_write)

print(jobs_magneto_totals)
print(len(jobs_magneto_totals))