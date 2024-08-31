import os
import pickle
import os.path


class Empleado:
    def __init__(self):
        self.legajo = 0
        self.nomyape = ""
        self.sueldo = 0.00
        self.estado = "A"  # 'A' activo. 'B' baja


# validaciones


def validaRango(nro, desde, hasta):
    try:
        int(nro)
        if int(nro) >= desde and int(nro) <= hasta:
            return False
        else:
            return True
    except:
        return True


def validaRangoReales(nro, desde, hasta):
    try:
        float(nro)
        if float(nro) >= desde and float(nro) <= hasta:
            return False
        else:
            return True
    except:
        return True


def busquedaDico(L):  # Busqueda dicotomica
    global afEmpleados, alEmpleados
    alEmpleados.seek(0, 0)
    aux = pickle.load(alEmpleados)
    tamReg = alEmpleados.tell()
    cantReg = os.path.getsize(afEmpleados) // tamReg
    desde = 0
    hasta = cantReg - 1  # Cantidad de registros -1
    medio = (desde + hasta) // 2
    alEmpleados.seek(medio * tamReg, 0)
    vrEmp = pickle.load(alEmpleados)
    while int(vrEmp.legajo) != L and desde < hasta:
        if L < int(vrEmp.legajo):  # Ajusta intervalo de busqueda
            hasta = medio - 1
        else:
            desde = medio + 1
        medio = (desde + hasta) // 2
        alEmpleados.seek(medio * tamReg, 0)
        vrEmp = pickle.load(alEmpleados)
    if int(vrEmp.legajo) == L:
        return medio * tamReg
    else:  # En caso de no encontrarlo retorna -1
        return -1
    # 33 min


def ordenaEmpleados():  # Ordenamiento falso burbuja
    global afEmpleados, alEmpleados
    alEmpleados.seek(0, 0)
    aux = pickle.load(alEmpleados)
    tamReg = alEmpleados.tell()
    tamArch = os.path.getsize(afEmpleados)
    cantReg = int(tamArch / tamReg)
    for i in range(0, cantReg - 1):
        for j in range(i + 1, cantReg):
            alEmpleados.seek(i * tamReg, 0)
            auxi = pickle.load(alEmpleados)
            alEmpleados.seek(j * tamReg, 0)
            auxj = pickle.load(alEmpleados)
            if auxi.legajo > auxj.legajo:
                alEmpleados.seek(i * tamReg, 0)
                pickle.dump(auxj, alEmpleados)
                alEmpleados.seek(j * tamReg, 0)
                pickle.dump(auxi, alEmpleados)


def formatearEmpleado(vrEmp):
    vrEmp.legajo = str(vrEmp.legajo)
    vrEmp.legajo = vrEmp.legajo.ljust(10, " ")
    vrEmp.nomyape = vrEmp.nomyape.ljust(40, " ")
    vrEmp.sueldo = str(vrEmp.sueldo)
    vrEmp.sueldo = vrEmp.sueldo.ljust(10, " ")
    # el estado no lo formatea porque es un char y le asigna valores fijos
    # de la misma longitud 'A' o 'B'


