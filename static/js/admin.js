$.fn.fresheditor.defaults.commands.insertImage.execCommandValue = function (callback) {
    createImagePicker($('[data-fieldname=body]').parent(), function (event, ui) {
        var s = $(ui.selected);
        callback(s.attr('data-itemsrc'));
    });
}
$.fn.fresheditor.defaults.enabledCommands.alignment = ["alignleft", "alignright"];
$.fn.fresheditor.defaults.i18n.alignleft = 'Align Left';
$.fn.fresheditor.defaults.i18n.alignright = 'Align Right';
$.fn.fresheditor.defaults.commands.alignleft = { shortcut: "Ctrl+Alt+l", execCommand: ["removeFormat", "unlink", "formatBlock", "justifyLeft"], execCommandValue: [null, null, ["<DIV>"], null] };
$.fn.fresheditor.defaults.commands.alignright = { shortcut: "Ctrl+Alt+r", execCommand: ["removeFormat", "unlink", "formatBlock", "justifyRight"], execCommandValue: [null, null, ["<DIV>"], null] };

function createImagePicker(insertAt, selectedCallback, jsonUrl) {
    jsonUrl = typeof jsonUrl !== 'undefined' ? jsonUrl : '/api/1/selectpicture/';
    var dialogdiv = $('<div id="imagepicker" title="Select Image"/>');
    var addnewbutton = $('<div id="imageupload">');
    var imagelist = $('<ul id="imagelist"/>')
        .selectable({ selected: function (event, ui) {
            dialogdiv.dialog('close');
            selectedCallback(event, ui);
        }});
    var i = 0;
    $.getJSON(jsonUrl, {'limit': 35, 'offset': 35 * i++}, function (data) {
        appendImages(data.objects, imagelist);
    });
    dialogdiv
        .append(addnewbutton)
        .append(imagelist)
        .bind('scroll', function () {
            if ($(this).scrollTop() + $(this).innerHeight() >= $(this)[0].scrollHeight) {
                $.getJSON(jsonUrl, {'limit': 35, 'offset': 35 * i++}, function (data) {
                    appendImages(data.objects, imagelist);
                });
            }
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
                .attr('data-itemfieldvalue', item.resource_uri)
                .append($('<img/>', {
                    src: item.thumbnailSrc,
                    height: item.thumbnailHeight,
                    width: item.thumbnailWidth,
                    alt: ''
                }))
        );
    });
}

//---------------------------------------------------------------
// Knockout stuff
//---------------------------------------------------------------

var lengthRegex = /[^\d]*(\d+)[^\d]*/;

ko.bindingHandlers.htmlValue = {
    init: function (element, valueAccessor, allBindingsAccessor) {
        ko.utils.registerEventHandler(element, "keyup", function () {
                var modelValue = valueAccessor();
                var elementValue = element.innerHTML;
                if (ko.isWriteableObservable(modelValue)) {
                    modelValue(elementValue);

                } else { //handle non-observable one-way binding
                    var allBindings = allBindingsAccessor();
                    if (allBindings['_ko_property_writers'] && allBindings['_ko_property_writers'].htmlValue) allBindings['_ko_property_writers'].htmlValue(elementValue);
                }
            }
        )
    },
    update: function (element, valueAccessor) {
        var value = ko.utils.unwrapObservable(valueAccessor()) || "";
        if (element.innerHTML !== value) {
            element.innerHTML = value;
        }
    }
};

