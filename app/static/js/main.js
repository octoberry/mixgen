$(document).ready(function () {

    var frm = $('.selectTrackForm');

    var generator = $("#generatorContainer");
    var player = $("#playerContainer");
    var generatorForm = $(".generatorForm");

    frm.submit(function (ev) {
        ev.preventDefault();
        var $form = $(this);
        $.ajax({
            type: "POST",
            url: GLOBAL.AJAX_TRACK_URL,
            data: $form.serialize(),
            dataType: 'json',
            success: function (data, textStatus, jqXHR) {
                player.html('<iframe width="560" height="315" src="//www.youtube.com/embed/'+data.id+'" frameborder="0" allowfullscreen></iframe>');
                generatorForm.find('input[name="track_id"]').val(data.track_id);
                generator.removeClass('hide');
            },
            error: function (jqXHR, textStatus, errorThrown) {
                alert('Error')
            }
            });
        })
    })
