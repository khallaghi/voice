var bestPictures = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  // prefetch: 'search/asghar/کسری',
  remote: {
    url: '/search/asghar/%QUERY.json',
    wildcard: '%QUERY'
  }
});

$('#remote .typeahead').typeahead(null, {
  name: 'best-pictures',
  display: 'value',
  source: bestPictures
});