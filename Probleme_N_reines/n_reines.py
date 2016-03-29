# Problème des N reines
#
# Comment placer N reines sur un échiquier (une par ligne) sans qu'elles ne se menacent mutuellement ?
# Une solution sera codée dans une chaine de caractères présentant, ligne par ligne, séparées par des espaces, la position de chaque reine.

import random
import operator

NB_REINES = 20
TAILLE_POPU = 400
NB_GENE = 1001

def gene_popu_ini(taille):
	popu = {}
	for i in range(taille):
		z = ' '.join([str(random.randint(0, NB_REINES - 1)) for k in range(NB_REINES)])
		while z in popu:
			z = ' '.join([str(random.randint(0, NB_REINES - 1)) for k in range(NB_REINES)])
		popu[z] = 0

	return popu

def eval_indi(indi0):
	indi = indi0.split()
	S = 0
	for k in range(len(indi)):
		for i in range(k+1, len(indi)):
			if indi[k] == indi[i]:
				S += 1
			elif int(indi[k]) + k == int(indi[i]) + i:
				S += 1
			elif int(indi[k]) + len(indi) - k == int(indi[i]) + len(indi) - i:
				S += 1
	return S

def eval_popu(popu):
	for elt in popu:
		popu[elt] = eval_indi(elt)

	return popu

def mute_indi(indi0):
	'''
	Modifie aléatoirement trois éléments de l'individu.
	'''
	indi = indi0.split()
	rk1 = random.randint(0,NB_REINES-1)
	rk2 = rk1
	rk3 = rk1
	rk4 = rk1
	while rk1 == rk2:
		rk2 = random.randint(0,NB_REINES-1)
	while rk3 == rk2 or rk3 == rk1:
		rk3 = random.randint(0,NB_REINES-1)
	while rk4 == rk3 or rk4 == rk2 or rk4 == rk1:
		rk4 = random.randint(0,NB_REINES-1)

	nw1 = str(indi[rk1])
	nw2 = str(indi[rk2])
	nw3 = str(indi[rk3])
	nw4 = str(indi[rk4])
	while nw1 == indi[rk1]:
		nw1 = str(random.randint(0,NB_REINES-1))
	while nw2 == indi[rk2]:
		nw2 = str(random.randint(0,NB_REINES-1))
	while nw3 == indi[rk3]:
		nw3 = str(random.randint(0,NB_REINES-1))
	while nw4 == indi[rk4]:
		nw4 = str(random.randint(0,NB_REINES-1))

	l = [i for i in indi]
	l[rk1] = nw1
	l[rk2] = nw2
	l[rk3] = nw3
	l[rk4] = nw4

	return ' '.join(l)

def cros_indi(indi10, indi20):
	'''
	Genere deux nouveaux individus en croisant deux individus.
	Le croisement se fait à un rang aléatoire.
	'''
	indi1 = indi10.split()
	indi2 = indi20.split()
	rk = random.randint(1, NB_REINES-1)

	return ' '.join(indi1[:rk] + indi2[rk:]), ' '.join(indi2[:rk] + indi1[rk:])

def regen_popu(popu):
	'''
	Le top 10 % de la population est conservé.
	Pour chacun, 3 sont créés par mutation.
	Et 6 autres par croisement avec un autre issu du top 20 %.
	'''
	popu_classee = [i[0] for i in sorted(popu.items(), key=operator.itemgetter(1))]
	popu10 = popu_classee[:len(popu_classee) // 10]
	popu20 = popu_classee[:len(popu_classee) // 5]

	new_popu = {}

	for i in popu10:
		new_popu[i] = 0

		for j in range(3):
			nn = mute_indi(i)
			new_popu[nn] = 0

		for j in range(3):
			k = cros_indi(i, popu20[random.randint(0, len(popu20)-1)])
			new_popu[k[0]] = 0
			new_popu[k[1]] = 0

	while len(new_popu) < TAILLE_POPU:
		new_popu[' '.join([str(random.randint(0, NB_REINES - 1)) for k in range(NB_REINES)])] = 0

	return eval_popu(new_popu), popu_classee[0]

popu = gene_popu_ini(TAILLE_POPU)
popu = eval_popu(popu)

for i in range(NB_GENE):
	rgn = regen_popu(popu)
	popu = rgn[0]
	top1 = rgn[1]

	if i % 100 == 0 or popu[top1] == 0:
		print("Génération %d - %s (%d)" % (i, top1, popu[top1]))
		if popu[top1] == 0:
			break
