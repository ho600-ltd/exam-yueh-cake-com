$(document).ajaxStart(function() {
    var $loading_image = $('#loading');
    $loading_image.css({
        position: 'fixed',
        top: '50%',
        left: '50%'
    });
    if ($loading_image.attr('status') != 'disable') {
        $.blockUI({
            baseZ: 9000,
            message: null
        });
        $loading_image.css('z-index', 10000).show();
    }
}).ajaxStop(function() {
    var $loading_image = $('#loading');
    if ($loading_image.attr('status') != 'disable') {
        $.unblockUI();
        $loading_image.hide();
    }
});


function show_modal($modal, title, body) {
    $('.modal-title', $modal).html(title);
    $('.modal-body', $modal).html(body);
    $modal.modal({
        keyboard: true
    });
};


var ALLOW_UPLOAD_FILENAMES = [
    '0A.asc',
    '1A.asc',
    '2A.asc',
    '3A.asc',
    '4A.asc',
    '5A.asc',
    '6A.asc',
    '7A.asc',
    '8A.asc',
    '9A.asc'
];
function send_encrypt_content($self) {
    return function() {
        var openpgp = window.openpgp;
        var $form = $self.parents('form');
        var filename = $('input[name=filename]', $form).val();
        var ho600_public_key = $('textarea[name=ho600_public_key]', $form).val();
        var public_key_content = $('textarea[name=public_key_content]', $form).val();
        var raw_content = $('textarea[name=encrypt_content]', $form).val();
        var encrypt_content;

        if (!filename || !ho600_public_key || !public_key_content || !raw_content) {
            show_modal($('#danger_modal'), 'Input Error', 'filename/ho600_public_key/public_key_content/raw_content are required!');
            return false;
        } else if (ALLOW_UPLOAD_FILENAMES.indexOf(filename) < 0) {
            show_modal($('#danger_modal'), 'Filename Error', 'filename only accept "0A.asc ~ 9A.asc" !');
            return false;
        } else if (/http:\/\/openpgpjs.org/.test(raw_content)) {
            show_modal($('#danger_modal'), 'Encrypt Error', 'Already Encrypted!');
            return false;
        }

        var keys = openpgp.key.readArmored(ho600_public_key).keys;
        keys.push(openpgp.key.readArmored(public_key_content).keys[0]);
        options = {data: raw_content, publicKeys: keys};
        openpgp.encrypt(options).then(function(ciphertext) {
            if(!confirm("Are you sure to send the answer? You can not modify the answer anymore.")) {
                return false;
            }
            encrypt_content = ciphertext.data;
            $('textarea[name=encrypt_content]', $form).val(encrypt_content);
            var data = {
                "public_key_content": public_key_content,
                "filename": filename,
                "encrypt_content": encrypt_content
            };
            $.ajax({
                url: "https://pqpmeji6f4.execute-api.us-west-2.amazonaws.com/prod/uploadpgpfiletos3/",
                data: JSON.stringify(data),
                type: 'POST',
                contentType: 'application/json',
                dataType: 'json',
                complete: function(xhr, text) {
                    if (/\b200\b/.test(xhr.responseText)) {
                        var json = $.parseJSON(xhr.responseText);
                        $('textarea[name=encrypt_content]',
                            $form).val("Please wait for the question!"
                        ).css({'readonly': 'readonly', 'disabled': 'disabled'});
                        var url = json['message'] + '/index.html';
                        var message = 'Please go to <a href="'+url+'">'+url+'</a>';
                        show_modal($('#primary_modal'), 'Register Successfully', message);
                    } else {
                        show_modal($('#danger_modal'), 'Error', xhr.responseText);
                    }
                }
            });
        });
    };
};


$(document).ready(function() {
    $('form').submit(false);

    $('.click-trigger').click(function() {
        var $btn = $(this);
        var function_name = $btn.attr('function_name');
        if (window[function_name]) {
            return window[function_name]($btn)();
        }
    }).show();

    $('.modal').on('hidden.bs.modal', function(e) {
        //INFO 在 modal 上，再 show #search_zipcode_modal ，並關掉 #search_zipcode_modal 後，原 modal 就無法 scroll 了。
        if ($('.modal.in').length > 0) {
            $('#id_body').addClass('modal-open');
        } else {
            $('#id_body').removeClass('modal-open');
        }
    });
});