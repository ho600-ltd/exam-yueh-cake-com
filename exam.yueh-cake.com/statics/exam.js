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

        var ho600_public_keys = openpgp.key.readArmored(ho600_public_key).keys;
        try {
            var public_keys = openpgp.key.readArmored(public_key_content).keys;
        } catch (err) {
            show_modal($('#danger_modal'), 'Public Key Format Error', err.message);
            return false;
        } finally {
            if (public_keys.length == 0) {
                show_modal($('#danger_modal'), 'Public Key Format Error', "Could not import your public key!");
                return false;
            }
        }
        var keys = [];
        keys.push(ho600_public_keys[0]);
        keys.push(public_keys[0]);

        try {
            var raw_content_message = openpgp.cleartext.readArmored(raw_content);
        } catch (err) {
            show_modal($('#danger_modal'), 'Answer Format Error', err.message);
            return false;
        }
        var v_options = {
            message: raw_content_message,
            publicKeys: public_keys
        };
        openpgp.verify(v_options).then(function(verified){
            if(!verified.signatures[0].valid) {
                show_modal($('#danger_modal'), 'Sign Error', 'The answer has no valid signature!');
                return false;
            } else {
                var options = {data: raw_content, publicKeys: keys};
                openpgp.encrypt(options).then(function(ciphertext) {
                    if(!confirm("Are you sure to send the answer? You can not modify the answer anymore.")) {
                        return false;
                    }
                    encrypt_content = ciphertext.data;
                    $('textarea[name=encrypt_content]', $form).val(encrypt_content);
                    var data = {
                        "filename": filename,
                        "encrypt_content": encrypt_content
                    };
                    if (filename == "0A.asc") {
                        data['public_key_content'] = public_key_content;
                    }

                    $.ajax({
                        url: "https://pqpmeji6f4.execute-api.us-west-2.amazonaws.com/prod/uploadpgpfiletos3/",
                        crossDomain: true,
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
                                if (json['message'] == filename) {
                                    show_modal($('#primary_modal'), 'Upload Successfully', filename + ' is uploaded');
                                } else {
                                    var url = '/' + json['message'] + '/index.html';
                                    var message = 'Please go to <a href="'+url+'">'+url+'</a>, and keep the url path in mind.  That is a combination of your public key email and id.';
                                    show_modal($('#primary_modal'), 'Register Successfully', message);
                                }
                            } else {
                                var json = $.parseJSON(xhr.responseText);
                                show_modal($('#danger_modal'), 'Error', json['message']);
                            }
                        }
                    });
                });
            }
        });
    };
};


function append_asc (url) {
    if (url == '0A.asc') {
        return false;
    }
    var $0a = $('#0A');
    var $ul = $0a.parent();
    $ul.append($('<li><a target="_blank" href="'+url+'">'+url+'</a></li>'));
}
function wait_for_the_next_exam () {
    $('textarea[name=encrypt_content]').val('Please wait for the next exam').css('background-color', '#d1d1d1');
    $('input[function_name=send_encrypt_content]').hide();
}


function check_asc_files (index) {
    if (parseInt(index) > 9) {
        var $li = $('form').parent();
        $('form').remove();
        $li.append($('<li>It is finish.</li>'));
        return false;
    }
    var d = new Date();
    var timestamp = d.getTime();
    var list = ['A', 'Q'];
    var a_url = index+list[0]+'.asc';
    $.ajax({
        type: 'HEAD',
        url: a_url+'?timestamp='+timestamp,
        success: function (json) {
            append_asc(a_url);
            console.log('success: '+ a_url);
            index = parseInt(index) + 1;
            var q_url = index+list[1]+'.asc';
            $.ajax({
                type: 'HEAD',
                url: q_url+'?timestamp='+timestamp,
                success: function (json) {
                    append_asc(q_url);
                    console.log('success: '+ q_url);
                    $('input[name=filename]').val(index+'A.asc');
                    check_asc_files(index);
                },
                error: function () {
                    console.log('error: '+q_url);
                    wait_for_the_next_exam();
                }
            });
        },
        error: function () {
            console.log('error: '+a_url);
        }
    });

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

    if ($('#0A:visible').length > 0) {
        $('#register_note').remove();
        check_asc_files('0');
    }
});