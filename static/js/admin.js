$.fn.fresheditor.defaults.commands.insertImage.execCommandValue = function (callback) {
    createImagePicker(
        $('[data-fieldname=body]').parent(),
        function (event) {
            callback($(event.target).parent().parent().attr('data-itemdisplaysrc'));
            $('[data-fieldname=body]').webkitimageresize();
        }
    );
}
$.fn.fresheditor.defaults.enabledCommands.alignment = ["alignleft", "alignright"];
$.fn.fresheditor.defaults.i18n.alignleft = 'Align Left';
$.fn.fresheditor.defaults.i18n.alignright = 'Align Right';
$.fn.fresheditor.defaults.commands.alignleft = { shortcut: "Ctrl+Alt+l", execCommand: ["removeFormat", "unlink", "formatBlock", "justifyLeft"], execCommandValue: [null, null, ["<DIV>"], null], glyphicon: "align-left" };
$.fn.fresheditor.defaults.commands.alignright = { shortcut: "Ctrl+Alt+r", execCommand: ["removeFormat", "unlink", "formatBlock", "justifyRight"], execCommandValue: [null, null, ["<DIV>"], null], glyphicon: "align-right" };

var currently_editing_body = false;

function createImagePicker(insertAt, selected_callback, jsonUrl) {
    jsonUrl = typeof jsonUrl !== 'undefined' ? jsonUrl : '/api/1/selectpicture/';
    var modal_div = $('#picturepicker');
    var imagelist = modal_div.find('#picturelist');
    var i = 0;
    $.getJSON(jsonUrl, {'limit': 35, 'offset': 35 * i++}, function (data) {
        appendImages(data.objects, imagelist, modal_div, selected_callback);
    });
    modal_div.modal();
    modal_div.find('.modal-body').bind(
        'scroll',
        function () {
            if ($(this).scrollTop() + $(this).innerHeight() >= $(this)[0].scrollHeight) {
                $.getJSON(jsonUrl, {'limit': 35, 'offset': 35 * i++}, function (data) {
                    appendImages(data.objects, imagelist, modal_div, selected_callback);
                });
            }
        }
    );
    $('#imageupload').fineUploader(
        {
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
                customHeaders: { 'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val() }
            }
        }).on('complete', function (event, id, filename, responseJSON) {
                  imagelist.empty();
                  createImagePicker(insertAt, selected_callback, jsonUrl)
              }
    );
}


function appendImages(data, imagelist, modal_div, selected_callback) {
    $.each(data, function (index, item) {
        imagelist.append(
            $('<li>')
                .bind(
                'click',
                { modal: modal_div, callback: selected_callback },
                function (event) {
                    event.data['modal'].modal('hide');
                    event.data['callback'](event);
                }
            )
                .attr('data-itemfieldvalue', item.resource_uri)
                .attr('data-itemdisplaysrc', item.displaySrc)
                .append(
                $('<a class="thumbnail" />').append(
                    $('<img/>', {
                        src: item.thumbnailSrc,
                        height: item.thumbnailHeight,
                        width: item.thumbnailWidth,
                        alt: ''
                    })
                )
            )
        );
    });
}

var lengthRegex = /[^\d]*(\d+)[^\d]*/;

