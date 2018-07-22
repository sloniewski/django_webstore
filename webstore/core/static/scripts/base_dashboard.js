$( document ).ready( function(){
    // initialize materialize components
    $('.collapsible').collapsible();
    $('.tooltipped').tooltip();
    $('select').formSelect();

    var elems = document.querySelectorAll('.datepicker');
    var options = {
        format: 'yyyy-mm-dd'
    };
    var instances = M.Datepicker.init(elems, options);

});
