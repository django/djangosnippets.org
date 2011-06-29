Snippets = window.Snippets || {};


(function(S, $) {

  var TagCompletion = function(options) {
    this.options = options || {};
    this.default_url = '/snippets/tag-hint/';
  };
  
  function clean_and_split(text, delimiter) {
    var cleaned = [],
        pieces = text.split(delimiter || ',');
    
    for (var i = 0; i < pieces.length; i++) {
      if (pieces[i].match(/\w+/)) {
        cleaned.push(pieces[i].replace(/^\s+|\s+$/, ''));
      }
    }
    return cleaned;
  }
  
  function get_last_piece(text) {
    var cleaned = clean_and_split(text, ',');
    if (cleaned.length > 0) {
      var last = cleaned[cleaned.length - 1];
      if (last.match(/\w+/))
        return last;
    }
  };
  
  TagCompletion.prototype.fetch_results = function(request, response) {
    var url = this.options.url || this.default_url,
        term = request.term,
        last_piece = get_last_piece(term);
    
    if (!last_piece)
      response([]);
    
    var pieces = clean_and_split(term),
        all_but_last = '';
    pieces.pop();
    
    if (pieces.length > 0)
      all_but_last = pieces.join(', ') + ', ';
    
    $.getJSON(url, {'q': last_piece}, function(data) {
      var results = [];
      $.each(data, function(k, v) {
        v.label = v.tag + ' (' + v.count + ')';
        v.value = all_but_last + v.tag + ', ';
        results.push(v);
      });
      response(results);
    });
  };
  
  TagCompletion.prototype.bind_listener = function(input_sel) {
    var self = this;
    
    this.input_element = $(input_sel);
    
    this.input_element.autocomplete({
      minLength: self.options.min_length || 3,
      source: function(request, response) {self.fetch_results(request, response);},
    });
  };
  
  var SnippetCompletion = function(options) {
    this.options = options || {};
    this.default_url = '/search/autocomplete/';
  };
  
  SnippetCompletion.prototype.render_item = function(ul, item) {
    var html = '<a href="'+item.url+'">'+item.label+'</a>';
    
    return $('<li></li>')
      .data('item.autocomplete', item)
      .append(html)
      .appendTo(ul);
  }
  
  SnippetCompletion.prototype.fetch_results = function(request, response) {
    var term = request.term,
        url = this.options.url || this.default_url;
    
    $.getJSON(url, {'q': term}, function(data) {
      var results = [];
      $.each(data, function(k, v) {
        results.push({
          'label': v.title,
          'value': v.title,
          'url': v.url
        });
      });
      response(results);
    });
  };
  
  SnippetCompletion.prototype.bind_listener = function(input_sel) {
    var self = this;
    
    this.input_element = $(input_sel);
    
    this.input_element.autocomplete({
      minLength: self.options.min_length || 3,
      source: function(request, response) {self.fetch_results(request, response);},
    }).data('autocomplete')._renderItem = this.render_item;
  };

  S.TagCompletion = TagCompletion;
  S.SnippetCompletion = SnippetCompletion;

})(Snippets, jQuery);
