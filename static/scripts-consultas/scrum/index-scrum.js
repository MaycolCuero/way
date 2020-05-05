

$(document).on('submit','#form_confirmar',function(e){
    e.preventDefault();
    var tarea = $(this).find('#id_tarea').val();
    console.log('id de la tarea'+tarea);
    $.ajax({
        type:"POST",
        url:"/usuarios/confirmar",
        context: document.body,
        dataType: 'json',
        data:{
            'id':tarea,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(dato){
            if (dato['datos'] == "guardados"){
                window.location.reload();
            }else{
                console.log('hubo un problema al guardar los datos');
            }
        }
    });
});