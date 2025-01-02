(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();
    
    
    // Initiate the wowjs
    new WOW().init();
    
    
    // Dropdown on mouse hover
    const $dropdown = $(".dropdown");
    const $dropdownToggle = $(".dropdown-toggle");
    const $dropdownMenu = $(".dropdown-menu");
    const showClass = "show";
    
    $(window).on("load resize", function() {
        if (this.matchMedia("(min-width: 992px)").matches) {
            $dropdown.hover(
            function() {
                const $this = $(this);
                $this.addClass(showClass);
                $this.find($dropdownToggle).attr("aria-expanded", "true");
                $this.find($dropdownMenu).addClass(showClass);
            },
            function() {
                const $this = $(this);
                $this.removeClass(showClass);
                $this.find($dropdownToggle).attr("aria-expanded", "false");
                $this.find($dropdownMenu).removeClass(showClass);
            }
            );
        } else {
            $dropdown.off("mouseenter mouseleave");
        }
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Facts counter
    $('[data-toggle="counter-up"]').counterUp({
        delay: 10,
        time: 2000
    });


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        margin: 25,
        dots: false,
        loop: true,
        nav : true,
        navText : [
            '<i class="bi bi-arrow-left"></i>',
            '<i class="bi bi-arrow-right"></i>'
        ],
        responsive: {
            0:{
                items:1
            },
            768:{
                items:2
            }
        }
    });
    
})(jQuery);

$(function() {
    // Check-in datepicker
    $('#date1').datetimepicker({
        format: 'L',
        minDate: new Date(),  // Bugungi kundan oldingi sanalarni tanlash mumkin emas
        icons: {
            time: "fa fa-clock",
            date: "fa fa-calendar",
            up: "fa fa-chevron-up",
            down: "fa fa-chevron-down",
            previous: 'fa fa-chevron-left',
            next: 'fa fa-chevron-right',
            today: 'fa fa-screenshot',
            clear: 'fa fa-trash',
            close: 'fa fa-remove'
        }
    });

    // Check-out datepicker
    $('#date2').datetimepicker({
        format: 'L',
        useCurrent: false, // Muhim: false qiymati berilishi kerak
        icons: {
            time: "fa fa-clock",
            date: "fa fa-calendar",
            up: "fa fa-chevron-up",
            down: "fa fa-chevron-down",
            previous: 'fa fa-chevron-left',
            next: 'fa fa-chevron-right',
            today: 'fa fa-screenshot',
            clear: 'fa fa-trash',
            close: 'fa fa-remove'
        }
    });

    // Check-in o'zgarganda check-out minimal sanasini yangilash
    $("#date1").on("change.datetimepicker", function (e) {
        $('#date2').datetimepicker('minDate', e.date);
    });

    // Check-out o'zgarganda check-in maksimal sanasini yangilash
    $("#date2").on("change.datetimepicker", function (e) {
        $('#date1').datetimepicker('maxDate', e.date);
    });
});

/*** Booking page ***/
document.addEventListener('DOMContentLoaded', function() {
    const checkinInput = document.getElementById('checkinDate');
    const checkoutInput = document.getElementById('checkoutDate');

    // Bugungi sanani olish
    const today = new Date().toISOString().split('T')[0];
    
    // Dastlabki minimal sanalarni o'rnatish
    checkinInput.min = today;
    checkoutInput.min = today;

    checkinInput.addEventListener('change', function() {
        // Check-out minimal sanasini check-in sanasidan keyingi kunga o'rnatish
        if (this.value) {
            const nextDay = new Date(this.value);
            nextDay.setDate(nextDay.getDate() + 1);
            const minCheckout = nextDay.toISOString().split('T')[0];
            checkoutInput.min = minCheckout;
        } else {
            // Agar check-in tanlanmagan bo'lsa, bugungi kunni min qilib qo'yamiz
            checkoutInput.min = today;
        }
        
        // Agar check-out sanasi check-in sanasidan oldin bo'lsa, uni tozalash
        if (checkoutInput.value && checkoutInput.value <= this.value) {
            checkoutInput.value = '';
        }
    });

    checkoutInput.addEventListener('change', function() {
        if (checkinInput.value) {
            // Check-out sanasi check-in sanasidan oldin bo'lmasligi kerak
            if (this.value <= checkinInput.value) {
                this.value = '';
                this.classList.add('invalid');
                alert('Check-out date must be after check-in date');
            } else {
                this.classList.remove('invalid');
            }
        }
    });
});
