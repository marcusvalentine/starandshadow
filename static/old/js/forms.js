$(function() {
	$(".datePicker").datepicker({
		dateFormat : 'yy-mm-dd',
	});
	$(".dateTimePicker").datetimepicker({
		dateFormat : 'yy-mm-dd',
		timeFormat : 'h:m',
		hour : 19,
		minute : 30
	});
	$(".timePicker").timepicker({
		timeFormat : 'h:m',
		hour : 21,
		minute : 30
	});
	d = new Date();
	d.setHours(19);
	d.setMinutes(30);
	d.setSeconds(0);
	$(".datePicker").each(function(i) {
		if($(this).datetimepicker('getDate') == null) {
			$(this).datetimepicker('setDate', d);
		}
	});
	$(".dateTimePicker").each(function(i) {
		if($(this).datetimepicker('getDate') == null) {
			$(this).datetimepicker('setDate', d);
		}
	})
	d.setHours(21);
	$(".timePicker").each(function(i) {
		if($(this).datetimepicker('getDate') == null) {
			$(this).datetimepicker('setDate', d);
		}
	});
	$('#id_body').wysiwyg({
		autoGrow: true,
		rmUnusedControls: true,
		controls: {
			bold: { visible: true },
			italic: { visible: true },
			createLink: { visible: true },
			insertImage: { visible: true },
			h1: { visible: true },
			h2: { visible: true },
			h3: { visible: true },
			h4: { visible: true },
			h5: { visible: true },
			h6: { visible: true },
			paragraph: { visible: true },
			html: { visible: true }
		},
		rmUnwantedBr: true,
		formHeight: 600,
		formWidth: 1000,
		initialContent: ''
	});
	$.wysiwyg.fileManager.setAjaxHandler("http://www.starandshadow.org.uk/upload/file-manager.php");
});
