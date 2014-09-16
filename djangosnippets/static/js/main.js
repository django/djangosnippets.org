(function($) {
    function enableFlaggingDialog() {
        var flagForm = $('#flagform'),
            dialog;
        if (flagForm.length) {
            $('#id_flag > option:first-child').remove();
            flagForm.dialog({modal: true, draggable: false});
            flagForm.dialog('close');
            $('#actions .actions__flag').bind('click', function(evt) {
                evt.preventDefault();
                flagForm.dialog('open');
            });
        }
    }

    function enableTagAutocompletion() {
        var snippet_completion = new Snippets.SnippetCompletion();
        snippet_completion.bind_listener('input[name=q]');

        if ($('#id_tags').length > 0) {
            var tag_completion = new Snippets.TagCompletion();
            tag_completion.bind_listener('#id_tags');
        }
    }

    enableFlaggingDialog();
    enableTagAutocompletion();
})(jQuery);