def modificarEmpleado():
    global afEmpleados, alEmpleados
    os.system("cls")
    print("OPCION 2 - Modificacion de un empleado.")
    print("--------------------------\n")
    t = os.path.getsize(afEmpleados)
    if t == 0:
        print("No hay empleados registrados\n.")
        os.system("pause")
    else:
        leg = input(
            "Ingresar el legajo del empleado a modificar. Entre 1 y 99999. [0] para salir: "
        )
        while validaRango(leg, 0, 99999):
            leg = input("Incorrecto - Entre 1 y 99999. [0] para salir: ")
        leg = int(leg)
        if leg != 0:
            pos = buscarEmpleado(leg)
            if pos == -1:
                print("El legajo del empleado no existe. ")
            else:
                emp = Empleado()
                alEmpleados.seek(pos, 0)
                emp = pickle.load(alEmpleados)
                if emp.estado == "B":
                    print("El empleado esta dado de baja (no es posible modificar)")
                else:
                    print("Empleado a modificar: ")
                    mostrarEmpleado(emp)
                    print(
                        "\n Solo se podran modificar el nombre y apellido y su sueldo. "
                    )
                    emp.nomyape = input(
                        "Nuevo nombre y apellido <hasta 40 caracteres>: "
                    )
                    while len(emp.nomyape) < 1 or len(emp.nomyape) > 40:
                        emp.nomyape = input(
                            "Incorrecto - Nombre y apellido <hasta 40 caracteres>: "
                        )
                    emp.sueldo = input("Nuevo sueldo <entre 100000 y 500000>: ")
                    while validaRangoReales(emp.sueldo, 100000, 500000):
                        emp.sueldo = input(
                            "Incorrecto - sueldo valido entre 100000 y 500000: "
                        )
                    emp.sueldo = float(emp.sueldo)
                    rpta = input("Confirma los cambios? (SI o NO): ")
                    while rpta.lower() != "si" and rpta.lower() != "no":
                        rpta = input("Incorrecto  - Confirma los cambios? (SI o NO): ")
                    if rpta.lower() == "si":
                        alEmpleados.seek(pos)
                        formatearEmpleado(emp)
                        pickle.dump(emp, alEmpleados)
                        alEmpleados.flush()
                        print("Modificacion exitosa")
                        print("Los datos actualizados del empleado son: ")
                        mostrarEmpleado(emp)
            os.system("pause")


def buscarEmpleado(leg):  # Busqueda secuencial
    global afEmpleados, alEmpleados
    t = os.path.getsize(afEmpleados)
    vrTemp = Empleado()
    alEmpleados.seek(0)
    while alEmpleados.tell() < t:
        pos = alEmpleados.tell()
        vrTemp = pickle.load(alEmpleados)
        if int(vrTemp.legajo) == leg:
            return pos
    return -1


def altaEmpleado():
    global afEmpleados, alEmpleados
    os.system("cls")
    print("OPCION 1 - Alta de empleados")
    print("---------------------\n")
    t = os.path.getsize(afEmpleados)
    if t == 0:
        print("No hay empleados registrados")
    else:
        print("Lista de empleados")
        print("------------------")
        alEmpleados.seek(0)
        while alEmpleados.tell() < t:
            vrEmp = pickle.load(alEmpleados)
            mostrarEmpleado(vrEmp)
            print()
    leg = input(
        "Ingresar el legajo del empleado a dar de alta. Entre 1 y 99999. [0] para salir: "
    )
    while validaRango(leg, 0, 99999):
        leg = input("Incorrecto - Entre 1 y 99999. [0] para salir: ")
    leg = int(leg)
    emp = Empleado()
    while leg != 0:
        if buscarEmpleado(leg) == -1:
            emp.legajo = leg
            emp.nomyape = input("Nombre y apellido <hasta 40 caracteres>: ")
            while len(emp.nomyape) < 1 or len(emp.nomyape) > 40:
                emp.nomyape = input(
                    "Incorrecto - Nombre y apellido <hasta 40 caracteres>: "
                )
            emp.sueldo = input("Sueldo <entre 100000 y 500000>: ")
            while validaRangoReales(emp.sueldo, 100000, 500000):
                emp.sueldo = input("Incorrecto - sueldo valido entre 100000 y 500000: ")
            emp.sueldo = float(emp.sueldo)
            formatearEmpleado(emp)
            pickle.dump(emp, alEmpleados)  # Graba
            alEmpleados.flush()  # Actualiza el .dat asociada a la variable de archivo
            print("Alta de empleado exitosa")
        else:
            print("Ya existe un empleado con el legajo", leg, "\n")
        os.system("pause")
        leg = input(
            "Ingrese el legajo del empleado a dar de alta. Entre 1 y 99999. [0] para volver: "
        )
        while validaRango(leg, 0, 99999):
            leg = input("Incorrecto - Entre 1 y 99999. [0] para volver: ")
        leg = int(leg)