ko.bindingHandlers.htmlValue = {
    init: function (element, valueAccessor, allBindingsAccessor) {
        ko.utils.registerEventHandler(
            element, "keyup", function () {
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
        ko.utils.registerEventHandler(
            element, "blur", function () {
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


function DocumentViewModel(data) {
    var self = this;
    ko.mapping.fromJS(data, {}, this);

    $('[data-fieldapiurl]').each(function () {
        var fieldname = $(this).attr('data-fieldname');
        var fieldvalue = $(this).attr('data-fieldvalue');
        self['select' + fieldname] = ko.observableArray([]);
        self['selected' + fieldname] = ko.observable(fieldvalue);
        self['selectedLink' + fieldname] = ko.computed(function () {
            var items = self['select' + fieldname]();
            var si = self['selected' + fieldname]()
            for (var i = 0; i < items.length; i++) {
                if (items[i].id == si) {
                    return items[i].absolute_url;
                }
            }
            return '';
        })
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

    self.save = function () {
        $.ajax(
            {
                url: $('.editthis').attr('data-apiobjecturl'),
                type: 'PUT',
                contentType: 'application/json',
                dataType: 'json',
                data: ko.mapping.toJSON(self),
                success: function () {
                    $('#save_message').modal();
                },
                error: function () {
                    $('#save_error').modal();
                },
                beforeSend: function (jqXHR, settings) {
                    jqXHR.setRequestHeader('X-CSRFToken', $('input[name=csrfmiddlewaretoken]').val());
                }
            }
        );
    };

    self.deleteEvent = function () {
        alert('To do');
        // TODO: deleting
    };

}

function EventViewModel(data) {
    var self = this;
    ko.mapping.fromJS(data, {}, this);

    self.confirmedText = ko.computed(function () {
        if (self.confirmed()) {
            return 'Confirmed';
        } else {
            return 'Not Confirmed';
        }
    });

    self.confirmedClass = ko.computed(function () {
        if (self.confirmed()) {
            return 'btn btn-success btn-sm';
        }
        return 'btn btn-danger btn-sm';
    });

    self.toggleConfirmed = function () {
        self.confirmed(!self.confirmed());
    };

    self.featuredText = ko.computed(function () {
        if (self.featured()) {
            return 'Featured';
        }
        return 'Normal';
    });

    self.featuredClass = ko.computed(function () {
        if (self.featured()) {
            return 'btn btn-info btn-sm';
        }
        return 'btn btn-default btn-sm';
    });

    self.toggleFeatured = function () {
        self.featured(!self.featured());
    };

    self.privateText = ko.computed(function () {
        if (self.private()) {
            return 'Private';
        }
        return 'Public';
    });

    self.privateClass = ko.computed(function () {
        if (self.private()) {
            return 'btn btn-warning btn-sm';
        }
        return 'btn btn-default btn-sm';
    });

    self.togglePrivate = function () {
        self.private(!self.private());
    };

    self.showYear = ko.computed(function () {
        if (typeof(self.year) != 'undefined' && self.year() != '') {
            return ' (' + self.year() + ')';
        }
        return '';
    });

    self.startDateTime = ko.computed(function () {
        if (self.modelType() == 'Season') {
            var item_start = moment(self.startDate() + ' 00:00:00', 'YYYY-MM-DD HH:mm:ss');
        } else {
            var item_start = moment(self.startDate() + ' ' + self.startTime(), 'YYYY-MM-DD HH:mm:ss');
        }
        return item_start.format('YYYY-MM-DD HH:mm:ssZ');
    })

    self.endDateTime = ko.computed(function () {
        if (self.modelType() == 'Film' || self.modelType() == 'Meeting') {
            return '';
        } else if (self.modelType() == 'Season') {
            var item_end = moment(self.endDate() + ' 00:00:00', 'YYYY-MM-DD HH:mm:ss');
        } else {
            var item_start = moment(self.startDate() + ' ' + self.startTime(), 'YYYY-MM-DD HH:mm:ss');
            var item_end = moment(self.startDate() + ' ' + self.endTime(), 'YYYY-MM-DD HH:mm:ss');
            if (item_end < item_start) {
                item_end.add('days', 1);
            }
        }
        return item_end.format('YYYY-MM-DD HH:mm:ssZ');
    })

    self.displayStart = ko.computed(function () {
        // DATETIME_FORMAT
        // python: 'g:i a l j F Y'
        // moment: 'h:mm a dddd D MMMM YYYY'
        //2013-06-23 19:30:00+01:00
        var fmt = 'h:mm a dddd D MMMM YYYY';
        if (self.modelType() == 'Season') {
            var item_start = moment(self.startDate() + ' 00:00:00', 'YYYY-MM-DD HH:mm:ss');
            var item_end = moment(self.endDate() + ' 00:00:00', 'YYYY-MM-DD HH:mm:ss');
            if (item_end.month() == item_start.month()) {
                fmt = 'dddd D';
            } else {
                if (item_end.year() == item_start.year()) {
                    fmt = 'dddd D MMMM';
                } else {
                    fmt = 'dddd D MMMM YYYY';
                }
            }
        } else {
            var item_start = moment(self.startDate() + ' ' + self.startTime(), 'YYYY-MM-DD HH:mm:ss');
            if (self.modelType() != 'Film' && self.modelType() != 'Meeting') {
                var item_end = moment(self.startDate() + ' ' + self.endTime(), 'YYYY-MM-DD HH:mm:ss');
                if (item_end < item_start) {
                    item_end.add('days', 1);
                    if (item_end.month() == item_start.month()) {
                        fmt = 'h:mm a dddd D';
                    } else {
                        if (item_end.year() == item_start.year()) {
                            fmt = 'h:mm a dddd D MMMM';
                        } else {
                            fmt = 'h:mm a dddd D MMMM YYYY';
                        }
                    }
                } else {
                    fmt = 'h:mm a';
                }
            }
        }
        return item_start.format(fmt);
    })

    self.displayEnd = ko.computed(function () {
        var fmt = 'h:mm a dddd D MMMM YYYY';
        if (self.modelType() == 'Film' || self.modelType() == 'Meeting') {
            return '';
        } else if (self.modelType() == 'Season') {
            var item_end = moment(self.endDate() + ' 00:00:00', 'YYYY-MM-DD HH:mm:ss');
            fmt = 'dddd D MMMM YYYY';
        } else {
            var item_start = moment(self.startDate() + ' ' + self.startTime(), 'YYYY-MM-DD HH:mm:ss');
            var item_end = moment(self.startDate() + ' ' + self.endTime(), 'YYYY-MM-DD HH:mm:ss');
            if (item_end < item_start) {
                item_end.add('days', 1);
            }
        }
        return item_end.format(fmt);
    })

    self.lengthNumber = ko.computed(function () {
        if (typeof(self.length) == 'undefined') return '';
        return self['length']().replace(lengthRegex, "$1");
    })

    self.isolength = ko.computed(function () {
        return 'PT' + self.lengthNumber() + 'M';
    })

    self.lengthLabel = ko.computed(function () {
        return self.lengthNumber() + ' minutes';
    })

    self.websiteVisible = ko.computed(function () {
        return (typeof(self.website) != 'undefined' && self.website() != '');
    })

    $('[data-fieldapiurl]').each(function () {
        var fieldname = $(this).attr('data-fieldname');
        var fieldvalue = $(this).attr('data-fieldvalue');
        self['select' + fieldname] = ko.observableArray([]);
        self['selectedLink' + fieldname] = ko.computed(function () {
            var items = self['select' + fieldname]();
            for (var i = 0; i < items.length; i++) {
                if (items[i].resource_uri == self[fieldname]()) {
                    return items[i].absolute_url;
                }
            }
            return '';
        })
        self['selectedLabel' + fieldname] = ko.computed(function () {
            var items = self['select' + fieldname]();
            for (var i = 0; i < items.length; i++) {
                if (items[i].resource_uri == self[fieldname]()) {
                    if (typeof items[i].name == 'undefined') {
                        return items[i].title;
                    } else {
                        return items[i].name;
                    }
                }
            }
            return '';
        })
        self['selectedVisible' + fieldname] = ko.computed(function () {
            return ((fieldname == 'season') && (self[fieldname]() != '/api/1/selectseason/2/'));
        })
        $.getJSON($(this).attr('data-fieldapiurl') + '?limit=0', function (data) {
            self['select' + fieldname](data.objects);
            self[fieldname](fieldvalue);
        })
    })

    self.pictureData = ko.observable();

    self.getPictureData = function () {
        if (self.picture() == null) {
            self.pictureData(
                {
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
                }
            );
        } else {
            $.ajax(
                {
                    url: self.picture(),
                    dataType: 'json',
                    async: false,
                    success: function (data) {
                        self.pictureData(data);
                    }
                    // TODO: deal with fails.
                }
            );
        }
    }

    self.getPictureData();

    $('[data-fieldname="picture"]').on('click.editable', function () {
        createImagePicker(
            $(this),
            function (event) {
                self.picture($(event.target).parent().parent().attr('data-itemfieldvalue'));
                self.getPictureData();
            },
            $(this).attr('data-fieldapiurl')
        );
        return false;
    });

    self.save = function () {
//        console.log(ko.mapping.toJS(self));
        $.ajax(
            {
                url: $('.editthis').attr('data-apiobjecturl'),
                type: 'PUT',
                contentType: 'application/json',
                dataType: 'json',
                data: ko.mapping.toJSON(self),
                success: function () {
                    $('#save_message').modal().on('hidden.bs.modal', function (e) { window.location.replace('?editing'); });
                },
                error: function () {
                    $('#save_error').modal();
                },
                beforeSend: function (jqXHR, settings) {
                    jqXHR.setRequestHeader('X-CSRFToken', $('input[name=csrfmiddlewaretoken]').val());
                }
            }
        );
    };

    self.deleteEvent = function () {
        self.deleted = true;
        self.save();
    };

    self.restoreEvent = function () {
        self.deleted = false;
        self.save();
    };

}

var startEdit = function () {
    if (typeof editThis === 'undefined') {
        $.getJSON($('.editthis').attr('data-apiobjecturl'), function (data) {
            data['modelType'] = $('.editthis').attr('data-modeltype');
            if (data['modelType'] === 'document' || data['modelType'] == 'minutes' || data['modelType'] == 'page') {
                editThis = new DocumentViewModel(data);
            } else {
                editThis = new EventViewModel(data);
            }
            ko.applyBindings(editThis);
        });
        $('[data-fieldname=body]')
            .fresheditor()
            .parent()
            .on(
            'focusin.edit_event',
            function () {
                $('html').addClass('editing');
                currently_editing_body = true;
            }
        )
            .on(
            'focusout.edit_event',
            function () {
                $('html').removeClass('editing');
                currently_editing_body = false;
            }
        );
    }
    $('#container').css('margin-left', '615px');
    $('#start_edit').off('click.edit_event');
    $('#start_edit').on('click.edit_event', cancelEdit);
    $('[data-fieldname=body]').webkitimageresize().fresheditor('edit', true);
    $('#adminarea').show();
}
var cancelEdit = function () {
    // TODO: check if there are unsaved changes and prompt for confirm.
    $('#adminarea').hide();
    $('#container').css('margin-left', 'auto');
    $('[data-fieldname=body]').fresheditor('edit', false);
    $('#start_edit').off('click.edit_event');
    $('#start_edit').on('click.edit_event', startEdit);
}

$('#start_edit').on('click.edit_event', startEdit);

if (location.search.indexOf('?editing') >= 0) {
    $('#start_edit').trigger('click.edit_event');
}