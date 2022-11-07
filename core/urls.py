from django.urls import path
#se importa todo de views
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    #path con render de template

    path('menu/',views.menu,name="menu"),

    path('', views.tienda, name="Tienda"),
    path('confirm/',views.Confirm,name='confirm'),
    path('kitchen/',views.Kitchen,name='kitchen'),
    path('kitchenall/',views.KitchenAll,name='kitchenAll'),
    path('listahc/', views.ListaHC, name='listhc'),
    path('listaal/', views.ListaAl, name='listal'),
    path('listakai/', views.ListaKai, name='listkai'),
    path('listasell/', views.ListaSell, name='listsell'),

    path('listacomd/', views.ListaComd, name='listcomd'),
    path('listaisum/', views.ListaInsumos, name='listinsum'),

    #formularios
    path('registros/',views.registros,name='registros'),
    path('newbowl/',views.NewBowl,name='newbowl'),
    path('newalmuerzo/',views.NewAlmuerzo,name='newalmuerzo'),
    path('newhandroll/',views.NewHandroll,name='newhandroll'),
    path('newhcclassic/',views.NewHandrollClassic,name='newhcclassic'),
    path('newdesayuno/',views.NewDesayuno,name='newdesayuno'),
    #falta newkai

    path('updatecomd/<int:id>',views.updateComd,name='updatecomd'),

    #ruta de funciones (sin rendear template)

    #Funciones de carrito
    path('agregar/<int:producto_id>/<str:typ>/', views.agregar_producto, name="Add"),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name="Del"),
    path('restar/<int:producto_id>/', views.restar_producto, name="Sub"),
    path('limpiar/', views.limpiar_carrito, name="CLS"),  
    path('tokitchen/',views.ToKitchen,name='tokitchen'),
    path('ready/<int:comd_id>',views.Ready,name='ready'),
    
    
    path('changestatepb/<int:id>',views.changeStatePB,name='cgstatepb'),
    path('changestatepa/<int:id>',views.changeStatePA,name='cgstatepa'),
    path('changestatepd/<int:id>',views.changeStatePD,name='cgstatepd'),
    path('changestateph/<int:id>',views.changeStatePH,name='cgstateph'),
    path('changestatebb/<int:id>',views.changeStateBB,name='cgstatebb'),
    path('changestatesd/<int:id>',views.changeStateSB,name='cgstatesb'),
    path('changestateeb/<int:id>',views.changeStateEB,name='cgstateeb'),
    path('changestatevh/<int:id>',views.changeStateVH,name='cgstatevh'),
    path('changestateaa/<int:id>',views.changeStateAA,name='cgstateaa'),
    path('changestateqd/<int:id>',views.changeStateQD,name='cgstateqd'),
    path('changestatevd/<int:id>',views.changeStateVD,name='cgstatevd'),
    
    
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
   
    #no se estan usando
    path('listaproducto/', views.ListaProducto, name='listproduct'),
    path('nuevoproducto/', views.NuevoProducto, name='newproduct'),
    path('modificarproducto/<int:id>', views.Update, name='updateproduct'),
    path('eliminarproducto/<int:id>', views.EliminarProducto, name='deleteproduct'),
    

    #lista modificar
    path('listaupdatehc/', views.ListaUpdateHC, name='listupdatehc'),
    path('updatehc/<int:id>', views.updateHC, name='updateHC'),
    path('listaupdatekai/', views.ListaUpdateKai, name='listupdatekai'),
    path('updatekai/<int:id>', views.updateKai, name='updateKai'),
]   