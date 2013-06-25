$.fn.fresheditor.defaults.commands.insertImage.execCommandValue = function (callback) {
    createImagePicker($('[data-modelfield=body]').parent(), function (event, ui) {
        var s = $(ui.selected);
        callback(s.attr('data-itemsrc'));
    });
}
$.fn.fresheditor.defaults.enabledCommands.alignment = ["alignleft", "alignright"];
$.fn.fresheditor.defaults.i18n.alignleft = 'Align Left';
//$.fn.fresheditor.defaults.i18n.aligncenter = 'Center';
$.fn.fresheditor.defaults.i18n.alignright = 'Align Right';
$.fn.fresheditor.defaults.commands.alignleft = { shortcut: "Ctrl+Alt+l", execCommand: ["removeFormat", "unlink", "formatBlock", "justifyLeft"], execCommandValue: [null, null, ["<DIV>"], null] };
//$.fn.fresheditor.defaults.commands.aligncenter = { shortcut: "Ctrl+Alt+c", execCommand: ["removeFormat", "unlink", "formatBlock", "justifyCenter"], execCommandValue: [null, null, ["<DIV>"], null] };
$.fn.fresheditor.defaults.commands.alignright = { shortcut: "Ctrl+Alt+r", execCommand: ["removeFormat", "unlink", "formatBlock", "justifyRight"], execCommandValue: [null, null, ["<DIV>"], null] };

function showMessage(level, mess, topic) {
    topic = typeof topic !== 'undefined' ? topic : '';
    $('#adminarea .message').last().after('<div class="message ' + level + ' ' + topic + '">' + mess + '</div>');
}

function replaceMessage(level, mess, topic) {
    deleteMessages(topic);
    showMessage(level, mess, topic);
}

function deleteMessages(topic) {
    $('#adminarea .message.' + topic).remove();
}

function findMessage() {
    var mess = getURLParameter('mess');
    if (mess != 'null') {
        showMessage('info', mess);
    }
}

findMessage();

// Business Logic

$('button').button();

$('button.approvedialog').click(function (event) {
    dialogdiv = $('#approvedialog');
    approvalDialog(event);
    return false;
});

$('button.unapproveitem').click(function (event) {
    item = $('.editthis');
    unapproveProgrammeItem(item.attr('data-modeltype'), item.attr('data-modelid'));
    return false
});

$('button.confirmitem').click(function (event) {
    item = $('.editthis');
    confirmProgrammeItem(item.attr('data-modeltype'), item.attr('data-modelid'), true);
    return false
});

$('button.unconfirmitem').click(function (event) {
    item = $('.editthis');
    confirmProgrammeItem(item.attr('data-modeltype'), item.attr('data-modelid'), false);
    return false
});

//$('a.button[disabled]').button({ disabled:true });
//$('a.button[hidden]').hide();

$('.startapproving').on('click.approving', function () {
    return approvingToggle('.stopapproving', '.startapproving', { 'approvals-meeting': $('[data-modeltype=Meeting]').attr('data-modelid') });
})

$('.stopapproving').on('click.approving', function () {
    return approvingToggle('.startapproving', '.stopapproving', {});
})

