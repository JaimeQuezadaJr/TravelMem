document.addEventListener("DOMContentLoaded", function(){
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function(element){
        return new bootstrap.Popover(element);
    });
});