function EventViewModel(data) {
    var self = this;
    ko.mapping.fromJS(data, {}, this);

    self.showYear = ko.computed(function () {
        if (self.year() != '') {
            return ' (' + self.year() + ')';
        }
        return '';
    });

    self.startDateTime = ko.computed(function () {
        return '';
    })

    self.endDateTime = ko.computed(function () {
        return '';
    })

    self.lengthNumber = ko.computed(function () {
        return self['length']().replace(lengthRegex, "$1");
    })

    self.isolength = ko.computed(function () {
        return 'PT' + self.lengthNumber() + 'M';
    })

    self.lengthLabel = ko.computed(function () {
        return self.lengthNumber() + ' minutes';
    })

    $('[data-fieldapiurl]').each(function () {
        var fieldname = $(this).attr('data-fieldname');
        var fieldvalue = $(this).attr('data-fieldvalue');
        self['select' + fieldname] = ko.observableArray([]);
        self['selected' + fieldname] = ko.observable(fieldvalue);
        self['selectedLabel' + fieldname] = ko.computed(function () {
            var items = self['select' + fieldname]();
            var si = self['selected' + fieldname]()
            for (var i = 0; i < items.length; i++) {
                if (items[i].id == si) {
                    if (typeof items[i].name == 'undefined') {
                        return items[i].title;
                    } else {
                        return items[i].name;
                    }
                }
            }
            return '';
        })
        $.getJSON($(this).attr('data-fieldapiurl') + '?limit=0', function (data) {
            self['select' + fieldname](data.objects);
            self['selected' + fieldname](fieldvalue);
        })
    })

    self.pictureData = ko.observable();

    self.getPictureData = function () {
        if (self.picture() == null) {
            self.pictureData({
                displayHeight: "400",
                displaySrc: "/static/cache/55/c3/55c3b98863eb12bb833799dd6613a3c0.jpg",
                displayWidth: "400",
                file: "/static/img/events/filler.png",
                height: "400",
                id: 789,
                modified: "2012-05-11",
                resource_uri: "/api/1/selectpicture/789/",
                slug: "filler.png",
                src: "/static/img/events/filler.png",
                thumbnailHeight: "100",
                thumbnailSrc: "/static/cache/a9/73/a973b47c595c935a74d73f2fe29e18a5.jpg",
                thumbnailWidth: "100",
                width: "400"
            });
        } else {
            $.ajax({
                url: self.picture(),
                dataType: 'json',
                async: false,
                success: function (data) {
                    self.pictureData(data);
                }
            });
        }
    }

    self.getPictureData();
    $('[data-fieldname="picture"]').on('click.editable', function () {
        createImagePicker($(this), function (event, ui) {
            self.picture($(ui.selected).attr('data-itemfieldvalue'));
            self.getPictureData();
        }, $(this).attr('data-fieldapiurl'));
        return false;
    });

    self.save = function () {
        console.log(ko.mapping.toJS(self));
        $.ajax({
            url: $('.editthis').attr('data-apiobjecturl'),
            type: 'PUT',
            contentType: 'application/json',
            dataType: 'json',
            data: ko.mapping.toJSON(self),
            success: function () {
                console.log("success")
            },
            error: function () {
                console.log("error")
            },
            beforeSend: function (jqXHR, settings) {
                jqXHR.setRequestHeader('X-CSRFToken', $('input[name=csrfmiddlewaretoken]').val());
            }
        });
    };
    self.deleteEvent = function () {
        alert('To do');
    };
}

$('#container').css('margin', '0 0 0 550px');

$.getJSON($('.editthis').attr('data-apiobjecturl'), function (data) {
    editThis = new EventViewModel(data);
    ko.applyBindings(editThis);
});

$('[data-fieldname=body]').parent().fresheditor().webkitimageresize();
$('.fresheditor-toolbar').hide();
$('.datePicker').datepicker({ dateFormat: 'yy-mm-dd' });
$('.timePicker').timepicker({
    timeFormat: 'HH:mm:ss',
    stepMinute: 5,
    showSecond: false
});
$('#editbodybutton').on('click.bodyeditable', function () {
    $('[data-fieldname=body]').fresheditor('edit', true);
    $('.editthis').addClass('editable');
    $(this).hide();
    $('.fresheditor-toolbar').show();
    $('#donebodybutton').show();
    return false;
})
$('#donebodybutton').on('click.bodyeditable', function () {
    $('[data-fieldname=body]').fresheditor('edit', false);
    $('.editthis').removeClass('editable');
    $(this).hide();
    $('.fresheditor-toolbar').hide();
    $('#editbodybutton').show();
    return false;
})
$('#logged-in-menu').menu();

//---------------------------------------------------------------
//---------------------------------------------------------------