function approvalDialog(event) {
    item = $('.editthis');
    $.ajax({
        url: '/api/approvaldata/',
        type: 'POST',
        dataType: 'json',
        data: {
            'itemtype': item.attr('data-modeltype'),
            'itemid': item.attr('data-modelid')
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        success: function (data) {
            dialogdiv.empty();
            for (var i = 0; i < data.sections.length; i++) {
                dialogdiv.append($(data.sections[i]));
            }
            dialogdiv
                .attr('title', 'Approve - ' + item.find('[data-modelfield=title]').text())
                .dialog({
                    height: 800,
                    width: 880,
                    modal: true,
                    create: function (event, ui) {
                        $("html").css('overflow', 'hidden');
                    },
                    beforeClose: function (event, ui) {
                        $("html").css('overflow', 'inherit');
                    }
                });
            $('a.button.approveitem').button().click(function (event) {
                approveProgrammeItem(item.attr('data-modeltype'), item.attr('data-modelid'), $('#meetingselectlist').find('option:selected').attr('value'));
                dialogdiv.dialog('close');
                return false;
            });
        },
        error: function (data) {
            replaceMessage(data['status'], data['message'], 'approveitem');
        }
    });
}

function approvingToggle(onThing, offThing, data) {
    $.ajax({
        url: '/api/setmeeting/',
        type: 'POST',
        dataType: 'json',
        data: data,
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        success: function (data) {
            replaceMessage(data['status'], data['message'], 'approving');
            $(offThing).attr('disabled', true).button({ disabled: true }).hide();
            $(onThing).attr('disabled', false).button({ disabled: false }).show();
            window.location.replace(document.URL.split("?")[0].split("#")[0]);
        },
        error: function (data) {
            showMessage(data['status'], data['message'], 'approving');
        }
    });
    return false;
}

function approveProgrammeItem(itemtype, itemid, meetingid) {
    $.ajax({
        url: '/api/approveevent/',
        type: 'POST',
        dataType: 'json',
        data: {
            'itemtype': itemtype,
            'itemid': itemid,
            'meetingid': meetingid
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        success: function (data) {
            replaceMessage(data['status'], data['message'], 'approveitem');
            if (data['status'] == 'success') {
                window.location.replace(document.URL.split("?")[0].split("#")[0]);
            }
        },
        error: function (data) {
            replaceMessage(data['status'], data['message'], 'approveitem');
        }
    });
}

function unapproveProgrammeItem(itemtype, itemid) {
    $.ajax({
        url: '/api/unapproveevent/',
        type: 'POST',
        dataType: 'json',
        data: {
            'itemtype': itemtype,
            'itemid': itemid
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        success: function (data) {
            replaceMessage(data['status'], data['message'], 'approveitem');
            if (data['status'] == 'success') {
                window.location.replace(document.URL.split("?")[0].split("#")[0]);
            }
        },
        error: function (data) {
            replaceMessage(data['status'], data['message'], 'approveitem');
        }
    });
}

function confirmProgrammeItem(itemtype, itemid, confirm) {
    $.ajax({
        url: '/api/confirmitem/',
        type: 'POST',
        dataType: 'json',
        data: {
            'itemtype': itemtype,
            'itemid': itemid,
            'confirm': confirm
        },
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        success: function (data) {
            replaceMessage(data['status'], data['message'], 'confirmitem');
            if (data['status'] == 'success') {
                window.location.replace(document.URL.split("?")[0].split("#")[0]);
            }
        },
        error: function (data) {
            replaceMessage(data['status'], data['message'], 'confirmitem');
        }
    });
}

$('#editbutton').on('click.editable', function () {
    $('[data-modelfield=body]').fresheditor();
    $('#adminarea .message.success').remove();
    return startEditing();
});

$('#deletebutton').on('click.editable', function () {
    var confirmed = confirm('Are you sure you want to delete "' + $('[data-modelfield=title]').text() + '"');
    if (confirmed) {
        $.ajax({
            url: $('.editthis').attr('data-apiurl'),
            type: 'DELETE',
            success: deleteWorked,
            error: deleteFailed
        });
    }
    return false;
});

function startEditing() {
    $('#editbutton').button({ disabled: true }).off('click.editable').on('click', function () {
        return false;
    });
    $('#savebutton').button({ disabled: false }).on('click.editable', finishEditing);
    $('[data-modelfield=body]').parent()
        .addClass('editable')
        .webkitimageresize();
    $('.fresheditor-toolbar').show();
    $('[data-fieldtype=ForeignKeyPicture]').removeAttr('height');
    $('[data-whileediting=show]').show();
    $('[data-whileediting=hide]').hide();
    $('[data-modelfield]').addClass('editable').widgetize();
    replaceMessage('info', 'Now editing "' + $('[data-modelfield=title]').text() + '"', 'editing');
    return false;
}

function finishEditing() {
    $('#savebutton').button({ disabled: true }).off('click.editable');
    $('#editbutton').button({ disabled: false }).on('click.editable', startEditing);
    $('[data-modelfield=body]').fresheditor('edit', false);
    $('.fresheditor-toolbar').hide();
    $('button[data-fieldtype]').attr('disabled', true);
    $('[data-whileediting=show]').hide();
    $('[data-whileediting=hide]').show();
    var itemData = {};
    $('[data-modelfield]').removeClass('editable').off('click.editable').each(function () {
        switch ($(this).attr('data-fieldtype')) {
            case 'CharField':
                itemData[$(this).attr('data-modelfield')] = getFieldValueCharField($(this));
                break;
            case 'ForeignKey':
                itemData[$(this).attr('data-modelfield')] = getFieldValueForeignKey($(this));
                break;
            case 'ForeignKeyPicture':
                itemData[$(this).attr('data-modelfield')] = getFieldValueForeignKeyPicture($(this));
                break;
            case 'TextField':
                itemData[$(this).attr('data-modelfield')] = getFieldValueTextField($(this));
                break;
            case 'PlainTextField':
                itemData[$(this).attr('data-modelfield')] = getFieldValuePlainTextField($(this));
                break;
            case 'URLField':
                itemData[$(this).attr('data-modelfield')] = getFieldValueURLField($(this));
                break;
            case 'BooleanField':
                itemData[$(this).attr('data-modelfield')] = getFieldValueBooleanField($(this));
                break;
            case 'DateField':
                itemData[$(this).attr('data-modelfield')] = getFieldValueDateField($(this));
                break;
            case 'TimeField':
                itemData[$(this).attr('data-modelfield')] = getFieldValueTimeField($(this));
                break;
        }
    });
    if (itemData['picture'] == '789') {
        delete itemData['picture'];
    }
    replaceMessage('warn', 'Saving, please wait.', 'editing');
    if ($('.editthis').attr('data-modelid') == 'None') {
        $.ajax({
            url: $('.editthis').attr('data-apiurl'),
            type: 'POST',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify(itemData),
            success: createWorked,
            error: createFailed,
            beforeSend: function (jqXHR, settings) {
                jqXHR.setRequestHeader('X-CSRFToken', $('input[name=csrfmiddlewaretoken]').val());
            }
        });
    } else {
        $.ajax({
            url: $('.editthis').attr('data-apiurl'),
            type: 'PUT',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify(itemData),
            success: updateWorked,
            error: updateFailed,
            beforeSend: function (jqXHR, settings) {
                jqXHR.setRequestHeader('X-CSRFToken', $('input[name=csrfmiddlewaretoken]').val());
            }
        });
    }
    return false;
}

function createWorked(data) {
    replaceMessage(data['status'], data['message'], 'editing');
    if ($('.editthis').attr('data-modeltype') == 'Minutes') {
        window.location.replace('/org/minutes/' + data.id);
    } else {
        window.location.replace(document.URL.substring(0, document.URL.length - 1) + data['instance'].id);
    }
}

function createFailed(data) {
    replaceMessage(data['status'], data['message'], 'editing');
}

function updateWorked(data) {
    replaceMessage(data['status'], data['message'], 'editing');
    window.location.replace(document.URL.split("?")[0]);
}

function updateFailed(data) {
    replaceMessage(data['status'], data['message'], 'editing');
}

function deleteWorked(data) {
    replaceMessage(data['status'], data['message'], 'editing');
    window.location.replace('/org/on/');
}

function deleteFailed(data) {
    replaceMessage(data['status'], data['message'], 'editing');
}

function createImageFieldPicker() {
    var t = $(this);
    createImagePicker(t, function (event, ui) {
        var s = $(ui.selected);
        t
            .attr('data-fieldvalue', s.attr('data-itemfieldvalue'))
            .attr('src', s.attr('data-itemsrc'))
            .attr('data-src', s.attr('data-itemdatasrc'));
    }, t.attr('data-fieldapiurl'));
    return false;
}

function createImagePicker(insertAt, selectedCallback, jsonUrl) {
    jsonUrl = typeof jsonUrl !== 'undefined' ? jsonUrl : '/api/select/graphic/';
    var dialogdiv = $('<div id="imagepicker" title="Select Image"/>');
    var addnewbutton = $('<div id="imageupload">');
    var imagelist = $('<ul id="imagelist"/>')
        .selectable({ selected: function (event, ui) {
            dialogdiv.dialog('close');
            selectedCallback(event, ui);
        }});
    var i = 0;
    $.getJSON(jsonUrl, {'page': i++}, function (data) {
        appendImages(data, imagelist);
    });
    dialogdiv
        .append(addnewbutton)
        .append(imagelist)
        .bind('scroll', function () {
            if ($(this).scrollTop() + $(this).innerHeight() >= $(this)[0].scrollHeight) {
                $.getJSON(jsonUrl, {'page': i++}, function (data) {
                    appendImages(data, imagelist);
                });
            }
            ;
        });
    insertAt.after(dialogdiv);
    $('#imagepicker').dialog({
        height: 600,
        width: 880,
        modal: true,
        create: function (event, ui) {
            $("html").css('overflow', 'hidden');
        },
        beforeClose: function (event, ui) {
            $("html").css('overflow', 'inherit');
        }
    });
    addnewbutton.fineUploader({
        multiple: false,
        validation: {
            allowedExtensions: ['png', 'gif', 'jpg', 'jpeg'],
            sizeLimit: 10000000
        },
        text: {
            uploadButton: 'Add New'
        },
        request: {
            endpoint: '/upload/new/',
            forceMultipart: true,
            inputName: 'slug',
            customHeaders: { 'X-CSRFToken': getCookie('csrftoken') }
        }
    }).on('complete', function (event, id, filename, responseJSON) {
            $('#imagepicker').dialog('close');
            createImagePicker(insertAt, selectedCallback, jsonUrl)
        });
}

function appendImages(data, imagelist) {
    $.each(data, function (index, item) {
        imagelist.append(
            $('<li class="ui-state-default" />')
                .attr('data-itemfieldvalue', item.id)
                .attr('data-itemsrc', item.image.src)
                .attr('data-itemdatasrc', '/static/' + item.url)
                .append($('<img/>', {
                    src: item.thumb.src,
                    height: item.thumb.height,
                    width: item.thumb.width,
                    alt: item.label
                })
                )
        );
    });
}

function imageseelected(event, ui) {
    console.log($(ui.selected).attr('data-selectitemurl'));
}

// Contenteditable features

$.fn.extend({
    widgetize: function () {
        this.each(function () {
            $(this).attr('disabled', false);
            switch ($(this).attr('data-fieldtype')) {
                case 'CharField':
                    $(this).widgetizeCharField();
                    break;
                case 'ForeignKey':
                    $(this).widgetizeForeignKey();
                    break;
                case 'ForeignKeyPicture':
                    $(this).widgetizeForeignKeyPicture();
                    break;
                case 'TextField':
                    $(this).widgetizeTextField();
                    break;
                case 'PlainTextField':
                    $(this).widgetizePlainTextField();
                    break;
                case 'URLField':
                    $(this).widgetizeURLField();
                    break;
                case 'BooleanField':
                    $(this).widgetizeBooleanField();
                    break;
                case 'DateField':
                    $(this).widgetizeDateField();
                    break;
                case 'TimeField':
                    $(this).widgetizeTimeField();
                    break;
            }
        })
    },
    widgetizeCharField: function () {
        $(this).on('click.editable', function () {
            var t = $(this);
            var textbox = $('<input>', {
                type: 'text',
                name: t.attr('data-modelfield'),
                value: t.text()
            }).css('width', '300px');
            textbox.bind('focusout change', {t: t}, function () {
                var i = $(this);
                t.text(i.attr('value'));
                i.remove();
                t.show();
            });
            t.hide().after(textbox);
            textbox.focus();
            return false;
        })
    },
    widgetizeForeignKey: function () {
        $(this).on('click.editable', function () {
            var t = $(this);
            var dropdown = $('[name=' + t.attr('data-modelfield') + ']');
            if (dropdown.length == 1) {
                dropdown.show();
                t.hide();
            } else {
                $.getJSON(t.attr('data-fieldapiurl'), function (data) {
                    dropdown = $('<select>', {
                        name: t.attr('data-modelfield')
                    }).css('max-width', '300px');
                    $.each(data, function (index, item) {
                        dropdown.append($("<option/>", {
                            value: item.id,
                            text: item.label,
                            selected: (item.id == t.attr('data-fieldvalue'))
                        }).attr('data-selectitemurl', item.url));
                    });
                    dropdown.bind('focusout change', {t: t}, function () {
                        var i = $(this);
                        var s = i.find('option:selected');
                        if (t.children('a').length == 0) {
                            t.attr('data-fieldvalue', s.attr('value')).text(s.text());
                        } else {
                            t.attr('data-fieldvalue', s.attr('value')).children('a').attr('href', s.attr('data-selectitemurl')).children('span').text(s.text());
                        }
                        i.hide();
                        t.show();
                    });
                    t.hide().after(dropdown);
                    dropdown.focus();
                });
            }
            return false;
        })
    },
    widgetizeForeignKeyPicture: function () {
        $(this).show().on('click.editable', createImageFieldPicker);
    },
    widgetizeTextField: function () {
        $(this).fresheditor('edit', true);
    },
    widgetizePlainTextField: function () {
        $(this).attr('contenteditable', true);
    },
    widgetizeURLField: function () {
        $(this).on('click.editable', function () {
            var t = $(this);
            var textbox = $('<input>', {
                type: 'text',
                name: t.attr('data-modelfield'),
                value: t.attr('href')
            }).css('width', '50%');
            textbox.bind('focusout change', {t: t}, function () {
                var i = $(this);
                t.attr('href', i.attr('value'));
                t.text(i.attr('value'));
                i.remove();
                t.show();
            });
            t.hide().after(textbox);
            textbox.focus();
            return false;
        })
    },
    widgetizeBooleanField: function () {
        $(this).on('click.editable', function () {
            var t = $(this);
            if (t.text() == t.attr('data-iftrue')) {
                t.text(t.attr('data-iffalse')).attr('class', 'false editable');
            } else {
                t.text(t.attr('data-iftrue')).attr('class', 'true editable');
            }
            return false;
        })
    },
    widgetizeDateField: function () {
        $(this).on('click.editable', function () {
            var t = $(this);
            var textbox = $('<input>', {
                type: 'text',
                id: t.attr('data-modelfield'),
                name: t.attr('data-modelfield'),
                value: t.attr('data-fieldvalue')
            }).css('width', '110px');
            textbox.datepicker({
                dateFormat: "yy-mm-dd",
                numberOfMonths: [ 1, 3 ],
                onClose: function (pickedValue) {
                    t.show().attr('data-fieldvalue', pickedValue).text(pickedValue);
                    this.remove();
                }
            }).show();
            t.hide().after(textbox);
            textbox.focus();
            return false;
        })
    },
    widgetizeTimeField: function () {
        $(this).on('click.editable', function () {
            var t = $(this);
            var textbox = $('<input>', {
                type: 'text',
                id: t.attr('data-modelfield'),
                name: t.attr('data-modelfield'),
                value: t.attr('data-fieldvalue')
            }).css('width', '80px');
            textbox.timepicker({
                timeFormat: 'HH:mm',
                stepHour: 1,
                stepMinute: 5,
                onClose: function (pickedValue) {
                    t.show().attr('data-fieldvalue', pickedValue).text(pickedValue);
                    this.remove();
                }
            }).show();
            t.hide().after(textbox);
            textbox.focus();
            return false;
        })
    }
});

function getFieldValueCharField(t) {
    return t.text();
}

function getFieldValueForeignKey(t) {
    return t.attr('data-fieldapiurl') + t.attr('data-fieldvalue') + '/';
}

function getFieldValueForeignKeyPicture(t) {
    return t.attr('data-fieldapiurl') + t.attr('data-fieldvalue') + '/';
}

function getFieldValueTextField(t) {
    alignments = ['left', 'center', 'right'];
    for (var i = 0; i < alignments.length; i++) {
        t.find('p[style*=' + alignments[i] + '],div[style*=' + alignments[i] + ']')
            .removeAttr('style')
            .removeClass('left center right imgleft imgcenter imgright')
            .addClass(alignments[i])
            .has('img')
            .removeClass('left center right imgleft imgcenter imgright')
            .addClass('img' + alignments[i]);
    }
    t.find('img').each(function (index, item) {
        item = $(item);
        item.attr('height', item.height());
        item.attr('width', item.width());
    });
    return t.html();
}

function getFieldValuePlainTextField(t) {
    return t.html();
}

function getFieldValueURLField(t) {
    return t.text();
}

function getFieldValueBooleanField(t) {
    return t.text() == t.attr('data-iftrue');
}

function getFieldValueDateField(t) {
    return t.attr('data-fieldvalue');
}

function getFieldValueTimeField(t) {
    return t.attr('data-fieldvalue');
}

if ($('.editthis').attr('data-modelid') == 'None') {
    $('#editbutton').trigger('click.editable');
}