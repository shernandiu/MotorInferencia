import re


class Ciclo:
    def __init__(self) -> None:
        self.anterior = None
        self.mesa_trabajo = set()
        self.conjunto_conflicto = []
        self.regla_aplicada = None

    def comprobar_refraccion(self, regla):
        i: Ciclo = self.anterior
        while(i is not None):
            if regla in i.conjunto_conflicto:
                if i.regla_aplicada == regla:
                    return False
                else:
                    i = i.anterior
            else:
                break
        return True

    def comprobar_ciclo(self, regla):
        i: Ciclo = self.anterior
        while(i is not None):
            if i.regla_aplicada == regla:
                if i.mesa_trabajo == self.mesa_trabajo:
                    return False
            i = i.anterior
        return True

    def calcular_cc(self):
        [self.conjunto_conflicto.append(i) for i in Regla.get_reglas() if self.comprobar_consecuente(i)]

    def comprobar_consecuente(self, regla) -> bool:
        for consecuente in regla.consecuente:
            if consecuente not in self.mesa_trabajo:
                return False
        for no_consecuente in regla.no_consecuente:
            if no_consecuente in self.mesa_trabajo:
                return False
        return True

    def generar_siguiente(self):
        for regla in self.conjunto_conflicto:
            if self.comprobar_refraccion(regla) and self.comprobar_ciclo(regla):
                regla_a_usar = regla
                break
        else:
            for regla in self.conjunto_conflicto:
                if self.comprobar_ciclo(regla):
                    regla_a_usar = regla
                    break
            else:
                return None

        self.regla_aplicada = regla_a_usar
        nuevo_ciclo = Ciclo()
        nuevo_ciclo.mesa_trabajo.update(self.mesa_trabajo)
        nuevo_ciclo.mesa_trabajo.update(regla_a_usar.anadir)
        nuevo_ciclo.mesa_trabajo.difference_update(regla_a_usar.eliminar)
        nuevo_ciclo.anterior = self
        return nuevo_ciclo


class Regla:
    __lista_reglas = None
    lista_reglas_con_variables = []

    def __init__(self, *args) -> None:
        """
        Constructor de regla
        args: Par??metros de la regla
        0 - Nombre
        1 - Consecuente
        2 - Lista a??adir
        3 - Lista eliminar
        4 - Consecuente negado
        """
        self.consecuente = set()
        self.no_consecuente = set()
        self.anadir = set()
        self.eliminar = set()
        self.replaces = {}

        self.nombre = args[0]
        try:
            [self.consecuente.add(i) for i in args[1]]
            [self.anadir.add(i) for i in args[2]]
            [self.eliminar.add(i) for i in args[3]]
            [self.no_consecuente.add(i) for i in args[4]]
            self.replaces = args[5]
        except IndexError:
            Regla.lista_reglas_con_variables.append(self)

    def sustituir(self, subtituciones: dict):
        propiedades = [self.consecuente, self.anadir, self.eliminar, self.no_consecuente]

        nuevas_props = []
        for prop in propiedades:
            nuevas_props.append([])
            for tupla_prop in prop:
                nuevas_props[-1].append(tuple([j if j not in subtituciones.keys() else subtituciones[j] for j in tupla_prop]))

        return Regla(self.nombre, *nuevas_props, subtituciones)

    def __str__(self) -> str:
        return self.nombre + str(self.replaces).replace('\'', '')

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Regla):
            return self.__str__() == __o.__str__()
        return False

    def __hash__(self) -> int:
        string: str = self.nombre+str(self.replaces)
        return string.__hash__()

    def print_ext(self) -> str:
        salida = self.nombre+': '
        salida += 'Si '
        if len(self.consecuente) > 0:
            lista_atrib = list(self.consecuente)
            for i in lista_atrib[:-1]:
                salida += str(i)+' ^ '
            salida += str(lista_atrib[-1])+' '
        if len(self.no_consecuente) > 0:
            lista_atrib = list(self.no_consecuente)
            for i in lista_atrib[:-1]:
                salida += '?? '
                salida += str(i)+' ^ '
            salida += '?? ' + str(lista_atrib[-1])+' '
        salida += 'Entonces '
        if len(self.anadir) > 0:
            lista_atrib = list(self.anadir)
            salida += 'A??adir '
            for i in lista_atrib[:-1]:
                salida += str(i)+' ^ '
            salida += str(lista_atrib[-1])+' '
        if len(self.eliminar) > 0:
            lista_atrib = list(self.eliminar)
            salida += 'Eliminar '
            for i in lista_atrib[:-1]:
                salida += str(i)+' ^ '
            salida += str(lista_atrib[-1])+' '
        return salida.replace('\'', '')

    def propiedades(self) -> set:
        return set().union(*self.consecuente, *self.no_consecuente, *self.anadir, *self.eliminar)

    @classmethod
    def get_reglas(self) -> list:
        if Regla.__lista_reglas is not None:
            return Regla.__lista_reglas

        r = re.compile('\$.')
        Regla.__lista_reglas = []

        for regla in Regla.lista_reglas_con_variables:
            list_of_regex = set()
            for consecuente in regla.consecuente:
                list_of_regex.update(filter(r.match, consecuente))

            for consecuente in regla.no_consecuente:
                list_of_regex.update(filter(r.match, consecuente))

            if len(list_of_regex) > 0:
                list_cartesian: list[list] = []
                for regex in list_of_regex:
                    list_cartesian.append([])
                    for character in LETRAS_PRESENTES:
                        list_cartesian[-1].append((regex, character))

                list_of_dicts: list[dict] = Regla.permutations(list_cartesian, 0, {})
                [Regla.__lista_reglas.append(i) for i in [regla.sustituir(j) for j in list_of_dicts]]
            else:
                Regla.__lista_reglas.append(regla)

        return Regla.__lista_reglas

    @classmethod
    def permutations(self, list_cartesian: list, current_iteration, progress: dict) -> list:
        done = []
        if current_iteration < len(list_cartesian):
            for i in list_cartesian[current_iteration]:
                new_dict = progress.copy()
                new_dict[i[0]] = i[1]
                done.extend(self.permutations(list_cartesian, current_iteration+1, new_dict))
        else:
            done.append(progress)

        return done


