from django.shortcuts import render, HttpResponse, redirect
from django.utils import timezone
from core.Carrito import Carrito
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import  Handroll, Article, Comanda, Selladitas, Desayuno, Almuerzo, HandrollReady, Kai, Selladitas, Bowl
from .models import ProteinaBowl,ProteinaAlmuerzo,ProteinaBowl,ProteinaDesayuno,ProteinaHandroll,BaseBowl,SalsaBowl,ExtraBowl
from .models import VegetalesHandroll,AgregadoAlmuerzo,QuesoDesayuno,VegetalesDesayuno

from .forms import NewUserForm, BowlForm, DesayunoForm, AlmuerzoForm, HandrollForm, ComentForm,HandrollClassicForm
from .forms import ComdForm, KaiForm
from .Carrito import Carrito
from django.shortcuts import (get_object_or_404,
							render,
							HttpResponseRedirect)
from django.db.models import Q
from datetime import datetime
from json import dumps


def menu(request):
    return render(request,'menu/menu.html')

def tienda(request):
    #Insumos
    probwl=ProteinaBowl.objects.all()
    pa = ProteinaAlmuerzo.objects.all()
    pd=ProteinaDesayuno.objects.all()
    ph=ProteinaHandroll.objects.all()
    bb=BaseBowl.objects.all()
    sb=SalsaBowl.objects.all()
    eb=ExtraBowl.objects.all()
    vh= VegetalesHandroll.objects.all()
    aa=AgregadoAlmuerzo.objects.all()
    qd=QuesoDesayuno.objects.all()
    vd=VegetalesDesayuno.objects.all()
    # Se obtiene todos los objetos de cada tipp=o
    bowls = Bowl.objects.all()
    hc = HandrollReady.objects.all()
    al = Almuerzo.objects.all()
    des = Desayuno.objects.all()
    sell = Selladitas.objects.all()
    # se asigna a una variable lo obtenido del buscador
    queryset = request.GET.get("buscar")
    # si el campo del objeto contiene el queryset lo filtra. Distinct para que no haya conflicto con dos o mas iguales
    if queryset:
        productos = Product.objects.filter(
            Q(id__icontains=queryset)
        ).distinct()
        bowls = Bowl.objects.filter(
            Q(id__icontains=queryset)
        ).distinct()
        hc = HandrollReady.objects.filter(
            Q(id__icontains=queryset)
        ).distinct()
        al = Almuerzo.objects.filter(
            Q(id__icontains=queryset)
        ).distinct()
        des = Desayuno.objects.filter(
            Q(id__icontains=queryset)
        ).distinct()
        sell = Selladitas.objects.filter(
            Q(id__icontains=queryset)
        ).distinct()
    # Contezto de datos
    context = {
        "b": bowls,
        "hc": hc,
        "al": al,
        "des": des,
        "sell": sell,
        "probwl":probwl,
        "proal":pa,
        "prodes":pd,
        "prohand":ph,
        "basebowl":bb,
        "ssbowl":sb,
        "extbowl":eb,
        "vgthand":vh,
        "agral":aa,
        "qsdes":qd,
        "bgtdes":vd
    }
    # Se retorna un render del template correspondiente a la ruta y le pasa el contexto
    return render(request, "core/tienda.html", context)


# Funcion agregar que tiene como parametro id y tipo del objeto
@login_required
def agregar_producto(request, producto_id, typ):
    # Se obtiene el carrito
    carrito = Carrito(request)
    # Segun el tipo del objeto, lo obtiene por id
    if typ == 'hc':
        producto = HandrollReady.objects.get(id=producto_id)
    elif typ == 'h':
        producto = Handroll.objects.get(id=producto_id)
    elif typ == 'kai':
        producto = Kai.objects.get(id=producto_id)
    elif typ == 'al':
        producto = Almuerzo.objects.get(id=producto_id)
    elif typ == 'b':
        producto = Bowl.objects.get(id=producto_id)
    elif typ == 'des':
        producto = Desayuno.objects.get(id=producto_id)
    elif typ == 'sell':
        producto = Selladitas.objects.get(id=producto_id)

    else:
        producto = ''
    # Se agrega objeto en carrito
    carrito.agregar(producto)
    # Redirecciona a tienda
    return redirect("Tienda")

# Funciones que ejecutan funciones de Carrito.py


@login_required
def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Product.objects.get(id=producto_id)
    carrito.eliminar(producto)
    return redirect("Tienda")


@login_required
def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Product.objects.get(id=producto_id)
    carrito.restar(producto)
    return redirect("Tienda")


@login_required
def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("Tienda")


@login_required
def Confirm(request):
    form = ComentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
                a = form.save(commit=True)
                comd.coments = a
        return redirect('')
    context = {
        "form": form,
    }
    return render(request, 'core/confirm.html', context)