def bajaEmpleado():
    global afEmpleados, alEmpleados
    os.system("cls")
    print("OPCION 3 - Baja de un empleado.")
    print("--------------------------\n")
    t = os.path.getsize(afEmpleados)
    if t == 0:
        print("No hay empleados registrados\n.")
        os.system("pause")
    else:
        leg = input(
            "Ingresar el legajo del empleado a dar de baja. Entre 1 y 99999. [0] para salir: "
        )
        while validaRango(leg, 0, 99999):
            leg = input("Incorrecto - Entre 1 y 99999. [0] para salir: ")
        leg = int(leg)
        if leg != 0:
            pos = buscarEmpleado(leg)
            if pos == -1:
                print("El legajo del empleado no existe. ")
            else:
                emp = Empleado()
                alEmpleados.seek(pos, 0)
                emp = pickle.load(alEmpleados)
                if emp.estado == "B":
                    print("El empleado ya esta dado de baja")
                else:
                    print("Datos del empleado a dar de baja:")
                    mostrarEmpleado(emp)
                    rta = input("Confirma la baja? (Si o No): ")
                    while rta.lower() != "si" and rta.lower() != "no":
                        rta = input("Incorrecto - Confirma? (Si o No): ")
                    if rta.lower() == "si":
                        emp.estado = "B"
                        alEmpleados.seek(pos)
                        pickle.dump(emp, alEmpleados)
                        alEmpleados.flush()
                        print("Baja logica exitosa")
                        print("Los datos actualizados del empleado son: ")
                        mostrarEmpleado(emp)
            os.system("pause")


def listarEmpleadosActivos():
    global alEmpleados, afEmpleados
    os.system("cls")
    print("OPCION 4 - Lista de empleados activos")
    print("--------------------------------------\n")
    t = os.path.getsize(afEmpleados)
    if t == 0:
        print("No hay empleados registrados")
    else:
        ordenaEmpleados()
        encabezado = ""
        encabezado += "{:<15}".format("Legajo")
        encabezado += "{:<40}".format("Nombre y Apellido")
        encabezado += "{:<20}".format("Sueldo")
        encabezado += "{:<10}".format("Estado")
        print(encabezado)
        print("-" * 85)
        emp = Empleado()
        alEmpleados.seek(0)
        while alEmpleados.tell() < t:
            emp = pickle.load(alEmpleados)
            if emp.estado == "A":
                mostrarEmpleado(emp)
        print()
        leg = int(input("Ingrese legajo: "))
        if busquedaDico(leg) == -1:
            print("Legajo no encontrado")
        else:
            print("Legajo encontrado")
    os.system("pause")


# str
def mostrarMenu():
    os.system("cls")
    print(
        """ABM de empleados\n
    1 - Alta de empleados\t\t
    2 - Modificacion de un empleado\t\t
    3 - Baja de un empleado\t\t
    4 - Listado de empleados activos\t\t
    0 - Salir\t"""
    )


def mostrarEmpleado(emp):
    salida = ""
    salida += "{:<15}".format(emp.legajo.strip())
    salida += "{:<40}".format(emp.nomyape.strip())
    salida += "{:<20}".format(emp.sueldo.strip())
    salida += "{:<10}".format(emp.estado.strip())
    print(salida)


##  PROGRAMA PRINCIPAL
afEmpleados = "c:\\Recursos\\empleados.dat"

if not os.path.exists(afEmpleados):
    alEmpleados = open(afEmpleados, "w+b")
else:
    alEmpleados = open(afEmpleados, "r+b")

# Menu
op = -1
while op != 0:
    mostrarMenu()
    op = input("Ingresar una opcion: ")
    while validaRango(op, 0, 4):
        op = input("Incorrecto - Ingresar una opcion valida[0-4]: ")
    op = int(op)
    if op == 1:
        altaEmpleado()
    elif op == 2:
        modificarEmpleado()
    elif op == 3:
        bajaEmpleado()
    elif op == 4:
        listarEmpleadosActivos()
    elif op == 0:
        print("\n\nGracias por su visita ...\n\n")
        alEmpleados.close()
