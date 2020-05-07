
//Obtener tarea

$(document).on('submit','#obtener_tarea', function(e){
    e.preventDefault();
    var id_tarea = $(this).find('#obtener').val();
    console.log('id de la tarea ' + id_tarea);
    $.ajax({
        type:"GET",
        url: "/xp/obtener",
        context: document.body,
        dataType: 'json',
        data: {
            'id_tarea':id_tarea
        },
        success: function (data) {
            document.location.reload();
        }
    });
});

// Inicio del Script para el modal de crear ciclo

$(document).ready(function() {
    $('.js-example-basic-multiple').select2();
    $('#sidebarToggle').click();
});

$(document).on('submit', '#form_ciclo', function (e) {
    e.preventDefault();
    var inicio = $(this).find('#f_inicio').val();
    var fin = $(this).find('#f_fin').val();
    var id_xp = $(this).find('#id_xp').val();
    var selected ="";
    var coma = 0;
    $('#form_ciclo input[type=checkbox]').each(function(){
        if (this.checked) {
            coma++;
            if(coma > 1){
                selected += ','+$(this).val();
            }else{
                selected += $(this).val();
            }     
        }
    });     
    idh = selected;

   
    console.log('Informacion de form');
    console.log(inicio);
    console.log(fin);
    console.log(idh);
    console.log(id_xp);
    console.log('se detuvo el envio de datos');

    $.ajax({
        type: "POST",
        url: "/xp/crearCiclo",
        context: document.body,
        dataType: 'json',
        data: {
            'f_inicio': inicio,
            'f_fin': fin,
            'idh': idh,
            'integrantes': datos,
            'id_xp':id_xp,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (data) {
               alert('Datos enviado');
            }
    });
});



$(document).on('input','#f_inicio', function(e){
    var f_inicio = $(this).val();
    document.getElementById('f_fin').min = f_inicio;
});

$(document).on('input','#f_fin', function(e){
    var f_fin = $(this).val();
    var f_inicio = document.getElementById('f_inicio').value;

    alerta1 = '<div class="alert alert-danger alert-dismissible fade show">'+
                    '<button type="button" class="close" data-dismiss="alert">&times;</button>'+
                    'Primero Ingrese la fecha de inicio'+
                '</div>'

    if(f_inicio == ""){
        document.getElementById('alerta').innerHTML=alerta1;
        document.getElementById('f_fin').value = "dd/mm/aaaa";
        setTimeout(function() { // funcion de Jquery
                $('#alerta').fadeOut(1500);
        },3000);

    }else{
        
        alerta = ' <div class="alert alert-danger alert-dismissible fade show">'+
                    '<button type="button" class="close" data-dismiss="alert">&times;</button>'+
                    'El Sprint no debe durar mas de 4 semanas'+
                '</div>'
    }
        
});


// fin del script del modal crear ciclo

// Agregar integrantes
$(document).on('submit','#agregarIntegrante',function(e){
    e.preventDefault();
    var email = $(this).find('#email').val();
    var rol = $(this).find('#rol').val();
    var idpro = $(this).find('#idpro').val();

    console.log(`email: ${email}`);
    console.log('rol: '+rol);
    console.log('PROYECTO: '+idpro);

    $.ajax({
        type:"POST",
        url:"/xp/agregar_integrantes",
        context: document.body,
        dataType: 'json',
        data:{
            'email':email,
            'rol':rol,
            'idpro':idpro,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(data){
            if(data['datos'] == "NO"){
                $('#error_integrante').text('EL usuario no existe o ya está en el proyecto');
            }else{
                $('#mostrar_integrantes').html(data['datos_integrantes']);
                $('#email').text('');
                $('#rol').selected;
            }
        }
    });
});

// fin de agregar integrantes

// Confirmar tareas

$(document).on('submit','#confirmar_tarea',function(e){
    e.preventDefault();
    alert('Confirmar presionado');
});