@login_required
def ToKitchen(request):
    # Generar una comanda
    comd = Comanda()
    # definir un tiempo con valor inicial cero
    tmp = 1
    # si hay items en el carrito entonces lo recorre
    if request.session["carrito"].items:
        for key, value in request.session["carrito"].items():
            # Crea un nuevo articulo, asigna valor y lo guarda
            article = Article()
            article.cod = value["nombre"]
            article.name = value["nombre"]
            article.cantidad = value["cantidad"]
            article.total = value["acumulado"]
            article.save()
            comd.save()
            # agrega el articulo en la comanda
            comd.article.add(article)
            comd.save()
            #si tiempo del producto es menor al tmp lo reemplaza. Si n0, suma 1
            if value["tiempo"]>tmp:
                tmp=value["tiempo"]
            else:
                tmp = tmp + 1

        # Cambia el estado de la ccmanda cuando pasa a cocina
        comd.cooking = True
        #asigna tiempo a comanda
        comd.time = tmp

        form = ComentForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                a = form.save(commit=True)
                comd.coments = a
            return redirect('kitchen')
        # Asigna hora de paso a cocina
        comd.time_to_kitchen = timezone.now()
        username = None
        if request.user.is_authenticated:
            username = request.user.username
            comd.author = username        
        comd.save()
        # limpia carrito
        request.session["carrito"]={}
    else:
        print('no hay carirto')

    return redirect("Tienda")
      
@login_required
def Kitchen(request):
    cmd = Comanda.objects.all()
    artcl = Article.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(cmd, 6)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    context={
        "cmd":users,
        "artcl":artcl,
    }
    return render(request, 'core/kitchen.html',context)

@login_required
def KitchenAll(request):
    cmd = Comanda.objects.all()
    artcl = Article.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(cmd, 6)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    context={
        "cmd":users,
        "artcl":artcl,
    }
    return render(request, 'core/kitchenall.html',context)

@login_required
def Ready(request,comd_id):
    cmd = Comanda.objects.get(id=comd_id)
    cmd.cooking=False
    cmd.finished=True
    cmd.time_finished= timezone.now()    
    cmd.save()
    return redirect("confirm")

# Listar productos
@login_required
def ListaProducto(request):
    p=Product.objects.all()
    context={
        "product":p,
    }
    return render(request, 'core/list/list_product.html',context)

@login_required
def ListaHC(request):
    p=HandrollReady.objects.all()
    context={
        "product":p,
    }
    return render(request, 'core/list/list_hc.html',context)

@login_required
def ListaAl(request):
    p=Almuerzo.objects.all()
    context={
        "product":p,
    }
    return render(request, 'core/list/list_al.html',context)

@login_required
def ListaKai(request):
    p=Kai.objects.all()
    context={
        "product":p,
    }
    return render(request, 'core/list/list_kai.html',context)

@login_required
def ListaSell(request):
    p=Selladitas.objects.all()
    context={
        "product":p,
    }
    return render(request, 'core/list/list_sell.html',context)

@login_required
def NuevoProducto(request):
    p=Product.objects.all()
    form=ProductForm(request.POST or None)
    if request.method == 'POST':
        

        if form.is_valid():
            a=form.save(commit=True)

            return HttpResponseRedirect("/listaproducto/")
        else:
            print('error')  
    context={
        "product":p,
        "form":form,
    }
    return render(request, 'core/new/new_product.html',context)