def __obtener_tupla(msg: str):
    prop = input(msg)
    prop = (prop[:a] if (a := prop.find('#')) != -1 else prop).strip()
    return prop.replace(' y ', ';').replace('^', ';').replace(', ', ';').split(';') if len(prop) > 0 else []


def __input(msg: str):
    prop = input(msg)
    return (prop[:a] if (a := prop.find('#')) != -1 else prop).strip()


def obtener_tupla(msg: str):
    return [tuple(x.strip(' ()').split(',')) for x in __obtener_tupla(msg)]


def obtener_tupla_doble(msg: str):
    prop = __obtener_tupla(msg)
    return [tuple(a.split(',')) for x in prop if (a := x.strip(' ()'))[0] != '??'], [tuple(a.strip(' ()??').split(',')) for x in prop if (a := x.strip(' ()'))[0] == '??']


LETRAS_PRESENTES = []
nombre = __input("Introduce el nombre de la regla: ")
while (len(nombre) > 0):
    consecuente, no_consecuente = obtener_tupla_doble("Introduce el consecuente: ")
    # no_consecuente = obtener_tupla("Introduce el consecuente negado: ")
    eliminar = obtener_tupla("Introduce la lista eliminar: ")
    anadir = obtener_tupla("Introduce la lista a??adir: ")
    Regla(nombre, consecuente, anadir, eliminar, no_consecuente)
    nombre = __input("\nIntroduce el nombre de la regla: ")

[print(i.print_ext()) for i in Regla.lista_reglas_con_variables]

c = Ciclo()
c.mesa_trabajo.update(obtener_tupla('Introduce la base de hechos: '))


tupla_a_comprobar = tuple(a.strip(' ()').split(',') if (a := __input('Introduce la tupla a buscar: ')) else [])


ciclo_maximo = None
if len(tupla_a_comprobar) == 0:
    ciclo_maximo = int(__input("Indica el ciclo m??ximo: "))

[LETRAS_PRESENTES.append(i) for i in set().union(*[x.propiedades() for x in Regla.lista_reglas_con_variables], *c.mesa_trabajo) if i[0] != '$']
LETRAS_PRESENTES.sort()

i = 0
while c is not None and (ciclo_maximo is None or i <= ciclo_maximo):
    print("Ciclo", i)
    i += 1

    print("MT:")
    [print(str(i).replace('\'', ''), end='  ') for i in c.mesa_trabajo]
    print()

    c.calcular_cc()

    print("CC:")
    [print(i, end='  ') for i in c.conjunto_conflicto]
    print()
    if tupla_a_comprobar in c.mesa_trabajo:
        break
    nc = c.generar_siguiente()
    print("Regla aplicada:")
    print(c.regla_aplicada)
    print()
    c = nc
if c is None:
    print("No se pueden aplicar mas reglas")
elif ciclo_maximo is not None and i > ciclo_maximo:
    print("Se ha llegado al ciclo m??ximo")
