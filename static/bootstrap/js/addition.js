 $(document).ready(function (){
        $('#exampleModal').modal('show')
    })

    $(function(){
        $('[data-countdown]').each(function() {
       var $this = $(this), finalDate = $(this).data('countdown');
       $this.countdown(finalDate, function(event) {
         $this.html(event.strftime('%D days %H hr %M min %S sec'));
       });
     });
    });