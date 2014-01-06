$('#myTab a').click(function (e) {
  e.preventDefault()
  $(this).tab('show')
})

$('#myTab a[href="#details"]').tab('show') // Select tab by name
$('#myTab a[href="#errors"]').tab('show') // Select tab by name
$('#myTab a[href="#messages"]').tab('show') // Select tab by name