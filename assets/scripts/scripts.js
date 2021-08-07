// Make navbar toggle the "scrolled" class when being at scroll position past hero title
 $(window).scroll(function(){
    const vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0)
    // to find distance to title
    var title_position = $(".hero-title").position();
    console.log(title_position);
 $('.nav-panel').toggleClass('scrolled', $(this).scrollTop() > title_position.top-60);
 });



  $(document).ready(function() {
    $(".navbar-toggler").click(function () {
      $(".nav-panel").toggleClass("clicked");
    });
  });