@login_required
def Update(request,id):
    context={

    }
    obj = get_object_or_404(Product, id = id)

    form = ProductForm(request.POST or None, instance = obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/listaproducto/")
    else:
        print('error')

    context["form"] = form

    return render(request, 'core/update_product.html',context)

@login_required
def EliminarProducto(request,id):
    # dictionary for initial data with
    # field names as keys
    
 
    # fetch the object related to passed id
    obj = get_object_or_404(Product, id = id)
    context ={
        'product':obj
    }
 
    if request.method =="POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return HttpResponseRedirect("/")
 
    
    return render(request, 'core/delete_product.html',context)

@login_required
def registros(request):
    bf= BowlForm()
    dsyn = DesayunoForm()
    almrz = AlmuerzoForm()
    hr = HandrollForm()
    hrcls = HandrollReady.objects.all()
    kai = Kai.objects.all()
    sll = Selladitas.objects.all()
    context={
        "bf":bf,
        "dsyn":dsyn,
        "almrz":almrz,
        "hr":hr,
        "hrcls":hrcls,
        "kai":kai,
        "sll":sll,
    }
    return render(request, 'core/registros.html',context)

@login_required
def NewBowl(request):
    bf= BowlForm()
    form= BowlForm()
    form=BowlForm(request.POST or None)
    if request.method == 'POST':
        

        if form.is_valid():
            a=form.save(commit=True)
            b = agregar_producto(request,a.id, a.typ)
            return HttpResponseRedirect("/")
        else:
            print('error') 
    context={
        "bf":bf,
        "form":form,
    }
    return render(request, 'core/new/newbowl.html',context)

@login_required
def NewAlmuerzo(request):
    form= AlmuerzoForm()
    form=AlmuerzoForm(request.POST or None)
    if request.method == 'POST':
        

        if form.is_valid():
            a=form.save(commit=True)
            b = agregar_producto(request,a.id, a.typ)
            return HttpResponseRedirect("/")
        else:
            print('error') 
    context={
        "form":form,
    }
    return render(request, 'core/new/newalmuerzo.html',context)

@login_required
def NewHandroll(request):
    form= HandrollForm()
    form=HandrollForm(request.POST or None)
    if request.method == 'POST':
        

        if form.is_valid():
            a=form.save(commit=True)
            b = agregar_producto(request,a.id, a.typ)
            return HttpResponseRedirect("/")
        else:
            print('error') 
    context={
        "form":form,
    }
    return render(request, 'core/new/newhandroll.html',context)

@login_required
def NewHandrollClassic(request):
    form= HandrollClassicForm()
    form=HandrollClassicForm(request.POST or None)
    if request.method == 'POST':
        

        if form.is_valid():
            a=form.save(commit=True)
            b = agregar_producto(request,a.id, a.typ)
            return HttpResponseRedirect("/")
        else:
            print('error') 
    context={
        "form":form,
    }
    return render(request, 'core/new/newhcclassic.html',context)


@login_required
def NewDesayuno(request):
    form= DesayunoForm()
    form=DesayunoForm(request.POST or None)
    if request.method == 'POST':
        

        if form.is_valid():
            a=form.save(commit=True)
            b = agregar_producto(request,a.id, a.typ)
            return HttpResponseRedirect("/")
        else:
            print('error') 
    context={
        "form":form,
    }
    return render(request, 'core/new/newdesayuno.html',context)




# Registro
def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("/")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="core/register.html", context={"register_form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="core/login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("/")

#para cambiar el estado, una funcion por objeto

def changeStatePB(request,id):
    ins= ProteinaBowl.objects.get(id=id)
    if ins.state == True:
        ins.state = False
        ins.save()
        return HttpResponseRedirect("/listaisum")
    else:
        ins.state = True
        ins.save()
        return HttpResponseRedirect("/listaisum")

def changeStatePA(request,id):
    ins= ProteinaAlmuerzo.objects.get(id=id)
    if ins.state == True:
        ins.state = False
        ins.save()
        return HttpResponseRedirect("/listaisum")
    else:
        ins.state = True
        ins.save()
        return HttpResponseRedirect("/listaisum")
def changeStatePD(request ,id):
    ins= ProteinaDesayuno.objects.get(id=id)
    if ins.state == True:
        ins.state = False
        ins.save()
        return HttpResponseRedirect("/listaisum")
    else:
        ins.state = True
        ins.save()
        return HttpResponseRedirect("/listaisum")

def changeStatePH(request,id):
    ins= ProteinaHandroll.objects.get(id=id)
    if ins.state == True:
        ins.state = False
        ins.save()
        return HttpResponseRedirect("/listaisum")
    else:
        ins.state = True
        ins.save()
        return HttpResponseRedirect("/listaisum")

def changeStateBB(request,id):
    ins= BaseBowl.objects.get(id=id)
    if ins.state == True:
        ins.state = False
        ins.save()
        return HttpResponseRedirect("/listaisum")
    else:
        ins.state = True
        ins.save()
        return HttpResponseRedirect("/listaisum")

def changeStateSB(request,id):
    ins= SalsaBowl.objects.get(id=id)
    if ins.state == True:
        ins.state = False
        ins.save()
        return HttpResponseRedirect("/listaisum")
    else:
        ins.state = True
        ins.save()
        return HttpResponseRedirect("/listaisum")

def changeStateEB(request,id):
    ins= ExtraBowl.objects.get(id=id)
    if ins.state == True:
        ins.state = False
        ins.save()
        return HttpResponseRedirect("/listaisum")
    else:
        ins.state = True
        ins.save()
        return HttpResponseRedirect("/listaisum")

def changeStateVH(request,id):
    ins= VegetalesHandroll.objects.get(id=id)
    if ins.state == True:
        ins.state = False
        ins.save()
        return HttpResponseRedirect("/listaisum")
    else:
        ins.state = True
        ins.save()
        return HttpResponseRedirect("/listaisum")

def changeStateAA(request,id):
    ins= AgregadoAlmuerzo.objects.get(id=id)
    if ins.state == True:
        ins.state = False
        ins.save()
        return HttpResponseRedirect("/listaisum")
    else:
        ins.state = True
        ins.save()
        return HttpResponseRedirect("/listaisum")

def changeStateQD(request,id):
    ins= QuesoDesayuno.objects.get(id=id)
    if ins.state == True:
        ins.state = False
        ins.save()
        return HttpResponseRedirect("/listaisum")
    else:
        ins.state = True
        ins.save()
        return HttpResponseRedirect("/listaisum")

def changeStateVD(request,id):
    ins= VegetalesDesayuno.objects.get(id=id)
    if ins.state == True:
        ins.state = False
        ins.save()
        return HttpResponseRedirect("/listaisum")
    else:
        ins.state = True
        ins.save()
        return HttpResponseRedirect("/listaisum")




def ListaInsumos(request):
    pb = ProteinaBowl.objects.all()
    pa = ProteinaAlmuerzo.objects.all()
    pd=ProteinaDesayuno.objects.all()
    ph=ProteinaHandroll.objects.all()
    bb=BaseBowl.objects.all()
    sb=SalsaBowl.objects.all()
    eb=ExtraBowl.objects.all()
    vh= VegetalesHandroll.objects.all()
    aa=AgregadoAlmuerzo.objects.all()
    qd=QuesoDesayuno.objects.all()
    vd=VegetalesDesayuno.objects.all()
    queryset = request.GET.get("buscar")
    # si el campo del objeto contiene el queryset lo filtra. Distinct para que no haya conflicto con dos o mas iguales
    if queryset:
        pb = ProteinaBowl.objects.filter(
            Q(name__icontains=queryset)
        ).distinct()
        pa = ProteinaAlmuerzo.objects.filter(
            Q(name__icontains=queryset)
        ).distinct()
        pd = ProteinaDesayuno.objects.filter(
            Q(name__icontains=queryset)
        ).distinct()
        ph = ProteinaHandroll.objects.filter(
            Q(name__icontains=queryset)
        ).distinct()
        bb = BaseBowl.objects.filter(
            Q(name__icontains=queryset)
        ).distinct()
        sb = SalsaBowl.objects.filter(
            Q(name__icontains=queryset)
        ).distinct()
        eb = ExtraBowl.objects.filter(
            Q(name__icontains=queryset)
        ).distinct()
        vh = VegetalesHandroll.objects.filter(
            Q(name__icontains=queryset)
        ).distinct()
        aa = AgregadoAlmuerzo.objects.filter(
            Q(name__icontains=queryset)
        ).distinct()
        qd = QuesoDesayuno.objects.filter(
            Q(name__icontains=queryset)
        ).distinct()
        vd = VegetalesDesayuno.objects.filter(
            Q(name__icontains=queryset)
        ).distinct()
    context = {
        "probowl":pb,
        "proal":pa,
        "prodes":pd,
        "prohand":ph,
        "basebowl":bb,
        "ssbowl":sb,
        "extbowl":eb,
        "vgthand":vh,
        "agral":aa,
        "qsdes":qd,
        "bgtdes":vd
    }
    return render(request,'core/list/list_insum.html',context)


def ListaComd(request):
    comd = Comanda.objects.all()
    context = {
        "comd":comd,
    }
    return render(request,'core/list/list_comd.html',context)

def updateComd(request,id):
    comd = Comanda.objects.get(id=id)
    form = ComdForm(instance=comd)
    if request.method == "POST":
        form = ComdForm(request.POST, instance=comd)
        if form.is_valid():
            a=form.save(commit=True)

            return HttpResponseRedirect("/listacomd/")
    else:
        form = ComdForm(instance=comd)
    context = {
        "form":form,
    }
    return render(request,'core/updatecomd.html',context)

def updateHC(request,id):
    hc = HandrollReady.objects.get(id=id)
    form = HandrollClassicForm(instance=hc)
    if request.method == "POST":
        form = HandrollClassicForm(request.POST, instance=hc)
        if form.is_valid():
            a=form.save(commit=True)

            return HttpResponseRedirect("/listaupdatehc/")
    else:
        form = HandrollClassicForm(instance=hc)
    context = {
        "form":form,
    }
    return render(request,'core/update/updatehc.html',context)

@login_required
def ListaUpdateHC(request):
    p=HandrollReady.objects.all()
    context={
        "product":p,
    }
    return render(request, 'core/update/listupdatehc.html',context)

def updateKai(request,id):
    kai = Kai.objects.get(id=id)
    form = KaiForm(instance=kai)
    if request.method == "POST":
        form = KaiForm(request.POST, instance=kai)
        if form.is_valid():
            a=form.save(commit=True)

            return HttpResponseRedirect("/listaupdatehc/")
    else:
        form = KaiForm(instance=kai)
    context = {
        "form":form,
    }
    return render(request,'core/update/updatekai.html',context)

@login_required
def ListaUpdateKai(request):
    p=Kai.objects.all()
    context={
        "product":p,
    }
    return render(request, 'core/update/listupdatekai.html',context)